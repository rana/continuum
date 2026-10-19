#!/usr/bin/env python3
"""Offline retained-sample checks, no timings or child processes rerun."""
import hashlib
import json
import pathlib
import statistics
import struct

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
r = json.loads((HERE / 'result.json').read_text())
for p in (HERE / 'check.py', HERE / 'PLAN.md', HERE.parent / 'recovery-sync/fail_sync.c'):
    pin = next(item for item in r['sources'] if item['path'] == str(p.relative_to(ROOT)))
    assert p.stat().st_size == pin['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest() == pin['sha256']


def identity(kind, data):
    return 'sha256:' + hashlib.sha256(b'continuum.object\0\0\1' + bytes([kind]) + data).hexdigest()


def blob(stage):
    return identity(1, struct.pack('>I', 128) + bytes([stage]) * 128)


def snapshot(stage):
    path = b'sample.bin'
    return identity(2, struct.pack('>I', 1) + struct.pack('>I', len(path)) + path + bytes.fromhex(blob(stage)[7:]))


def head(stage):
    return dict(root=snapshot(stage), generation=stage + 1)


def receipt(stage):
    return dict(sequence=stage + 1,
                request=dict(acceptor='probe', target='source', operation_id=f'update-{stage}',
                             expected=None if stage == 0 else head(stage - 1), candidate=snapshot(stage)),
                outcome='accepted', observed=None if stage == 0 else head(stage - 1), resulting=head(stage))


assert len(r['cells']) == 9 and len(r['samples']) == 369
assert {(c['updates'], c['repeat']) for c in r['cells']} == {(n, i) for n in (1, 16, 64) for i in range(3)}
for cell in r['cells']:
    n = cell['updates']
    assert cell['objects'] == cell['independent_final_objects'] == 2 * n
    assert cell['accepted_outcomes'] == n and cell['independent_final_outcomes'] == n + 2
    assert cell['source_blob_bytes'] == 128 * n
    assert 0 < cell['journal_bytes'] < cell['journal_bytes_after_timed_stale'] < 1_048_576
    for op, calls in cell['sync_observations'].items():
        expected = ['journal', 'boundary', 'store', 'parent']
        if op == 'new_stale':
            expected += ['WRITE-IN-PROGRESS', 'store', 'journal', 'boundary.pending', 'store', 'store']
        assert calls == expected
    samples = [s for s in r['samples'] if (s['updates'], s['repeat']) == (n, cell['repeat'])]
    for op in ('get', 'head', 'receipt', 'retry', 'duplicate_put', 'new_stale'):
        selected = [s for s in samples if s['operation'] == op]
        assert len(selected) == (1 if op == 'new_stale' else 8)
        wanted = {'get': dict(type='blob', bytes=[n - 1] * 128), 'head': head(n - 1),
                  'receipt': receipt(n - 1), 'retry': dict(receipt=receipt(0), replayed=True),
                  'duplicate_put': dict(id=blob(n - 1)),
                  'new_stale': dict(receipt=dict(sequence=n + 1,
                      request=dict(acceptor='probe', target='source', operation_id='stale-timed',
                                   expected=None, candidate=snapshot(n - 1)),
                      outcome='precondition_failed', observed=head(n - 1), resulting=head(n - 1)), replayed=False)}[op]
        for sample in selected:
            assert sample['returncode'] == 0 and sample['stderr'] == '' and sample['elapsed_ns'] > 0
            assert json.loads(sample['stdout']) == wanted
for summary in r['summaries']:
    values = [s['elapsed_ns'] for s in r['samples'] if (s['updates'], s['operation']) == (summary['updates'], summary['operation'])]
    assert (summary['samples'], summary['median_ns'], summary['min_ns'], summary['max_ns']) == (len(values), statistics.median(values), min(values), max(values))
assert r['filesystem'] == 'tmpfs'
print('PASS: retained 369 exact results, independent object IDs/receipts, sync observations, summaries and probe-source custody; tmpfs scope explicit')
