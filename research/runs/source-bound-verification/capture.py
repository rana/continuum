#!/usr/bin/env python3
"""Capture this CSV pilot's fixed checks; not an arbitrary-command/model runner."""
import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import sysconfig
import time
from unittest import mock
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[3]
PRIOR = ROOT / 'research/runs/independent-csv-pilot'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    return path


def bytes_record(data):
    return {'bytes': len(data), 'sha256': sha(data), 'base64': base64.b64encode(data).decode('ascii')}


def interpreter():
    binary = Path(sys.executable).resolve(strict=True)
    return {'executable': sys.executable, 'resolved_executable': str(binary),
            'binary_sha256': sha(binary.read_bytes()), 'version': sys.version,
            'platform': platform.platform()}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def module_origins():
    stdlib = Path(sysconfig.get_path('stdlib')).resolve()
    sites = {Path(sysconfig.get_path(name)).resolve() for name in ['purelib', 'platlib']}
    records = []
    for name, module in sorted(sys.modules.items()):
        location = getattr(module, '__file__', None)
        if not location:
            continue
        path = Path(location).resolve()
        if path.is_relative_to(stdlib) and not any(path.is_relative_to(site) for site in sites):
            continue
        if path.is_file():
            records.append({'module': name, 'path': str(path), 'sha256': sha(path.read_bytes())})
    return records


def optional_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        return {'capture_read_error': str(error)}


def worker(stage, subject, output):
    """Retain actual child inputs before each read, including overwritten inputs."""
    output.mkdir(parents=True, exist_ok=False)
    fixtures = output / 'temporary-inputs'
    fixtures.mkdir()
    calls = []
    temporary_count = 0
    real_run = subprocess.run

    @contextmanager
    def retained_directory(*args, **kwargs):
        nonlocal temporary_count
        path = fixtures / f'{temporary_count:04d}'
        temporary_count += 1
        path.mkdir()
        yield str(path)  # Retain instead of deleting the directory after a check.

    def captured_run(argv, *, capture_output, text, **kwargs):
        if not capture_output or text is not True or kwargs:
            raise ValueError('unexpected subprocess configuration in fixed CSV checks')
        requested = list(map(str, argv))
        if (len(requested) < 3 or Path(requested[1]).resolve() != subject / 'inspect_csv.py' or
                Path(requested[0]).name not in ('python3', Path(sys.executable).name)):
            raise ValueError('unexpected command in fixed CSV checks')
        source = Path(requested[2]).resolve(strict=True)
        if not source.is_relative_to(fixtures):
            raise ValueError('fixture outside retained worker directory')
        data = source.read_bytes()
        executed = [sys.executable, *requested[1:]]
        started = time.monotonic()
        result = real_run(executed, capture_output=True)  # Retain raw bytes, then decode for original checks.
        after = source.read_bytes()
        record = {'requested_argv': requested, 'executed_argv': executed,
                  'input_path': str(source), 'input': bytes_record(data),
                  'input_unchanged_after_child': after == data,
                  'stdout': bytes_record(result.stdout), 'stderr': bytes_record(result.stderr),
                  'returncode': result.returncode, 'elapsed_seconds': time.monotonic() - started}
        calls.append(record)
        write(output / 'children.json', calls)
        if after != data:
            raise ValueError('fixture changed during child execution')
        return subprocess.CompletedProcess(executed, result.returncode,
                                           result.stdout.decode('utf-8'), result.stderr.decode('utf-8'))

    module_path = subject / 'test_inspect_csv.py' if stage == 'tests' else PRIOR / 'verify_requirement.py'
    module = load_module(module_path, 'captured_csv_checks')
    metadata = {'stage': stage, 'interpreter': interpreter(),
                'check_module_sha256': sha(module_path.read_bytes()), 'check_module': str(module_path),
                'capture_driver_sha256': sha(Path(__file__).read_bytes()),
                'environment': {key: os.environ.get(key) for key in ['PYTHONUTF8', 'PYTHONDONTWRITEBYTECODE', 'LANG', 'LC_ALL']}}
    write(output / 'worker.json', metadata)
    with mock.patch.object(module.tempfile, 'TemporaryDirectory', retained_directory), \
            mock.patch.object(module.subprocess, 'run', captured_run):
        if stage == 'tests':
            result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
            success = result.wasSuccessful()
            count = result.testsRun
        else:
            success = module.verify(subject / 'inspect_csv.py') == 0
            count = len(calls)
    metadata['observed_nonstdlib_modules_after_checks'] = module_origins()
    write(output / 'worker.json', metadata)
    write(output / 'result.json', {'passed': success, 'checks': count, 'child_processes': len(calls)})
    return 0 if success else 1


def capture(args):
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runtime = output / 'runtime'
    runtime.mkdir()
    binary = runtime / args.binary.name
    binary.write_bytes(args.binary.resolve(strict=True).read_bytes())
    binary.chmod(0o700)
    build_bytes = args.build_provenance.read_bytes()
    if json.loads(build_bytes)['binary_sha256'] != sha(binary.read_bytes()):
        raise ValueError('native binary does not match build provenance')
    (output / 'build-provenance.json').write_bytes(build_bytes)
    database = output / 'seed.db'

    def cli(command, *values):
        argv = [str(binary), command, str(database), *map(str, values)]
        run = subprocess.run(argv, capture_output=True, text=True)
        with (output / 'native-log.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'argv': argv, 'returncode': run.returncode,
                                     'stdout': run.stdout, 'stderr': run.stderr}) + '\n')
        if run.returncode:
            raise RuntimeError(run.stderr)
        return json.loads(run.stdout)

    cli('init')
    subject = output / 'subject'
    subject.mkdir()
    manifest = json.loads((PRIOR / 'completed-checkpoint/checkpoint.json').read_text())
    entries = []
    for item in manifest['source']['files']:
        data = (PRIOR / 'completed-checkpoint/source' / item['path']).read_bytes()
        assert sha(data) == item['sha256']
        path = subject / item['path']
        path.write_bytes(data)
        identity = cli('blob', path)['id']
        assert identity == item['blob']
        entries.append({'path': item['path'], 'blob': identity})
    source_snapshot = cli('put', write(output / 'subject-snapshot.json', {'type': 'snapshot', 'entries': entries}))['id']
    assert source_snapshot == manifest['source']['snapshot']
    driver = Path(__file__).resolve()
    commands = [[sys.executable, str(driver), '--worker', stage, '--subject', str(subject),
                 '--worker-output', str(output / stage)] for stage in ['tests', 'oracle']]
    operation = 'csv-local-verification-' + uuid.uuid4().hex
    request = {'schema': 'continuum.csv_verification_request.v1', 'operation_id': operation,
               'source_snapshot': source_snapshot, 'source_files': manifest['source']['files'],
               'commands': commands, 'interpreter': interpreter(),
               'capture_driver': {'sha256': sha(driver.read_bytes()), 'utf8': driver.read_text()},
               'oracle_script': {'sha256': sha((PRIOR / 'verify_requirement.py').read_bytes()),
                                 'utf8': (PRIOR / 'verify_requirement.py').read_text()},
               'environment_overlay': {'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1'},
               'instrumentation': ['Retain TemporaryDirectory inputs instead of deleting them.',
                                   'Capture every fixed CSV subprocess as raw bytes and retain input before/after.',
                                   'Resolve requested python3 through the identified worker interpreter; record requested and executed argv.'],
               'limits': ['Trusted local observation, not authentication, sandboxing or proof of physical durability.',
                          'Source digests observed before/after; no hostile concurrent filesystem model.',
                          'Interpreter executable digest is not a complete OS/stdlib/environment image.']}
    request_path = write(output / 'verification-request.json', request)
    request_id = cli('blob', request_path)['id']  # Retain the actual request before dispatch.
    env = os.environ.copy()
    env.update(request['environment_overlay'])
    outcomes = []
    started_utc = datetime.now(timezone.utc).isoformat()
    for stage, argv in zip(['tests', 'oracle'], commands):
        started = time.monotonic()
        run = subprocess.run(argv, cwd=subject, env=env, capture_output=True)
        outcome = {'stage': stage, 'argv': argv, 'returncode': run.returncode,
                   'elapsed_seconds': time.monotonic() - started,
                   'stdout': bytes_record(run.stdout), 'stderr': bytes_record(run.stderr)}
        # Retain raw exit/output even if an exception prevented worker metadata.
        write(output / f'{stage}-raw-outcome.json', outcome)
        outcome.update({'worker': optional_json(output / stage / 'worker.json'),
                        'result': optional_json(output / stage / 'result.json'),
                        'children': optional_json(output / stage / 'children.json')})
        outcomes.append(outcome)
    unchanged = all(sha((subject / item['path']).read_bytes()) == item['sha256'] for item in manifest['source']['files'])
    receipt = {'schema': 'continuum.csv_verification_receipt.v1', 'operation_id': operation,
               'request': request_id, 'request_sha256': sha(request_path.read_bytes()),
               'source_snapshot': source_snapshot, 'started_utc': started_utc,
               'finished_utc': datetime.now(timezone.utc).isoformat(), 'stages': outcomes,
               'source_unchanged_after_checks': unchanged,
               'passed': unchanged and all(o['returncode'] == 0 and isinstance(o['result'], dict) and o['result'].get('passed') is True for o in outcomes),
               'scope': 'New local CSV observation under the explicit capture hooks; not an authenticated external receipt.'}
    receipt_path = write(output / 'verification-receipt.json', receipt)
    receipt_id = cli('blob', receipt_path)['id']
    if not receipt['passed']:
        raise RuntimeError('verification failed; request, receipt and diagnostics retained')
    bundle = json.loads(gzip.decompress((ROOT / 'research/runs/checkpoint-object-import/import-objects.json.gz').read_bytes()))
    bundle['objects'].extend([cli('get', request_id), cli('get', receipt_id)])
    bundle_path = write(output / 'import-objects.json', bundle)
    state = json.loads((ROOT / 'research/runs/checkpoint-object-import/authored-work-state.json').read_text())
    state['id'] = 'csv-source-bound-work'
    state['attempts'].append({'id': 'csv-local-verification', 'operation_id': operation,
                             'source_snapshot': source_snapshot,
                             'summary': 'New local observation: exact source, interpreter, every child input and raw output retained.',
                             'dispatch_state': 'receipt_recorded', 'request': request_id, 'receipt': receipt_id,
                             'outcome_note': 'Observed 11 tests and nine oracle cases under documented retention/capture hooks. This receipt is separate from the earlier model reply and does not authenticate a worker.'})
    state['decisions'].append({'id': 'known-count-correction', 'state': 'active',
                              'statement': 'The historical model reply incorrectly said six tests were added. The pilot already corrected this to seven added and eleven total; preserve the reply, do not investigate or rewrite it again.',
                              'basis_attempt_ids': ['csv-visible-turn', 'csv-local-verification'],
                              'reopen_when': 'A new source requirement changes the test inventory.'})
    state['objective']['statement'] = 'Use the completed CSV change and new source-bound local verification without repeating its implementation or known test-count correction.'
    state['objective']['done_when'] = 'The source-bound request, observation and checkpoint are retained with explicit limits.'
    state['handoff']['id'] = 'source-bound-inspection-offer'
    state['handoff']['scope'] = 'Inspect both the model and verification receipts. Reuse them within their recorded source/environment scope; this is an offer, not recipient acceptance.'
    state['handoff']['required_decision_ids'].append('known-count-correction')
    state_path = write(output / 'authored-work-state.json', state)
    repo = output / 'csv-source'
    subprocess.run(['git', 'clone', str(PRIOR / 'csv-source.bundle'), str(repo)], capture_output=True, check=True)
    argv = [sys.executable, str(ROOT / 'tools/project_checkpoint.py'), '--repository', str(repo),
            '--binary', str(binary), '--build-provenance', str(output / 'build-provenance.json'),
            '--work-state', str(state_path), '--import-objects', str(bundle_path),
            '--output', str(output / 'checkpoint'), '--max-bytes', '16384']
    run = subprocess.run(argv, capture_output=True, text=True)
    write(output / 'checkpoint-command.json', {'argv': argv, 'returncode': run.returncode,
                                              'stdout': run.stdout, 'stderr': run.stderr})
    if run.returncode:
        raise RuntimeError(run.stderr)
    checkpoint = json.loads((output / 'checkpoint/checkpoint.json').read_text())
    assert checkpoint['source']['snapshot'] == source_snapshot
    write(output / 'result.json', {'passed': True, 'source_snapshot': source_snapshot,
                                   'request': request_id, 'receipt': receipt_id,
                                   'context_pack': checkpoint['context_pack'],
                                   'tests': outcomes[0]['result'], 'oracle': outcomes[1]['result'],
                                   'retained_child_inputs': sum(len(o['children']) for o in outcomes),
                                   'scope': receipt['scope']})
    print((output / 'result.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', choices=['tests', 'oracle'])
    parser.add_argument('--subject', type=Path)
    parser.add_argument('--worker-output', type=Path)
    parser.add_argument('--binary', type=Path)
    parser.add_argument('--build-provenance', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker:
        if args.subject is None or args.worker_output is None:
            parser.error('worker needs subject and worker-output')
        return worker(args.worker, args.subject.resolve(strict=True), args.worker_output.resolve())
    if args.binary is None or args.build_provenance is None or args.output is None:
        parser.error('capture needs binary, build-provenance and output')
    capture(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
