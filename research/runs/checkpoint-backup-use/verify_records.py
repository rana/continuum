#!/usr/bin/env python3
"""Verify retained backup-use observations without execution or inference."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_bytes())


def main():
    result = load('observed/result.json')
    checkpoint = load('observed/checkpoint-input.json')
    assert checkpoint == json.loads((ROOT.parent / 'source-bound-verification/checkpoint/checkpoint.json').read_bytes())
    assert result['context_pack'] == checkpoint['context_pack']
    assert result['checkpoint_source_snapshot'] == checkpoint['source']['snapshot']
    rendered = (ROOT / 'observed/restored-context.jsonl').read_bytes()
    assert rendered == (ROOT.parent / 'source-bound-verification/checkpoint/context.jsonl').read_bytes()
    assert len(rendered) == result['rendered_bytes'] == 5420
    assert hashlib.sha256(rendered).hexdigest() == result['rendered_sha256']
    logs = [json.loads(line) for line in gzip.decompress((ROOT / 'observed/native-log.jsonl.gz').read_bytes()).splitlines()]
    success = [(r['argv'], json.loads(r['stdout'])) for r in logs if r['returncode'] == 0]
    gets = [(argv[-1], obj) for argv, obj in success if argv[1] == 'get']
    assert len(result['objects_compared']) == result['backup_report']['objects'] == 17
    for record in result['objects_compared']:
        values = [obj for object_id, obj in gets if object_id == record['id']]
        assert len(values) == 2 and values[0] == values[1]
        assert values[0]['id'] == record['id']
        assert hashlib.sha256(json.dumps(values[0], sort_keys=True).encode()).hexdigest() == record['get_envelope_sha256']
    original = result['original_acceptance_receipt']
    replays = [value for argv, value in success if argv[1] == 'accept' and value.get('replayed')]
    assert replays == [{'receipt': original, 'replayed': True}] * 2
    assert result['source_head'] == result['restored_verification']['freshness']['observed']
    assert result['source_head']['generation'] == 1
    assert result['restored_head_after_probe']['generation'] == 2
    assert result['restored_verification']['freshness']['status'] == 'matches_at_observation'
    old = result['historical_verification_after_probe']
    assert old['exact_projection_verified'] and old['freshness']['status'] == 'stale_at_observation'
    assert not old['action_authority_verified']
    failures = [json.loads(r['stderr']) for r in logs if r['returncode'] != 0]
    assert failures == [result['current_verification_error_after_probe']]
    assert result['published_export_bytes_unchanged'] and result['source_logical_inventory_unchanged']
    assert not result['new_inference'] and not result['new_csv_execution']
    # Both historical model and local execution payloads were part of the exact copy.
    retained_ids = {r['id'] for r in result['objects_compared']}
    state = json.loads((ROOT.parent / 'source-bound-verification/authored-work-state.json').read_bytes())
    for attempt in state['attempts']:
        assert attempt['source_snapshot'] in retained_ids
        assert attempt['request'] in retained_ids and attempt['receipt'] in retained_ids
    print(json.dumps({'verified': True, 'objects_compared': 17, 'rendered_bytes': 5420,
                      'exact_original_replays': 2, 'restored_copy_freshness_change': True,
                      'new_execution': False}, indent=2))


if __name__ == '__main__':
    main()
