#!/usr/bin/env python3
"""Deliberately fault a scratch oracle; verify failed receipt custody end to end."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--build-provenance', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    original = ROOT / 'research/runs/independent-csv-pilot/verify_requirement.py'
    before = hashlib.sha256(original.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as directory:
        scratch = Path(directory)
        driver = scratch / 'research/runs/source-bound-verification/capture.py'
        driver.parent.mkdir(parents=True)
        shutil.copyfile(Path(__file__).with_name('capture.py'), driver)
        prior = scratch / 'research/runs/independent-csv-pilot'
        prior.mkdir(parents=True)
        shutil.copytree(original.parent / 'completed-checkpoint', prior / 'completed-checkpoint')
        (prior / 'verify_requirement.py').write_text(
            'import subprocess, sys, tempfile\n'
            'def verify(script):\n'
            '    return subprocess.run([sys.executable, str(script), "/dev/null"], '
            'capture_output=True, text=True).returncode\n')
        capture = scratch / 'run'
        argv = [sys.executable, str(driver), '--binary', str(args.binary.resolve()),
                '--build-provenance', str(args.build_provenance.resolve()), '--output', str(capture)]
        run = subprocess.run(argv, capture_output=True)
        assert run.returncode != 0
        receipt_bytes = (capture / 'verification-receipt.json').read_bytes()
        receipt = json.loads(receipt_bytes)
        assert receipt['passed'] is False
        oracle = next(stage for stage in receipt['stages'] if stage['stage'] == 'oracle')
        assert oracle['returncode'] != 0 and oracle['result'] is None and oracle['children'] is None
        assert b'fixture outside retained worker directory' in base64.b64decode(oracle['stderr']['base64'])
        logs = [json.loads(line) for line in (capture / 'native-log.jsonl').read_text().splitlines()]
        identity = json.loads(logs[-1]['stdout'])['id']
        native = subprocess.run([str(args.binary.resolve()), 'get', str(capture / 'seed.db'), identity],
                                capture_output=True, check=True)
        restored = json.loads(native.stdout)
        assert bytes(restored['object']['bytes']) == receipt_bytes
        for name in ['verification-request.json', 'verification-receipt.json', 'oracle-raw-outcome.json']:
            with gzip.open(out / (name + '.gz'), 'wb') as stream:
                stream.write((capture / name).read_bytes())
        result = {'injection': 'Only a scratch oracle invokes an off-fixture path; original source unchanged.',
                  'driver_returncode': run.returncode, 'driver_stderr_utf8': run.stderr.decode('utf-8'),
                  'failed_receipt_native_id': identity, 'failed_receipt_restored_byte_for_byte': True,
                  'missing_worker_result_preserved_as_absent': True,
                  'oracle_traceback_preserved_in_receipt': True,
                  'no_success_checkpoint': not (capture / 'checkpoint/checkpoint.json').exists(),
                  'original_oracle_sha256_before': before,
                  'original_oracle_sha256_after': hashlib.sha256(original.read_bytes()).hexdigest()}
        assert result['original_oracle_sha256_before'] == result['original_oracle_sha256_after']
        (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
