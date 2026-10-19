#!/usr/bin/env python3
"""Offline verification and exact workload join; no storage/timing invocation."""
import hashlib
import json
import pathlib
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
prior = here.parent / 'cli-cost'
for directory, filesystem in ((prior, 'tmpfs'), (here, 'ext2/ext3')):
    subprocess.run([sys.executable, str(prior / 'verify.py'), '--result', str(directory / 'result.json'),
                    '--filesystem', filesystem], check=True)
a, b = [json.loads((d / 'result.json').read_text()) for d in (prior, here)]
for field in ('binary_sha256', 'binary_bytes', 'sources', 'storage_source_commit', 'base_commit', 'rustc', 'python', 'kernel', 'system', 'machine', 'build_command', 'timing_scope', 'timer'):
    assert a[field] == b[field], field
assert a['cells'] == b['cells'], 'exact workload sizes, identities, histories and sync observations differ'
assert len(a['samples']) == len(b['samples']) == 369
for left, right in zip(a['samples'], b['samples']):
    assert {k:v for k,v in left.items() if k != 'elapsed_ns'} == {k:v for k,v in right.items() if k != 'elapsed_ns'}
selection = json.loads((here / 'selection.json').read_text())
for label, directory in (('earlier', prior), ('filesystem_repeat', here)):
    assert hashlib.sha256((directory / 'result.json').read_bytes()).hexdigest() == selection[label + '_result_sha256']
assert selection['findmnt_fstype'] == 'ext4' and selection['temporary_parent_selection'] == 'new disposable directory on the checkout filesystem via TMPDIR'
assert not selection['physical_device_or_power_loss_qualified']
print('PASS: same binary/source/workload; all 369 response records and nine journal cuts match across separately retained tmpfs and ext4-namespace observations')
