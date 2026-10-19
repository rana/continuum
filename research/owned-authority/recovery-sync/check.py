#!/usr/bin/env python3
"""Linux libc-fsync interposition against our own disposable native CLI only."""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True, type=pathlib.Path)
    parser.add_argument('--before', type=pathlib.Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    result = dict(scope='single-threaded Linux libc interposition; not kernel EIO, power-loss or persistence reordering',
                  binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        library = root / 'fail_sync.so'
        compiled = subprocess.run(['cc', '-shared', '-fPIC', '-O2', '-Wall', '-Wextra', '-Werror', '-o', str(library), str(HERE / 'fail_sync.c'), '-ldl'], capture_output=True)
        assert compiled.returncode == 0, compiled.stderr
        invocation = 0
        def invoke(executable, store, command, *values, fail=None):
            nonlocal invocation
            invocation += 1
            audit = root / f'audit-{invocation}'
            environment = dict(os.environ)
            environment['LD_PRELOAD'] = str(library)
            environment['CONTINUUM_SYNC_LOG'] = str(audit)
            environment.pop('CONTINUUM_SYNC_FAIL_AT', None)
            if fail is not None:
                environment['CONTINUUM_SYNC_FAIL_AT'] = str(fail)
            process = subprocess.run([str(executable), command, str(store), *map(str, values)], env=environment, capture_output=True)
            calls = []
            for line in audit.read_text().splitlines() if audit.exists() else []:
                index, returned, errno, path = line.split('\t', 3)
                path = pathlib.Path(path)
                resource = 'directory' if path == store else 'parent' if path == store.parent else path.name
                calls.append(dict(index=int(index), returned=int(returned), errno=int(errno), resource=resource))
            return process, calls
        def images(path):
            return {f.name: f.read_bytes() for f in path.iterdir()}
        def fixture(executable, name, fail_at):
            store, request_file = root / name, root / (name + '.json')
            response, _ = invoke(executable, store, 'init')
            assert response.returncode == 0, response.stderr
            def put(value):
                request_file.write_text(json.dumps(value))
                response, _ = invoke(executable, store, 'put', request_file)
                assert response.returncode == 0, response.stderr
                return json.loads(response.stdout)['id']
            blob = put(dict(type='blob', bytes=list(b'uncertain source\n')))
            snapshot = put(dict(type='snapshot', entries=[dict(path='source', blob=blob)]))
            request = dict(acceptor='local', target='main', operation_id='uncertain', expected=None, candidate=snapshot)
            request_file.write_text(json.dumps(request))
            failed, calls = invoke(executable, store, 'accept', request_file, fail=fail_at)
            assert failed.returncode != 0 and failed.stdout == b'' and b'Input/output error' in failed.stderr
            assert calls[-1]['resource'] == 'directory' and calls[-1]['errno'] == 5
            expected = dict(receipt=dict(sequence=1, request=request, outcome='accepted', observed=None,
                                        resulting=dict(root=snapshot, generation=1)), replayed=True)
            return store, request_file, expected, calls
        if args.before:
            before = args.before.resolve()
            store, request_file, expected, failed_calls = fixture(before, 'before', 3)
            content = images(store)
            replay, calls = invoke(before, store, 'accept', request_file, fail=1)
            assert replay.returncode == 0 and json.loads(replay.stdout) == expected and not calls
            assert images(store) == content
            result['before'] = dict(binary_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),
                                    uncertain_commit_calls=failed_calls,
                                    retry_calls=calls, retry_acknowledged_without_new_barrier=True)
        store, request_file, expected, failed_calls = fixture(binary, 'after', 7)
        content = images(store)
        failures = []
        for index, resource in enumerate(('journal', 'boundary', 'directory', 'parent'), 1):
            refused, calls = invoke(binary, store, 'accept', request_file, fail=index)
            assert refused.returncode != 0 and refused.stdout == b'' and b'Input/output error' in refused.stderr
            assert len(calls) == index and calls[-1]['resource'] == resource and calls[-1]['errno'] == 5
            assert images(store) == content
            failures.append(dict(fail_at=index, refused_without_acknowledgement=True, calls=calls))
        replay, calls = invoke(binary, store, 'accept', request_file)
        assert replay.returncode == 0 and json.loads(replay.stdout) == expected
        assert [c['resource'] for c in calls] == ['journal', 'boundary', 'directory', 'parent']
        assert all(c['returned'] == 0 for c in calls) and images(store) == content
        result['after'] = dict(uncertain_commit_calls=failed_calls, startup_failures=failures,
                               retry_success_calls=calls, exact_historical_receipt=True,
                               journal_bytes_unchanged=True)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
