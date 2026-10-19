#!/usr/bin/env python3
"""Original bounded API/open probe. Disposable checkout-filesystem stores only."""
import argparse
import hashlib
import json
import pathlib
import platform
import statistics
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FRAMING = HERE.parent / 'framing'
sys.path.insert(0, str(FRAMING))
from check_store import independent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(cli, worker, output):
    cli, worker = cli.resolve(), worker.resolve()
    cells = []
    with tempfile.TemporaryDirectory(prefix='.owned-open-probe-', dir=ROOT) as temporary:
        parent = pathlib.Path(temporary)
        filesystem = subprocess.check_output(['stat', '-f', '-c', '%T', str(parent)], text=True).strip()
        fstype = subprocess.check_output(['findmnt', '--noheadings', '--target', str(parent), '--output', 'FSTYPE'], text=True).strip()
        for n in (1, 16, 64):
            for repeat in range(3):
                store, inputs = parent / f'store-{n}-{repeat}', parent / 'input.json'
                def call(command, *args):
                    return json.loads(subprocess.check_output([str(cli), command, str(store), *map(str, args)]))
                def write(value):
                    inputs.write_text(json.dumps(value))
                    return inputs
                call('init')
                head = None
                for i in range(n):
                    blob = dict(type='blob', bytes=[i] * 128)
                    blob_id = call('put', write(blob))['id']
                    snapshot = call('put', write(dict(type='snapshot', entries=[dict(path='sample.bin', blob=blob_id)])))['id']
                    request = dict(acceptor='probe', target='source', operation_id=f'update-{i}', expected=head, candidate=snapshot)
                    accepted = call('accept', write(request))
                    assert not accepted['replayed'] and accepted['receipt']['outcome'] == 'accepted'
                    head = dict(root=snapshot, generation=i + 1)
                    assert accepted['receipt']['resulting'] == head
                    if i == 0:
                        first_request, first_receipt = request, accepted['receipt']
                spec = dict(blob_id=blob_id, blob=blob, head=head, receipt=accepted['receipt'],
                            first_request=first_request, first_receipt=first_receipt, latest_operation=f'update-{n - 1}')
                baseline = {name:(store / name).read_bytes() for name in ('journal', 'boundary')}
                child = subprocess.run([str(worker), str(store), str(write(spec)), str(cli)], capture_output=True)
                assert child.returncode == 0, child.stderr.decode()
                observed = json.loads(child.stdout)
                assert child.stderr == b'' and observed['open_ns'] > 0
                assert len(observed['samples']) == 640
                assert {name:(store / name).read_bytes() for name in baseline} == baseline
                objects, history = independent(store)
                assert len(objects) == 2 * n and len(history) == n
                assert set(p.name for p in store.iterdir()) == {'lock', 'journal', 'boundary'}
                cells.append(dict(updates=n, repeat=repeat, spec=spec, observed=observed,
                                  journal_sha256=sha(baseline['journal']), journal_bytes=len(baseline['journal']),
                                  boundary_sha256=sha(baseline['boundary']), objects=len(objects), outcomes=len(history),
                                  worker_returncode=child.returncode, worker_stderr=child.stderr.decode()))
    sources = [HERE / 'check.py', HERE / 'PLAN.md', FRAMING / 'src/bin/owned-phase.rs',
               FRAMING / 'src/store.rs', FRAMING / 'src/journal.rs', FRAMING / 'src/lib.rs', ROOT / 'src/object.rs', FRAMING / 'Cargo.lock']
    result = dict(observed_date='2026-10-19', storage_source_commit='8bc0fc1578fb915f10fedd22ee016bf9c4e9b2df',
                  parent_source_commit='ae7e6c626586c1040e076d5efd92fcea3abbd068',
                  cli_sha256=sha(cli.read_bytes()), worker_sha256=sha(worker.read_bytes()),
                  rustc=subprocess.check_output(['rustc','--version'],text=True).strip(), python=platform.python_version(),
                  kernel=platform.release(), machine=platform.machine(), filesystem=filesystem, findmnt_fstype=fstype,
                  timer='std::time::Instant; API call including Result propagation and black_box, excluding argument cloning, checking and response serialization',
                  sources=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sources], cells=cells)
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: nine opens, 5760 API samples, nine held/released child lock controls, exact responses, unchanged bytes and independent histories')
    for n in (1,16,64):
        selected=[c for c in cells if c['updates']==n]
        print(n, 'updates open median ms', statistics.median(c['observed']['open_ns'] for c in selected)/1e6)
        for op in ('get','head','receipt','retry','duplicate_put'):
            times=[s['elapsed_ns'] for c in selected for s in c['observed']['samples'] if s['operation']==op]
            print(op, 'API median ns',statistics.median(times))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cli',type=pathlib.Path,required=True)
    p.add_argument('--worker',type=pathlib.Path,required=True)
    p.add_argument('--output',type=pathlib.Path,required=True)
    a=p.parse_args()
    main(a.cli,a.worker,a.output)
