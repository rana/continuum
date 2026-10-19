#!/usr/bin/env python3
"""Archived-byte verification and corruption checks; no CSV/model execution."""
import copy
import gzip
import hashlib
import json
from receipt_view import ROOT, SOURCE, BUDGET, encode, make_view


def check(view, raw, native_id):
    if view != make_view(raw, native_id):
        raise ValueError('view differs from exact fixed projection')
    if len(encode(view)) > BUDGET:
        raise ValueError('budget exceeded')
    # Independently partition every leaf, including empty objects/arrays.
    paths = list(view['selected_json_pointers']) + view['omitted_subtrees_json_pointers']
    if len(paths) != len(set(paths)):
        raise ValueError('duplicate coverage')

    def walk(value, path=''):
        if isinstance(value, dict) and value:
            for k, child in value.items():
                walk(child, path + '/' + k.replace('~', '~0').replace('/', '~1'))
        elif isinstance(value, list) and value:
            for i, child in enumerate(value):
                walk(child, path + '/' + str(i))
        elif sum(path == p or path.startswith(p + '/') for p in paths) != 1:
            raise ValueError('incomplete or overlapping coverage')

    walk(json.loads(raw))


def main():
    raw = gzip.decompress((SOURCE / 'verification-receipt.json.gz').read_bytes())
    native_id = json.loads((SOURCE / 'result.json').read_bytes())['receipt']
    logs = [json.loads(line) for line in gzip.decompress((SOURCE / 'native-log.jsonl.gz').read_bytes()).splitlines()]
    native = [json.loads(line['stdout']) for line in logs if line['argv'][1] == 'get']
    fetched = next(obj for obj in native if obj['id'] == native_id)
    assert fetched['object']['type'] == 'blob'
    assert bytes(fetched['object']['bytes']) == raw
    view = json.loads((ROOT / 'receipt-view.json').read_bytes())
    check(view, raw, native_id)
    corrupt = []
    changed = copy.deepcopy(view)
    changed['selected_json_pointers']['/stages/0/result']['checks'] = 12
    corrupt.append((changed, raw, native_id))
    missing = copy.deepcopy(view)
    missing['omitted_subtrees_json_pointers'].pop()
    corrupt.append((missing, raw, native_id))
    corrupt.append((view, raw + b' ', native_id))
    corrupt.append((view, raw, 'sha256:' + '0' * 64))
    for args in corrupt:
        try:
            check(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('corruption accepted')
    one = json.loads((ROOT / 'turn-1-response.json').read_bytes())['structuredContent']
    two = json.loads((ROOT / 'turn-2-response.json').read_bytes())['structuredContent']
    for response in [one, two]:
        assert not response['truncated'] and response['stop_reason'] == 'end_turn'
    first = json.loads(one['text'].removeprefix('```json\n').removesuffix('\n```'))
    assert first['retrieve'] == [{'id': native_id, 'representation': 'receipt-view'}]
    supplied = json.loads((ROOT / 'turn-2-request.json').read_bytes())
    assert supplied['context'].endswith(encode(view).decode())
    # Verify exact replay of prior exposure, not a claim of independent turn two.
    prior = json.loads((ROOT / 'turn-1-request.json').read_bytes())
    assert supplied['prior_exchange'] == [
        {'role': 'user', 'text': prior['context'] + '\n' + prior['request']},
        {'role': 'assistant', 'text': one['text']}]
    result = {'verified': True, 'source_raw_sha256': hashlib.sha256(raw).hexdigest(),
              'view_bytes': len(encode(view)), 'original_bytes': len(raw),
              'coverage_subtrees': len(view['selected_json_pointers']) + len(view['omitted_subtrees_json_pointers']),
              'corruptions_rejected': len(corrupt), 'actual_calls': 2,
              'usage': {k: sum(r['usage'][k] for r in [one, two]) for k in ['input_tokens', 'output_tokens']},
              'new_csv_execution': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
