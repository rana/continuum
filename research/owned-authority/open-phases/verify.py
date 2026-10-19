#!/usr/bin/env python3
"""Offline exact sample/ownership evidence check; no measured process rerun."""
import hashlib
import json
import pathlib
import runpy
import statistics

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
# Also check the earlier retained full-process observation and reuse only its
# independently constructed canonical object/receipt expectations.
helpers = runpy.run_path(str(HERE.parent / 'cli-cost/verify.py'))
r = json.loads((HERE / 'result.json').read_text())
prior = json.loads((HERE.parent / 'cli-cost/result.json').read_text())
for p in (HERE / 'check.py', HERE / 'PLAN.md', HERE.parent / 'framing/src/bin/owned-phase.rs'):
    pin = next(s for s in r['sources'] if s['path'] == str(p.relative_to(ROOT)))
    assert p.stat().st_size == pin['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest() == pin['sha256']
for pin in r['sources']:
    if pin['path'] in {s['path'] for s in prior['sources']}:
        assert pin == next(s for s in prior['sources'] if s['path'] == pin['path'])
assert r['cli_sha256'] == prior['binary_sha256']
assert (r['filesystem'], r['findmnt_fstype']) == ('ext2/ext3','ext4')
assert len(r['cells']) == 9
assert {(c['updates'],c['repeat']) for c in r['cells']} == {(n,i) for n in (1,16,64) for i in range(3)}
for cell in r['cells']:
    n, spec, actual = cell['updates'], cell['spec'], cell['observed']
    assert cell['objects'] == 2*n and cell['outcomes'] == n
    previous = next(c for c in prior['cells'] if (c['updates'],c['repeat']) == (n,cell['repeat']))
    for key in ('journal_sha256','journal_bytes','boundary_sha256'):
        assert cell[key] == previous[key]
    expected = dict(blob_id=helpers['blob'](n-1), blob=dict(type='blob',bytes=[n-1]*128),
                    head=helpers['head'](n-1), receipt=helpers['receipt'](n-1),
                    first_request=helpers['receipt'](0)['request'], first_receipt=helpers['receipt'](0), latest_operation=f'update-{n-1}')
    assert spec == expected
    assert actual['responses'] == dict(get=spec['blob'],head=spec['head'],receipt=spec['receipt'],
                                       retry=dict(receipt=spec['first_receipt'],replayed=True),duplicate_put=spec['blob_id'])
    assert cell['worker_returncode'] == 0 and cell['worker_stderr'] == '' and actual['open_ns'] > 0
    held, released = actual['held_probe'], actual['released_probe']
    assert held['returncode'] != 0 and held['stdout'] == '' and held['stderr']
    assert 'block' in held['stderr'].lower() or 'unavailable' in held['stderr'].lower()
    assert released['returncode'] == 0 and released['stderr'] == '' and json.loads(released['stdout']) == spec['head']
    assert len(actual['samples']) == 640
    for op in ('get','head','receipt','retry','duplicate_put'):
        selected = [s for s in actual['samples'] if s['operation'] == op]
        assert len(selected) == 128 and all(s['elapsed_ns'] > 0 for s in selected)
print('PASS: nine exact histories/response sets, 5760 positive API timings and held/refused then released/successful ownership controls; matching CLI/source custody')
for n in (1,16,64):
    print(n, 'updates: open median ms', statistics.median(c['observed']['open_ns'] for c in r['cells'] if c['updates']==n)/1e6)
