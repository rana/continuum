#!/usr/bin/env python3
"""Version-2 write quarantine under synthetic errors at actual libc fsync calls."""
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
    result = dict(binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                  scope='single-threaded Linux fsync interposition, no kernel/device writeback or power-loss experiment',
                  protocol=2, quarantine_cases=[], safe_boundary_cases=[])
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        library = root / 'fail_sync.so'
        subprocess.run(['cc', '-shared', '-fPIC', '-O2', '-Wall', '-Wextra', '-Werror', '-o', str(library),
                        str(HERE.parent / 'recovery-sync/fail_sync.c'), '-ldl'], check=True, capture_output=True)
        invocation = 0
        def call(executable, target, command, *values, fail=None):
            nonlocal invocation
            invocation += 1
            audit = root / f'audit-{invocation}'
            environment = dict(os.environ)
            environment.update(LD_PRELOAD=str(library), CONTINUUM_SYNC_LOG=str(audit))
            environment.pop('CONTINUUM_SYNC_FAIL_AT', None)
            if fail is not None:
                environment['CONTINUUM_SYNC_FAIL_AT'] = str(fail)
            process = subprocess.run([str(executable), command, str(target), *map(str, values)], env=environment, capture_output=True)
            calls = []
            for line in audit.read_text().splitlines() if audit.exists() else []:
                index, returned, errno, path = line.split('\t', 3)
                path = pathlib.Path(path)
                role = 'directory' if path == target else 'parent' if path == target.parent else path.name
                calls.append(dict(index=int(index), returned=int(returned), errno=int(errno), resource=role))
            return process, calls
        def images(path):
            return {p.name: p.read_bytes() for p in path.iterdir()}
        def seed(executable, name):
            store, request_file = root / name, root / (name + '.json')
            initialized, _ = call(executable, store, 'init')
            assert initialized.returncode == 0, initialized.stderr
            def put(value):
                request_file.write_text(json.dumps(value))
                process, _ = call(executable, store, 'put', request_file)
                assert process.returncode == 0, process.stderr
                return json.loads(process.stdout)['id']
            blob = put(dict(type='blob', bytes=list(b'original fenced source\n')))
            snapshot = put(dict(type='snapshot', entries=[dict(path='source', blob=blob)]))
            request = dict(acceptor='local', target='main', operation_id='choose', expected=None, candidate=snapshot)
            request_file.write_text(json.dumps(request))
            receipt = dict(sequence=1, request=request, outcome='accepted', observed=None,
                           resulting=dict(root=snapshot, generation=1))
            return store, request_file, receipt
        if args.before:
            before = args.before.resolve()
            store, request_file, receipt = seed(before, 'before')
            failed, calls = call(before, store, 'accept', request_file, fail=7)
            assert failed.returncode != 0 and not failed.stdout and calls[-1]['errno'] == 5
            replay, retry_calls = call(before, store, 'accept', request_file)
            assert json.loads(replay.stdout) == dict(receipt=receipt, replayed=True)
            assert len(retry_calls) == 4
            result['before'] = dict(binary_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),
                                    uncertain_commit_calls=calls, retry_calls=retry_calls,
                                    no_persistent_quarantine=True)
            # Explicit old-image transport is supported; in-place opening isn't.
            store, request_file, receipt = seed(before, 'legacy-clean')
            acknowledged, _ = call(before, store, 'accept', request_file)
            assert json.loads(acknowledged.stdout) == dict(receipt=receipt, replayed=False)
            old_image = images(store)
            refused, _ = call(binary, store, 'receipt', 'local', 'choose')
            assert refused.returncode != 0 and images(store) == old_image
            archive, restored = root / 'legacy.export', root / 'legacy-restored'
            exported, _ = call(before, store, 'export', archive)
            assert exported.returncode == 0
            restored_result, _ = call(binary, restored, 'restore', archive)
            assert restored_result.returncode == 0
            assert (restored / 'boundary').read_bytes()[:8] == b'CTJBD002'
            replay, _ = call(binary, restored, 'accept', request_file)
            assert json.loads(replay.stdout) == dict(receipt=receipt, replayed=True)
            rejected_old_writer, _ = call(before, restored, 'receipt', 'local', 'choose')
            assert rejected_old_writer.returncode != 0
            result['explicit_archive_restore_preserves_v1_objects_and_receipt'] = True
            result['legacy_image_clean_acknowledged'] = True
            result['cross_version_inplace_opens_refused'] = True
        # Startup has four barriers. Persist intent (5,6), data (7), pending
        # boundary (8), committed boundary directory (9), fence removal (10).
        expected = ['WRITE-IN-PROGRESS', 'directory', 'journal', 'boundary.pending', 'directory']
        for fail_at, resource in zip(range(5, 10), expected):
            store, request_file, receipt = seed(binary, f'error-{fail_at}')
            original = images(store)
            failed, calls = call(binary, store, 'accept', request_file, fail=fail_at)
            assert failed.returncode != 0 and not failed.stdout
            assert calls[-1]['errno'] == 5 and calls[-1]['resource'] == resource
            assert (store / 'WRITE-IN-PROGRESS').exists()
            preserved = images(store)
            if fail_at <= 6:
                assert preserved['journal'] == original['journal'] and preserved['boundary'] == original['boundary']
            retries = []
            for command, values in [('receipt', ('local', 'choose')), ('accept', (request_file,)), ('export', (root / f'refused-{fail_at}.export',))]:
                refused, startup = call(binary, store, command, *values)
                assert refused.returncode != 0 and not refused.stdout and b'quarantined' in refused.stderr
                assert not startup and images(store) == preserved
                retries.append(command)
            result['quarantine_cases'].append(dict(fail_at=fail_at, calls=calls, refused_operations=retries,
                                                   no_repair_sync_attempted=True, bytes_preserved=True))
        # Fence-clear sync can fail only after core data+boundary publication
        # already succeeded; surviving clear state may safely recover the result.
        store, request_file, receipt = seed(binary, 'cleanup-error')
        failed, calls = call(binary, store, 'accept', request_file, fail=10)
        assert failed.returncode != 0 and not failed.stdout and calls[-1]['errno'] == 5
        assert not (store / 'WRITE-IN-PROGRESS').exists()
        preserved = images(store)
        replay, startup = call(binary, store, 'accept', request_file)
        assert json.loads(replay.stdout) == dict(receipt=receipt, replayed=True)
        assert images(store) == preserved and len(startup) == 4
        result['safe_boundary_cases'].append(dict(case='cleanup_error_after_successful_core_commit', calls=calls,
                                                  retry_calls=startup, exact_original_receipt=True))
        # Completed commit before lost reply remains usable. Startup failures
        # still cannot return a receipt, even though no quarantine is needed.
        store, request_file, receipt = seed(binary, 'lost-reply')
        exited, commit_calls = call(binary, store, 'accept', request_file, 'after-commit')
        assert exited.returncode == 76 and not exited.stdout and len(commit_calls) == 10
        preserved, startup_failures = images(store), []
        for fail_at in range(1, 5):
            refused, calls = call(binary, store, 'accept', request_file, fail=fail_at)
            assert refused.returncode != 0 and not refused.stdout and calls[-1]['errno'] == 5
            assert images(store) == preserved
            startup_failures.append(dict(fail_at=fail_at, calls=calls))
        replay, startup = call(binary, store, 'accept', request_file)
        assert json.loads(replay.stdout) == dict(receipt=receipt, replayed=True)
        assert [c['resource'] for c in startup] == ['journal', 'boundary', 'directory', 'parent']
        assert images(store) == preserved
        result['safe_boundary_cases'].append(dict(case='completed_commit_lost_reply', commit_calls=commit_calls,
                                                  startup_failures=startup_failures, retry_calls=startup,
                                                  exact_original_receipt=True))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
