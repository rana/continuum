#!/usr/bin/env python3
"""Check archived observations; no database or inference execution."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    result = json.loads((ROOT / 'result.json').read_bytes())
    assert result['writer_transaction_open_before'] and result['writer_transaction_open_after']
    assert result['reservation'] == 'BEGIN IMMEDIATE; no data changes'
    assert len(result['baseline']) == len(result['held']) == len(result['released']) == 3
    for before, held, after in zip(result['baseline'], result['held'], result['released']):
        assert before['argv'] == held['argv'] == after['argv']
        assert before['returncode'] == after['returncode'] == 0
        assert before['stdout'] == after['stdout']
        assert held['returncode'] == 1 and held['stdout'] == ''
        assert json.loads(held['stderr']) == {'error': 'database error: database is locked'}
    control = result['read_only_control']
    head = json.loads(result['baseline'][1]['stdout'])
    receipt = json.loads(result['baseline'][2]['stdout'])
    assert head == {'root': control['root'], 'generation': control['generation']}
    assert receipt == control['receipt']
    assert control['canonical_object_bytes'] > 0 and control['flags'] == 'SQLITE_OPEN_READ_ONLY'
    assert result['logical_history_unchanged'] and result['sqlite_version'] == '3.53.2'
    response = json.loads((ROOT / 'claude-response.json').read_bytes())['structuredContent']
    assert response['stop_reason'] == 'end_turn' and not response['truncated']
    print(json.dumps({'verified': True, 'baseline_commands': 3, 'held_busy_failures': 3,
        'released_commands': 3, 'same_build_sqlite_read_only_control': True,
        'new_execution': False}, indent=2))


if __name__ == '__main__':
    main()
