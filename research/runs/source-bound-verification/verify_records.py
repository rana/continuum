#!/usr/bin/env python3
"""Verify the archived capture without rerunning CSV checks or inference."""
import base64
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    path = ROOT / name
    data = path.read_bytes() if path.exists() else gzip.decompress(Path(str(path) + '.gz').read_bytes())
    return json.loads(data)


def decode(record):
    data = base64.b64decode(record['base64'], validate=True)
    assert len(data) == record['bytes']
    assert hashlib.sha256(data).hexdigest() == record['sha256']
    return data


def main():
    request = load('verification-request.json')
    receipt = load('verification-receipt.json')
    request_bytes = gzip.decompress((ROOT / 'verification-request.json.gz').read_bytes())
    assert receipt['request_sha256'] == hashlib.sha256(request_bytes).hexdigest()
    assert receipt['operation_id'] == request['operation_id']
    assert receipt['source_snapshot'] == request['source_snapshot'] == load('result.json')['source_snapshot']
    assert receipt['passed'] and receipt['source_unchanged_after_checks']
    for name in ['capture_driver', 'oracle_script']:
        assert hashlib.sha256(request[name]['utf8'].encode()).hexdigest() == request[name]['sha256']
    counts = []
    all_inputs = []
    for stage in receipt['stages']:
        assert stage['returncode'] == 0 and stage['result']['passed']
        assert stage['worker']['interpreter']['binary_sha256'] == request['interpreter']['binary_sha256']
        assert stage['worker']['capture_driver_sha256'] == request['capture_driver']['sha256']
        decode(stage['stdout'])
        decode(stage['stderr'])
        assert len(stage['children']) == stage['result']['child_processes']
        for child in stage['children']:
            data = decode(child['input'])
            all_inputs.append(data)
            decode(child['stdout'])
            decode(child['stderr'])
            assert child['input_unchanged_after_child']
            assert child['executed_argv'][0] == stage['worker']['interpreter']['executable']
        counts.append((stage['stage'], stage['result']['checks'], len(stage['children'])))
    assert counts == [('tests', 11, 28), ('oracle', 9, 9)]
    assert len(all_inputs) == 37 and any(b'\xff' in data for data in all_inputs)
    oracle = receipt['stages'][1]
    assert len({c['input']['sha256'] for c in oracle['children'][:8]}) == 1
    assert decode(oracle['children'][-1]['input']) == b'a,b\nNA\n'
    observations = json.loads(decode(oracle['stdout']))['observations']
    assert len(observations) == 9
    for child, observed in zip(oracle['children'], observations):
        assert decode(child['stdout']).decode('utf-8') == observed['stdout']
        assert decode(child['stderr']).decode('utf-8') == observed['stderr']
        assert child['returncode'] == observed['returncode']
    first = load('checkpoint/checkpoint.json')
    restored = load('restored-checkpoint/checkpoint.json')
    assert first['context_pack'] == restored['context_pack'] == load('result.json')['context_pack']
    state = load('authored-work-state.json')
    assert len(state['attempts']) == 2
    assert state['attempts'][1]['request'] == receipt['request']
    assert state['attempts'][1]['receipt'] == load('result.json')['receipt']
    assert any(d['id'] == 'known-count-correction' for d in state['decisions'])
    failed = load('fault-check/verification-receipt.json')
    assert not failed['passed']
    fault = failed['stages'][1]
    assert fault['result'] is None and fault['children'] is None
    assert b'fixture outside retained worker directory' in decode(fault['stderr'])
    assert load('fault-check/result.json')['failed_receipt_restored_byte_for_byte']
    print(json.dumps({'verified': True, 'source_snapshot': request['source_snapshot'],
                      'tests': 11, 'oracle_cases': 9, 'retained_actual_child_inputs': len(all_inputs),
                      'failed_receipt_custody_verified': True, 'same_pack_restored': True,
                      'new_execution': False}, indent=2))


if __name__ == '__main__':
    main()
