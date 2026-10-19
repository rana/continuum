#!/usr/bin/env python3
"""Validate archived observations; does not reopen databases or run commands."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_bytes())


def main():
    final = ROOT / 'final'
    result = load('final/result.json')
    cut = load('final/cut-inventory.json')
    assert cut == load('final/restored-before-retries.json') == load('final/restored-after-retries.json')
    live = load('final/live-after-backup.json')
    negative = load('final/main-only-before-native-open.json')
    assert cut['schema'] == live['schema'] == negative['schema']
    assert cut['application_id'] == negative['application_id'] == 0x434f4e54
    assert cut['user_version'] == negative['user_version'] == 1
    assert not negative['heads'] and not negative['events'] and not negative['objects']
    assert len(cut['objects']) == 7 and len(cut['events']) == 3
    assert len(live['objects']) == 9 and len(live['events']) == 4
    assert cut['heads'][0][-1] == 2 and live['heads'][0][-1] == 3
    assert result['pinned_head'] == result['restored_head']
    assert result['live_head_after_backup']['generation'] == 3
    assert result['main_only_copy_head'] is None and result['source_wal_bytes_before_backup'] > 0
    assert result['restored_integrity_check'] == [['ok']] and result['restored_foreign_key_check'] == []
    steps = load('final/backup-progress.json')
    assert len(steps) == result['backup_steps'] == result['pinned_page_count']
    assert {s['total'] for s in steps} == {len(steps)}
    assert [s['remaining'] for s in steps] == list(range(len(steps) - 1, -1, -1))
    assert steps[-1]['status'] == 101 and steps[0]['remaining'] > 0
    logs = [json.loads(line) for line in gzip.decompress((final / 'native-log.jsonl.gz').read_bytes()).splitlines()]
    successes = [(line['argv'], json.loads(line['stdout'])) for line in logs if line['returncode'] == 0]
    fetched = [(argv, value) for argv, value in successes if argv[1] == 'get']
    for object_id, _ in cut['objects']:
        values = [obj for argv, obj in fetched if argv[-1] == object_id]
        assert len(values) == 2 and values[0] == values[1]
        assert values[0]['id'] == object_id
    historic = [json.loads(row[-1]) for row in cut['events']]
    assert result['exact_replays'] == [{'receipt': r, 'replayed': True} for r in historic]
    for receipt in historic:
        assert any(argv[1] == 'accept' and value == {'receipt': receipt, 'replayed': True}
                   for argv, value in successes)
    late_root = result['live_head_after_backup']['root']
    assert late_root not in {row[0] for row in cut['objects']}
    assert late_root in {row[0] for row in live['objects']}
    assert result['late_operation_retry_error'] == {'error': 'object not found: ' + late_root}
    assert result['operation_conflict_error'] == {'error': 'operation ID was already used for a different request'}
    errors = [json.loads(line['stderr']) for line in logs if line['returncode'] != 0]
    assert result['late_operation_retry_error'] in errors
    assert result['operation_conflict_error'] in errors
    assert result['binary_sha256'] == load('build-provenance.json')['binary_sha256']
    response = load('claude-response.json')['structuredContent']
    assert not response['truncated'] and response['stop_reason'] == 'end_turn'
    print(json.dumps({'verified': True, 'native_objects_compared': 7, 'exact_replays': 3,
                      'cut_generation': 2, 'later_live_generation': 3,
                      'schema_compared': True, 'new_execution': False}, indent=2))


if __name__ == '__main__':
    main()
