#!/usr/bin/env python3
"""Finite enumeration, retained minimal mutant witnesses and optional SQLite check."""
import argparse
from dataclasses import asdict
import hashlib
import itertools
import json
import pathlib
import subprocess
import tempfile
from machine import Machine
from oracle import Request, evaluate

MUTANTS = ('root_only', 'retry_uses_current', 'changed_request_ignored',
           'sequence_only_success', 'stale_not_retained', 'target_scoped_operation')


def compare(trace, mutant=None):
    history, machine = (), Machine(mutant)
    for index, request in enumerate(trace):
        history, expected = evaluate(history, request)
        actual = machine.apply(request)
        if actual != expected:
            return dict(step=index + 1, expected=expected, actual=actual)
    return None


def sqlite_trace(binary, trace):
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        db, input_file = root / 'store.sqlite', root / 'input.json'
        def call(command, *args):
            return subprocess.run([str(binary), command, str(db), *map(str, args)], capture_output=True)
        def put(value):
            input_file.write_text(json.dumps(value))
            result = call('put', input_file)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)['id']
        initialized = call('init')
        assert initialized.returncode == 0, initialized.stderr
        roots = {}
        for name in ('A', 'B'):
            blob = put(dict(type='blob', bytes=list(name.encode())))
            # Independently derive v1 object identities from the published wire format.
            envelope = b'continuum.object\0\0\x01'
            blob_expected = 'sha256:' + hashlib.sha256(envelope + b'\x01\0\0\0\x01' + name.encode()).hexdigest()
            assert blob == blob_expected
            roots[name] = put(dict(type='snapshot', entries=[dict(path='source', blob=blob)]))
            snapshot_bytes = envelope + b'\x02\0\0\0\x01\0\0\0\x06source' + bytes.fromhex(blob.split(':')[1])
            assert roots[name] == 'sha256:' + hashlib.sha256(snapshot_bytes).hexdigest()
        def head(value):
            return None if value is None else dict(root=roots[value[0]], generation=value[1])
        history = ()
        for request in trace:
            history, expected = evaluate(history, request)
            native_request = dict(acceptor=request.acceptor, target=request.target,
                                  operation_id=request.operation, candidate=roots[request.candidate],
                                  expected=head(request.expected))
            input_file.write_text(json.dumps(native_request))
            result = call('accept', input_file)
            if expected == 'conflict':
                assert result.returncode != 0 and b'operation' in result.stderr.lower(), result
                continue
            assert result.returncode == 0, result.stderr
            receipt, replayed = expected
            native_receipt = dict(receipt, request=native_request,
                                  observed=head(receipt['observed']), resulting=head(receipt['resulting']))
            assert json.loads(result.stdout) == dict(receipt=native_receipt, replayed=replayed)
            # Separately opened CLI lookup must return the original historical receipt.
            lookup = call('receipt', request.acceptor, request.operation)
            assert lookup.returncode == 0 and json.loads(lookup.stdout) == native_receipt
        return len(trace)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', type=pathlib.Path)
    args = parser.parse_args()
    # Finite alphabet: two valid roots, three operation IDs, absent/A1/B1
    # preconditions, plus changed target and acceptor controls. Breadth first;
    # no pruning, no state equivalence assumptions, all traces up to depth 4.
    alphabet = [Request(op, root, expected) for op, root, expected in itertools.product(
        ('x', 'y', 'z'), ('A', 'B'), (None, ('A', 1), ('B', 1)))]
    alphabet += [Request('x', 'A', target='other'), Request('x', 'A', acceptor='other')]
    witnesses, total, steps = {}, 0, 0
    for depth in range(1, 5):
        for trace in itertools.product(alphabet, repeat=depth):
            total += 1
            steps += depth
            assert compare(trace) is None, trace
            for mutant in MUTANTS:
                if mutant not in witnesses:
                    difference = compare(trace, mutant)
                    if difference:
                        witnesses[mutant] = dict(trace=[asdict(r) for r in trace], difference=difference)
    assert set(witnesses) == set(MUTANTS), set(MUTANTS) - witnesses.keys()
    # ABA requires a longer trace than the bounded alphabet provides: return to
    # root A at generation 3, then try an old A1 precondition under a fresh key.
    aba = [Request('a', 'A'), Request('b', 'B', ('A', 1)), Request('c', 'A', ('B', 2)),
           Request('d', 'B', ('A', 1)), Request('a', 'A'), Request('d', 'B', ('A', 1))]
    assert compare(aba) is None and compare(aba, 'root_only') is not None
    baseline = None
    if args.binary:
        binary = args.binary.resolve()
        traces = [[Request(**dict(r, expected=tuple(r['expected']) if r['expected'] else None))
                   for r in item['trace']] for item in witnesses.values()]
        traces.append(aba)
        baseline = dict(traces=len(traces), operations=sum(sqlite_trace(binary, t) for t in traces),
                        binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    print(json.dumps(dict(alphabet=len(alphabet), max_depth=4, traces=total,
                          transition_comparisons=steps, mutants=witnesses,
                          aba_trace=[asdict(r) for r in aba], sqlite=baseline), indent=2))


if __name__ == '__main__':
    main()
