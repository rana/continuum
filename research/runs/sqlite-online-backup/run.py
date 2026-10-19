#!/usr/bin/env python3
"""Disposable native-store experiment using Python's SQLite Online Backup API."""
import argparse
from contextlib import closing
import hashlib
import json
import platform
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def inventory(connection):
    return {
        'application_id': connection.execute('PRAGMA application_id').fetchone()[0],
        'user_version': connection.execute('PRAGMA user_version').fetchone()[0],
        'schema': connection.execute('SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name').fetchall(),
        'objects': connection.execute('SELECT id,hex(canonical) FROM objects ORDER BY id').fetchall(),
        'heads': connection.execute('SELECT * FROM heads ORDER BY acceptor,target').fetchall(),
        'events': connection.execute('SELECT sequence,acceptor,target,operation_id,hex(request),receipt FROM events ORDER BY sequence').fetchall(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    binary_sha = hashlib.sha256(binary.read_bytes()).hexdigest()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    db = out / 'source.db'
    log = out / 'native-log.jsonl'
    counter = 0

    def cli(command, database, *rest, expected=0):
        argv = [str(binary), command, str(database), *map(str, rest)]
        result = subprocess.run(argv, capture_output=True, text=True, timeout=10)
        with log.open('a') as stream:
            stream.write(json.dumps({'argv': argv, 'returncode': result.returncode,
                                     'stdout': result.stdout, 'stderr': result.stderr}) + '\n')
        if result.returncode != expected:
            raise RuntimeError(f'{command} exited {result.returncode}: {result.stderr}')
        return json.loads(result.stdout) if expected == 0 else json.loads(result.stderr)

    def accept(database, request, expected=0):
        nonlocal counter
        counter += 1
        path = out / f'request-{counter}.json'
        path.write_bytes(encoded(request))
        return cli('accept', database, path, expected=expected)

    cli('init', db)
    # Keep an idle connection open before native writes so committed WAL survives.
    keeper = sqlite3.connect(db)
    assert keeper.execute('PRAGMA journal_mode').fetchone()[0] == 'wal'
    demo = cli('demo', db)
    expected_head = demo['current_head']
    assert expected_head['generation'] == 2
    wal = Path(str(db) + '-wal')
    wal_bytes = wal.stat().st_size
    assert wal_bytes > 0
    negative = out / 'main-file-only.db'
    shutil.copyfile(db, negative)
    with closing(sqlite3.connect(negative.as_uri() + '?immutable=1', uri=True)) as copy_conn:
        negative_before_open = inventory(copy_conn)
    (out / 'main-only-before-native-open.json').write_bytes(encoded(negative_before_open))
    assert negative_before_open['heads'] == [] and negative_before_open['events'] == []
    assert negative_before_open['application_id'] == 0x434f4e54
    assert negative_before_open['user_version'] == 1
    negative_head = cli('head', negative, 'demo', 'main')
    assert negative_head != expected_head

    # Explicit read transaction fixes the cut before the callback's native writer.
    source = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)
    source.execute('BEGIN')
    cut = inventory(source)
    (out / 'cut-inventory.json').write_bytes(encoded(cut))
    progress = []
    late = None
    deadline = time.monotonic() + 20

    def step(status, remaining, total):
        nonlocal late
        progress.append({'status': status, 'remaining': remaining, 'total': total})
        if time.monotonic() > deadline:
            raise TimeoutError('bounded experiment backup deadline')
        if late is None:
            assert remaining > 0, 'writer must commit between unfinished backup steps'
            marker = out / 'late.txt'
            marker.write_bytes(b'committed after the pinned backup cut\n')
            blob = cli('blob', db, marker)['id']
            obj = out / 'late-snapshot.json'
            obj.write_bytes(encoded({'type': 'snapshot', 'entries': [{'path': 'late.txt', 'blob': blob}]}))
            root = cli('put', db, obj)['id']
            request = {'acceptor': 'demo', 'target': 'main', 'operation_id': 'after-backup-cut',
                       'expected': expected_head, 'candidate': root}
            accepted = accept(db, request)
            assert accepted['receipt']['outcome'] == 'accepted'
            late = {'blob': blob, 'snapshot': root, 'request': request, 'acceptance': accepted}

    backup = out / 'backup.db'
    destination = sqlite3.connect(backup)
    try:
        source.backup(destination, pages=1, progress=step, sleep=0.01)
    finally:
        destination.close()
        source.rollback()
        source.close()
    assert progress[-1]['status'] == sqlite3.SQLITE_DONE
    assert len({p['total'] for p in progress}) == 1
    assert [p['remaining'] for p in progress] == list(range(progress[0]['total'] - 1, -1, -1))
    assert late is not None
    (out / 'backup-progress.json').write_bytes(encoded(progress))
    # Restore only the CLOSED backup's main file, into a fresh directory.
    restored_dir = out / 'restored'
    restored_dir.mkdir()
    restored = restored_dir / 'work.db'
    assert not Path(str(backup) + '-wal').exists()
    shutil.copyfile(backup, restored)
    restored_sha_before_open = hashlib.sha256(restored.read_bytes()).hexdigest()
    assert restored_sha_before_open == hashlib.sha256(backup.read_bytes()).hexdigest()
    with closing(sqlite3.connect(restored)) as conn:
        restored_inventory = inventory(conn)
        integrity = conn.execute('PRAGMA integrity_check').fetchall()
        foreign_keys = conn.execute('PRAGMA foreign_key_check').fetchall()
    (out / 'restored-before-retries.json').write_bytes(encoded(restored_inventory))
    assert restored_inventory == cut
    assert integrity == [('ok',)] and foreign_keys == []
    restored_head = cli('head', restored, 'demo', 'main')
    assert restored_head == expected_head
    assert cli('events', restored, 'demo', 'main') == [demo[k]['receipt'] for k in ['initial', 'advanced', 'stale_proposal']]
    object_count = 0
    for object_id, _ in cut['objects']:
        assert cli('get', restored, object_id) == cli('get', db, object_id)
        object_count += 1
    replays = []
    for name in ['initial', 'advanced', 'stale_proposal']:
        receipt = demo[name]['receipt']
        assert cli('receipt', restored, 'demo', receipt['request']['operation_id']) == receipt
        retry = accept(restored, receipt['request'])
        assert retry == {'receipt': receipt, 'replayed': True}
        replays.append(retry)
    conflict = dict(demo['initial']['receipt']['request'], candidate=late['snapshot'])
    conflict_error = accept(restored, conflict, expected=1)
    assert 'different request' in conflict_error['error'] or 'operation' in conflict_error['error']
    assert cli('receipt', restored, 'demo', 'after-backup-cut') is None
    for object_id in [late['blob'], late['snapshot']]:
        assert cli('get', restored, object_id, expected=1) == {'error': 'object not found: ' + object_id}
    late_retry_error = accept(restored, late['request'], expected=1)
    assert late_retry_error == {'error': 'object not found: ' + late['snapshot']}
    assert cli('receipt', restored, 'demo', 'after-backup-cut') is None
    assert cli('head', db, 'demo', 'main') == late['acceptance']['receipt']['resulting']
    with closing(sqlite3.connect(restored)) as conn:
        after_retries = inventory(conn)
        (out / 'restored-after-retries.json').write_bytes(encoded(after_retries))
        assert after_retries == cut  # retries/conflict did not alter restored state
    with closing(sqlite3.connect(db)) as conn:
        live = inventory(conn)
        (out / 'live-after-backup.json').write_bytes(encoded(live))
    assert len(live['events']) == len(cut['events']) + 1
    assert len(live['objects']) == len(cut['objects']) + 2
    keeper.close()
    assert hashlib.sha256(binary.read_bytes()).hexdigest() == binary_sha
    result = {'schema': 'continuum.sqlite_backup_experiment.v1',
              'binary': str(binary), 'binary_sha256': binary_sha,
              'python': sys.version, 'python_sqlite': sqlite3.sqlite_version, 'platform': platform.platform(),
              'source_wal_bytes_before_backup': wal_bytes, 'main_only_copy_head': negative_head,
              'pinned_head': expected_head, 'restored_head': restored_head,
              'live_head_after_backup': late['acceptance']['receipt']['resulting'],
              'cut_objects': object_count, 'cut_events': len(cut['events']),
              'live_objects': len(live['objects']), 'live_events': len(live['events']),
              'backup_steps': len(progress), 'pinned_page_count': progress[0]['total'],
              'progress_remaining_strictly_decreased': True, 'writer_committed_between_steps': True,
              'restored_integrity_check': integrity, 'restored_foreign_key_check': foreign_keys,
              'restored_sha256_before_native_open': restored_sha_before_open,
              'exact_replays': replays, 'operation_conflict_error': conflict_error, 'late_operation_retry_error': late_retry_error,
              'late_receipt_absent_from_restore': True, 'late_blob_absent_from_restore': True,
              'restored_inventory_unchanged_after_retries': True,
              'scope': 'Completed local backup, pinned cut and same-binary/schema-version restore; no crash/publication/upgrade/power-loss guarantee.'}
    (out / 'result.json').write_bytes(encoded(result))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
