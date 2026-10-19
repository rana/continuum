#!/usr/bin/env python3
"""Check archived implementation comparison; no new native execution."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    result = json.loads((ROOT / 'result.json').read_bytes())
    old = json.loads((ROOT.parent / 'read-writer-reservation/result.json').read_bytes())
    assert result['writer_transaction_open_before'] and result['writer_transaction_open_after']
    assert result['logical_history_unchanged']
    assert len(result['held']) == len(old['held']) == 3
    for before, prior_held, baseline, held, after in zip(old['baseline'], old['held'], result['baseline'], result['held'], result['released']):
        assert prior_held['returncode'] == 1
        assert baseline['returncode'] == held['returncode'] == after['returncode'] == 0
        assert before['stdout'] == baseline['stdout'] == held['stdout'] == after['stdout']
        assert held['stderr'] == ''
    review = json.loads((ROOT / 'claude-response.json').read_bytes())['structuredContent']
    assert not review['truncated'] and review['stop_reason'] == 'end_turn'
    validation = json.loads((ROOT / 'validation.json').read_bytes())
    assert validation['observed_commands'][0]['integration_tests'] == 30
    assert validation['observed_commands'][0]['snapshot_loss_unit_tests'] == 1
    print(json.dumps({'verified': True, 'old_held_failures': 3, 'new_held_successes': 3,
        'exact_output_preserved': True, 'new_execution': False}, indent=2))


if __name__ == '__main__':
    main()
