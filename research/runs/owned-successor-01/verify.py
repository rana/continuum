#!/usr/bin/env python3
"""Offline custody/reconstruction checks. Never invokes a provider or edits project files."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True, type=pathlib.Path)
    binary = parser.parse_args().binary.resolve()
    offer = json.loads((ROOT / 'offer.json').read_text())
    preflight = json.loads((ROOT / 'preflight.json').read_text())
    result = json.loads((ROOT / 'result.json').read_text())
    wrapper = json.loads((ROOT / 'provider-result.json').read_text())
    returned = wrapper['structuredContent']
    response = json.loads(returned['text'].removeprefix('```json\n').removesuffix('\n```'))
    assert response == json.loads((ROOT / 'response.json').read_text())
    assert returned['status'] == 'OK' and not returned['truncated'] and returned['stop_reason'] == 'end_turn'
    assert returned['usage'] == result['usage'] and result['provider_attempts'] == 1
    assert response['patch'].encode() == (ROOT / 'successor.patch').read_bytes()
    request_bytes = (ROOT / 'request.json').read_bytes()
    assert digest(request_bytes) == preflight['request_sha256']
    assert digest((ROOT / 'offered.export').read_bytes()) == preflight['archive_sha256']
    assert digest((ROOT / 'completed.export').read_bytes()) == result['completed_archive_sha256']
    ack = response['acknowledgement']
    assert ack['source_commit'] == offer['source_commit'] and ack['source_snapshot'] == offer['source_snapshot'] and ack['acceptance_sequence'] == 1
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        def call(command, store, *args):
            process = subprocess.run([str(binary), command, str(store), *map(str, args)], capture_output=True)
            assert process.returncode == 0, process.stderr
            return json.loads(process.stdout)
        offered, completed = base / 'offered', base / 'completed'
        call('restore', offered, ROOT / 'offered.export')
        call('restore', completed, ROOT / 'completed.export')
        assert call('receipt', offered, 'continuum', 'offer-source') == offer['acceptance']['receipt']
        assert bytes(call('get', offered, offer['request_blob'])['bytes']) == request_bytes
        context = json.loads(request_bytes)['context']
        original = call('get', offered, offer['source_snapshot'])
        original_code = next(entry['blob'] for entry in original['entries'] if entry['path'] == 'check_archive.py')
        original_code = bytes(call('get', offered, original_code)['bytes'])
        assert original_code.decode() in context
        assert call('receipt', completed, 'continuum', 'offer-source') == offer['acceptance']['receipt']
        assert call('receipt', completed, 'continuum', 'accept-checked-successor') == result['accepted']['receipt']
        final = call('get', completed, result['accepted']['receipt']['request']['candidate'])
        final_id = next(entry['blob'] for entry in final['entries'] if entry['path'] == 'check_archive.py')
        final_bytes = bytes(call('get', completed, final_id)['bytes'])
        assert digest(final_bytes) == result['final_source_sha256']
        scratch = base / 'patch-check'
        scratch.mkdir()
        (scratch / 'check_archive.py').write_bytes(original_code)
        for name in ('successor.patch', 'coordinator.patch'):
            subprocess.run(['git', 'apply', '--check', str(ROOT / name)], cwd=scratch, check=True, capture_output=True)
            subprocess.run(['git', 'apply', str(ROOT / name)], cwd=scratch, check=True, capture_output=True)
        assert (scratch / 'check_archive.py').read_bytes() == final_bytes
    print('PASS: exact request/exposure, actual complete response, separate patches, both native exports and original/historical receipts reconstruct offline; no inference performed')


if __name__ == '__main__':
    main()
