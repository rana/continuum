#!/usr/bin/env python3
"""Fixed, single-worker fresh-process cost probe; no inference or upstream use."""
import argparse
import hashlib
import json
import os
import pathlib
import platform
import statistics
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FRAMING = HERE.parent / 'framing'
sys.path.insert(0, str(FRAMING))
from check_store import independent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(binary, output):
    binary = binary.resolve()
    # Do not inherit an interposer or fault selection into timing samples.
    env = dict(os.environ)
    for key in ('LD_PRELOAD', 'CONTINUUM_SYNC_FAIL_AT', 'CONTINUUM_SYNC_LOG'):
        env.pop(key, None)
    records, cells = [], []
    with tempfile.TemporaryDirectory(prefix='continuum-cli-cost-') as temporary:
        root = pathlib.Path(temporary)
        filesystem = subprocess.check_output(['stat', '-f', '-c', '%T', str(root)], text=True).strip()
        shim = root / 'fsync.so'
        subprocess.run(['cc', '-shared', '-fPIC', '-O2', '-o', str(shim),
                        str(HERE.parent / 'recovery-sync/fail_sync.c'), '-ldl'], check=True)
        for updates in (1, 16, 64):
            for repeat in range(3):
                store = root / f'store-{updates}-{repeat}'
                inputs = root / 'input.json'

                def call(command, *args, record=False, extra_env=None):
                    started = time.perf_counter_ns()
                    child = subprocess.run([str(binary), command, str(store), *map(str, args)],
                                           capture_output=True, env=env if extra_env is None else extra_env)
                    elapsed = time.perf_counter_ns() - started
                    assert child.returncode == 0, child.stderr.decode()
                    value = json.loads(child.stdout)
                    if record:
                        records.append(dict(updates=updates, repeat=repeat, operation=record,
                                            elapsed_ns=elapsed, stdout=child.stdout.decode(), stderr=child.stderr.decode(),
                                            returncode=child.returncode))
                    return value

                def write_input(value):
                    inputs.write_text(json.dumps(value))
                    return inputs

                def stable_bytes():
                    return {name: (store / name).read_bytes() for name in ('journal', 'boundary')}

                call('init')
                expected, first, first_receipt = None, None, None
                for stage in range(updates):
                    blob = dict(type='blob', bytes=[stage] * 128)
                    blob_id = call('put', write_input(blob))['id']
                    snapshot = dict(type='snapshot', entries=[dict(path='sample.bin', blob=blob_id)])
                    snapshot_id = call('put', write_input(snapshot))['id']
                    request = dict(acceptor='probe', target='source', operation_id=f'update-{stage}',
                                   expected=expected, candidate=snapshot_id)
                    result = call('accept', write_input(request))
                    assert result['replayed'] is False and result['receipt']['sequence'] == stage + 1
                    assert result['receipt']['outcome'] == 'accepted'
                    expected = dict(root=snapshot_id, generation=stage + 1)
                    assert result['receipt']['resulting'] == expected
                    if first is None:
                        first, first_receipt = request, result['receipt']
                latest_receipt = result['receipt']
                baseline = stable_bytes()
                cell = dict(updates=updates, repeat=repeat, objects=2 * updates,
                            accepted_outcomes=updates, journal_bytes=len(baseline['journal']),
                            source_blob_bytes=128 * updates,
                            journal_sha256=digest(baseline['journal']), boundary_sha256=digest(baseline['boundary']))

                def operations(instrument=False):
                    for operation, command, args, wanted in (
                        ('get', 'get', [blob_id], blob),
                        ('head', 'head', ['probe', 'source'], expected),
                        ('receipt', 'receipt', ['probe', f'update-{updates - 1}'], latest_receipt),
                        ('retry', 'accept', [write_input(first)], dict(receipt=first_receipt, replayed=True)),
                        ('duplicate_put', 'put', [None], dict(id=blob_id)),
                    ):
                        # Inputs are prepared before the timed child invocation.
                        if operation == 'retry':
                            args = [write_input(first)]
                        if operation == 'duplicate_put':
                            args = [write_input(blob)]
                        if instrument:
                            log = root / 'sync.log'
                            log.unlink(missing_ok=True)
                            with_shim = dict(env, LD_PRELOAD=str(shim), CONTINUUM_SYNC_LOG=str(log))
                            actual = call(command, *args, extra_env=with_shim)
                            calls = sync_roles(log, store, root)
                            assert calls == ['journal', 'boundary', 'store', 'parent'], calls
                            cell.setdefault('sync_observations', {})[operation] = calls
                        else:
                            actual = call(command, *args, record=operation)
                        assert actual == wanted, (operation, actual, wanted)
                        assert stable_bytes() == baseline

                for _ in range(8):
                    operations()
                stale = dict(acceptor='probe', target='source', operation_id='stale-timed',
                             expected=None, candidate=snapshot_id)
                actual = call('accept', write_input(stale), record='new_stale')
                assert actual == dict(receipt=dict(sequence=updates + 1, request=stale, outcome='precondition_failed',
                                                  observed=expected, resulting=expected), replayed=False)
                cell['journal_bytes_after_timed_stale'] = (store / 'journal').stat().st_size
                baseline = stable_bytes()
                operations(instrument=True)
                stale['operation_id'] = 'stale-instrumented'
                log = root / 'sync.log'
                log.unlink(missing_ok=True)
                with_shim = dict(env, LD_PRELOAD=str(shim), CONTINUUM_SYNC_LOG=str(log))
                actual = call('accept', write_input(stale), extra_env=with_shim)
                assert actual['receipt'] == dict(sequence=updates + 2, request=stale, outcome='precondition_failed',
                                                 observed=expected, resulting=expected)
                assert actual['replayed'] is False
                calls = sync_roles(log, store, root)
                assert calls == ['journal', 'boundary', 'store', 'parent', 'WRITE-IN-PROGRESS',
                                 'store', 'journal', 'boundary.pending', 'store', 'store'], calls
                cell['sync_observations']['new_stale'] = calls
                objects, history = independent(store)
                assert len(objects) == 2 * updates and len(history) == updates + 2
                assert set(p.name for p in store.iterdir()) == {'lock', 'journal', 'boundary'}
                cell['independent_final_objects'] = len(objects)
                cell['independent_final_outcomes'] = len(history)
                cells.append(cell)
    summaries = []
    for updates in (1, 16, 64):
        for operation in ('get', 'head', 'receipt', 'retry', 'duplicate_put', 'new_stale'):
            samples = [r['elapsed_ns'] for r in records if r['updates'] == updates and r['operation'] == operation]
            summaries.append(dict(updates=updates, operation=operation, samples=len(samples),
                                  median_ns=statistics.median(samples), min_ns=min(samples), max_ns=max(samples)))
    paths = [HERE / 'check.py', HERE / 'PLAN.md', HERE.parent / 'recovery-sync/fail_sync.c',
             FRAMING / 'Cargo.lock', ROOT / 'src/object.rs', *sorted((FRAMING / 'src').rglob('*.rs'))]
    result = dict(storage_source_commit='8bc0fc1578fb915f10fedd22ee016bf9c4e9b2df',
                  base_commit='ea197d7c37352dbe13585ecf0e2c7fa489a03fe2',
                  binary_sha256=digest(binary.read_bytes()), binary_bytes=binary.stat().st_size,
                  build_command='cargo build --release --locked --manifest-path research/owned-authority/framing/Cargo.toml',
                  rustc=subprocess.check_output(['rustc', '--version'], text=True).strip(),
                  python=platform.python_version(), kernel=platform.release(), system=platform.system(),
                  machine=platform.machine(), filesystem=filesystem, timer='time.perf_counter_ns',
                  timing_scope='Uninstrumented full subprocess including launch/capture/recovery/sync/output; input preparation excluded',
                  sources=[dict(path=str(p.relative_to(ROOT)), sha256=digest(p.read_bytes()), bytes=p.stat().st_size) for p in paths],
                  cells=cells, summaries=summaries, samples=records)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'PASS: {len(cells)} stores; {len(records)} retained uninstrumented samples; exact outputs, nonappend bytes, sync roles and independent semantic histories checked')
    for s in summaries:
        print(f"{s['updates']:2} updates {s['operation']:13} n={s['samples']:2} median={s['median_ns']/1e6:.3f} ms")


def sync_roles(log, store, parent):
    roles = []
    for line in log.read_text().splitlines():
        number, status, error, path = line.split('\t')
        assert int(number) == len(roles) + 1 and status == '0' and error == '0'
        p = pathlib.Path(path)
        roles.append('store' if p == store else 'parent' if p == parent else p.name)
    return roles


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    run(args.binary, args.output)
