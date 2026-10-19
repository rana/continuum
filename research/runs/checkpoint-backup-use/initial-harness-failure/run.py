#!/usr/bin/env python3
"""Use native export on an existing checkpoint; mutate only a restored copy."""
import argparse
import gzip
import hashlib
import json
import shutil
import sqlite3
import subprocess
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def inventory(database):
    connection = sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)
    try:
        rows = {
            'objects': connection.execute('SELECT id,hex(canonical) FROM objects ORDER BY id').fetchall(),
            'heads': connection.execute('SELECT * FROM heads ORDER BY acceptor,target').fetchall(),
            'events': connection.execute('SELECT sequence,acceptor,target,operation_id,hex(request),receipt FROM events ORDER BY sequence').fetchall(),
            'schema': connection.execute('SELECT type,name,sql FROM sqlite_master ORDER BY type,name').fetchall(),
        }
        return rows
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    binary_sha = digest(binary.read_bytes())
    checkpoint = args.checkpoint.resolve()
    manifest = json.loads((checkpoint / 'checkpoint.json').read_bytes())
    prepare = json.loads((checkpoint / 'prepare.json').read_bytes())
    database = checkpoint / 'work.db'
    before = inventory(database)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / 'checkpoint-input.json').write_text(json.dumps(manifest, indent=2) + '\n')
    pack = manifest['context_pack']
    anchor = prepare['anchor']
    acceptor, target = anchor['acceptor'], anchor['target']
    expected_head = anchor['expected']
    logs = []

    def cli(command, db, *rest, expected=0):
        argv = [str(binary), command, str(db), *map(str, rest)]
        result = subprocess.run(argv, capture_output=True, text=True, timeout=30)
        item = {'argv': argv, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        # Append raw outcome before interpreting or checking it.
        with (out / 'native-log.jsonl').open('a') as stream:
            stream.write(json.dumps(item) + '\n')
        logs.append(item)
        if result.returncode != expected:
            raise RuntimeError(f'{command} exited {result.returncode}: {result.stderr}')
        return json.loads(result.stdout if expected == 0 else result.stderr)

    initial_verification = cli('verify-current-context', database, pack)
    assert initial_verification['exact_projection_verified']
    assert initial_verification['freshness']['status'] == 'matches_at_observation'
    assert initial_verification['freshness']['observed'] == expected_head
    events = cli('events', database, acceptor, target)
    assert len(events) == 1, 'pilot expects the original single checkpoint acceptance'
    original = events[0]
    assert original['resulting'] == expected_head
    exported = out / 'export.db'
    report = cli('backup', database, exported)
    exported_bytes = exported.read_bytes()
    assert digest(exported_bytes) == report['file_sha256']
    assert len(exported_bytes) == report['file_bytes']
    restored_dir = out / 'restored'
    restored_dir.mkdir()
    restored = restored_dir / 'work.db'
    shutil.copyfile(exported, restored)
    assert inventory(restored) == before
    restored_verification = cli('verify-current-context', restored, pack)
    assert restored_verification == initial_verification
    inspection = cli('inspect-context', restored, pack)
    rendered = inspection['rendered'].encode()
    assert rendered == (checkpoint / 'context.jsonl').read_bytes()
    (out / 'restored-context.jsonl').write_bytes(rendered)
    # Every native get checks canonical object identity, in both stores.
    objects = []
    for object_id, _ in before['objects']:
        source = cli('get', database, object_id)
        recovered = cli('get', restored, object_id)
        assert source == recovered
        objects.append({'id': object_id, 'kind': source['object']['type'],
                        'get_envelope_sha256': digest(json.dumps(source, sort_keys=True).encode())})
    request = out / 'original-accept-request.json'
    request.write_text(json.dumps(original['request'], indent=2) + '\n')
    replay = cli('accept', restored, request)
    assert replay == {'receipt': original, 'replayed': True}
    assert inventory(restored) == before
    # Controlled freshness probe affects the restored working copy only.
    marker = out / 'restore-probe.txt'
    marker.write_bytes(b'Disposable restored-copy freshness probe; no recipient or execution claim.\n')
    blob = cli('blob', restored, marker)['id']
    snapshot_path = out / 'probe-snapshot.json'
    snapshot_path.write_text(json.dumps({'type': 'snapshot', 'entries': [{'path': 'probe.txt', 'blob': blob}]}, indent=2) + '\n')
    candidate = cli('put', restored, snapshot_path)['id']
    probe_request = out / 'probe-accept-request.json'
    probe_request.write_text(json.dumps({'acceptor': acceptor, 'target': target,
        'operation_id': 'restored-copy-freshness-probe', 'expected': expected_head, 'candidate': candidate}, indent=2) + '\n')
    advanced = cli('accept', restored, probe_request)
    assert advanced['receipt']['outcome'] == 'accepted'
    assert advanced['receipt']['resulting']['generation'] == expected_head['generation'] + 1
    historical = cli('verify-context', restored, pack)
    assert historical['exact_projection_verified']
    assert historical['freshness']['status'] == 'stale_at_observation'
    current_error = cli('verify-current-context', restored, pack, expected=1)
    assert 'stale' in current_error['error']
    late_replay = cli('accept', restored, request)
    assert late_replay == replay
    assert cli('inspect-context', restored, pack)['rendered'].encode() == rendered
    assert cli('head', database, acceptor, target) == expected_head
    assert inventory(database) == before
    assert exported.read_bytes() == exported_bytes
    assert digest(binary.read_bytes()) == binary_sha
    result = {'schema': 'continuum.checkpoint_backup_use.v1', 'binary_sha256': binary_sha,
        'checkpoint_source_snapshot': manifest['source']['snapshot'], 'context_pack': pack,
        'rendered_bytes': len(rendered), 'rendered_sha256': digest(rendered), 'backup_report': report,
        'source_head': expected_head, 'restored_head_after_probe': advanced['receipt']['resulting'],
        'original_acceptance_receipt': original, 'original_retry_before_and_after_probe': replay,
        'objects_compared': objects, 'restored_verification': restored_verification,
        'historical_verification_after_probe': historical, 'current_verification_error_after_probe': current_error,
        'source_logical_inventory_unchanged': True, 'published_export_bytes_unchanged': True,
        'new_inference': False, 'new_csv_execution': False,
        'scope': 'Backup-use validation; only the disposable restored working copy was advanced. No worker activation or semantic receipt authentication.'}
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'source-inventory.sha256').write_text(digest(json.dumps(before, sort_keys=True).encode()) + '\n')
    # Preserve exact full native outcomes without printing numerical Blob arrays.
    (out / 'native-log.jsonl.gz').write_bytes(gzip.compress((out / 'native-log.jsonl').read_bytes(), mtime=0))
    print(json.dumps({k: v for k, v in result.items() if k != 'objects_compared'}, indent=2))


if __name__ == '__main__':
    main()
