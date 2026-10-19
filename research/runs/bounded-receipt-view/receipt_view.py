#!/usr/bin/env python3
"""Fixed CSV-pilot projection, not a native or general JSON-view API."""
import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'source-bound-verification'
BUDGET = 16384


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def make_view(raw, blob_id):
    receipt = json.loads(raw)
    if receipt['schema'] != 'continuum.csv_verification_receipt.v1':
        raise ValueError('unsupported receipt')
    # Fixed selectors. Unknown fields are omitted explicitly, never silently copied.
    names = ['schema', 'operation_id', 'request', 'request_sha256', 'source_snapshot',
             'started_utc', 'finished_utc', 'passed', 'source_unchanged_after_checks', 'scope']
    selected = {'/' + k: copy.deepcopy(receipt[k]) for k in names}
    if len(receipt['stages']) != 2:
        raise ValueError('expected two pilot stages')
    for i in range(2):
        for k in ['stage', 'argv', 'returncode', 'worker', 'result']:
            selected[f'/stages/{i}/{k}'] = copy.deepcopy(receipt['stages'][i][k])
    omitted = []

    def walk(value, path):
        if path in selected:
            return
        if not any(p.startswith(path + '/') for p in selected):
            omitted.append(path)
            return
        if isinstance(value, dict):
            for key, child in value.items():
                escaped = key.replace('~', '~0').replace('/', '~1')
                walk(child, path + '/' + escaped)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, path + '/' + str(i))
        else:
            raise ValueError('selector cannot descend through scalar')

    walk(receipt, '')
    view = {'schema': 'continuum.csv_receipt_view.pilot.v1',
            'source': {'native_blob_id': blob_id, 'raw_bytes': len(raw),
                       'raw_sha256': hashlib.sha256(raw).hexdigest(),
                       'repository_file': '../source-bound-verification/verification-receipt.json.gz'},
            'selector': 'fixed-fields-v1', 'budget_bytes': BUDGET,
            'selected_json_pointers': selected, 'omitted_subtrees_json_pointers': omitted,
            'limits': 'Exact selected JSON values; omitted subtrees remain in the original Blob. '
                      'Custody and local assertions do not authenticate execution or prove portability. '
                      'No child inputs, outputs or individual assertions are exposed in this view.'}
    if len(encode(view)) > BUDGET:
        raise ValueError('view exceeds budget; no truncation allowed')
    return view


def main():
    raw = gzip.decompress((SOURCE / 'verification-receipt.json.gz').read_bytes())
    result = json.loads((SOURCE / 'result.json').read_bytes())
    view = make_view(raw, result['receipt'])
    (ROOT / 'receipt-view.json').write_bytes(encode(view))
    print(json.dumps({'view_bytes': len(encode(view)), 'original_bytes': len(raw),
                      'omitted_subtrees': len(view['omitted_subtrees_json_pointers'])}))


if __name__ == '__main__':
    main()
