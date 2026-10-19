#!/usr/bin/env python3
"""Same-version no-overwrite export/restore and interrupted-publication controls."""
import hashlib
import json
import pathlib
import struct
import subprocess
import sys
import tempfile
from check_store import independent
from check_journal import files


def main():
    binary = pathlib.Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, input_file = root / 'source', root / 'input.json'
        def call(command, target, *args):
            return subprocess.run([str(binary), command, str(target), *map(str, args)], capture_output=True)
        assert call('init', source).returncode == 0
        def put(value):
            input_file.write_text(json.dumps(value))
            result = call('put', source, input_file)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)['id']
        blob = put(dict(type='blob', bytes=list(b'exact investigation source\n')))
        snapshot = put(dict(type='snapshot', entries=[dict(path='source', blob=blob)]))
        request = dict(acceptor='local', target='main', operation_id='first', expected=None, candidate=snapshot)
        def accept(value, target=source):
            input_file.write_text(json.dumps(value))
            result = call('accept', target, input_file)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)
        original = accept(request)
        stale = dict(request, operation_id='stale')
        rejected = accept(stale)
        advanced = dict(request, operation_id='advance', expected=original['receipt']['resulting'])
        moved = accept(advanced)
        assert moved['receipt']['sequence'] == 3
        before = files(source)
        archive = root / 'snapshot.export'
        assert call('export', source, archive).returncode == 0
        assert files(source) == before
        exported = archive.read_bytes()
        assert archive.stat().st_nlink == 1
        # Independent container decoder; frame/semantic validation on restore below.
        assert exported[:8] == b'CTJEX001'
        assert struct.unpack('<Q', exported[8:16])[0] == len(before['journal'])
        assert exported[16:-32] == before['journal']
        assert hashlib.sha256(b'continuum:export:v1\0' + exported[:-32]).digest() == exported[-32:]
        # Later source changes cannot change the published cut.
        accept(dict(request, operation_id='later', expected=moved['receipt']['resulting']))
        assert archive.read_bytes() == exported
        restored = root / 'restored'
        assert call('restore', restored, archive).returncode == 0
        restored_before = files(restored)
        assert restored_before['journal'] == before['journal']
        assert independent(restored) == independent_from_copy(root, before)
        for old, response in ((request, original), (stale, rejected), (advanced, moved)):
            assert accept(old, restored) == dict(response, replayed=True)
            assert files(restored) == restored_before
        assert json.loads(call('get', restored, blob).stdout) == dict(type='blob', bytes=list(b'exact investigation source\n'))
        assert call('restore', restored, archive).returncode != 0 and files(restored) == restored_before
        assert call('export', source, archive).returncode != 0 and archive.read_bytes() == exported
        print('PASS: exact committed image, source advances after cut, original accepted/stale receipts and objects survive fresh restore; existing export/restore destinations unchanged')
        # Independent exporters race for one name. Only one publication succeeds.
        raced = root / 'race.export'
        runners = [subprocess.Popen([str(binary), 'export', str(restored), str(raced)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = [(p.communicate(), p.returncode) for p in runners]
        # Store ownership can itself reject a competitor; either way no overwrite.
        assert sorted(code for _, code in results) == [0, 1]
        assert raced.read_bytes() == exported
        print('PASS: competing subprocess exporters yield one successful immutable destination')
        for fault, code, published in [('export-before-link', 83, False), ('export-after-link', 84, True), ('export-after-sync', 85, True)]:
            destination = root / (fault + '.export')
            result = call('export', restored, destination, fault)
            assert result.returncode == code and result.stdout == b''
            assert destination.exists() == published
            if published:
                assert destination.read_bytes() == exported
                assert destination.stat().st_nlink == (2 if fault == 'export-after-link' else 1)
                target = root / (fault + '-restore')
                assert call('restore', target, destination).returncode == 0
                assert (target / 'journal').read_bytes() == before['journal']
        for fault, code, readable in [('restore-before-ready', 81, False), ('restore-after-ready', 82, True)]:
            target = root / fault
            result = call('restore', target, archive, fault)
            assert result.returncode == code and result.stdout == b''
            image = files(target)
            assert (call('head', target, 'local', 'main').returncode == 0) == readable
            assert call('restore', target, archive).returncode != 0 and files(target) == image
        print('PASS: three export and two restore process exits; partial installation refuses, lost-reply ready restore recovers; artifacts preserved')
        corruptions = [b'', exported[:15], exported[:16], exported[:-1], exported + b'X']
        for index in (0, 8, 16, len(exported) - 1):
            data = bytearray(exported); data[index] ^= 1; corruptions.append(bytes(data))
        # Physically self-consistent archives with invalid semantic events.
        def sealed(payload):
            payloads = payload if isinstance(payload, (list, tuple)) else [payload]
            image, previous = b'', bytes(32)
            for ordinal, item in enumerate(payloads):
                frame = struct.pack('<8sIQ32s', b'CTJFR001', len(item), ordinal, previous) + item
                previous = hashlib.sha256(b'continuum:journal-frame:v1\0' + frame).digest()
                image += frame + previous
            container = b'CTJEX001' + struct.pack('<Q', len(image)) + image
            return container + hashlib.sha256(b'continuum:export:v1\0' + container).digest()
        corruptions.append(sealed(b'{}'))
        # Valid container and frame chain; ObjectV1 Snapshot names a Blob absent from replayed state.
        path = b'source'
        canonical = b'continuum.object\0' + struct.pack('>HBI', 1, 2, 1) + struct.pack('>I', len(path)) + path + bytes(32)
        corruptions.append(sealed(json.dumps(dict(record='ObjectV1', canonical=list(canonical)), separators=(',', ':')).encode()))
        for number, data in enumerate(corruptions):
            damaged, target = root / f'bad-{number}.export', root / f'bad-{number}-restore'
            damaged.write_bytes(data)
            rejected_archive = call('restore', target, damaged)
            assert rejected_archive.returncode != 0
            if number == len(corruptions) - 1:
                assert b'missing object or wrong kind' in rejected_archive.stderr, rejected_archive.stderr
            assert not target.exists() and damaged.read_bytes() == data
        print(f'PASS: {len(corruptions)} malformed archives rejected before target creation')
        # Coordinator follow-up: accepted same encoding with a real Blob before
        # the Snapshot distinguishes missing closure from a vacuous format failure.
        blob_body = b'closure control'
        blob_bytes = b'continuum.object\0' + struct.pack('>HBI', 1, 1, len(blob_body)) + blob_body
        snapshot_bytes = canonical[:-32] + hashlib.sha256(blob_bytes).digest()
        positive = root / 'closure-positive.export'
        positive.write_bytes(sealed([json.dumps(dict(record='ObjectV1', canonical=list(data)), separators=(',', ':')).encode()
                                     for data in (blob_bytes, snapshot_bytes)]))
        target = root / 'closure-positive'
        assert call('restore', target, positive).returncode == 0
        objects, history = independent(target)
        assert len(objects) == 2 and not history
        print('PASS: missing-Blob rejection reason verified; same encoding with preceding real Blob restores two objects')
    print('LIMIT: trusted local Unix paths, same schema, bounded images; process exits are not power loss; leftover staging aliases require explicit inspection; no migration or receiver acceptance')


def independent_from_copy(root, before):
    path = root / 'independent-original'
    path.mkdir()
    for name, value in before.items():
        (path / name).write_bytes(value)
    return independent(path)


if __name__ == '__main__':
    main()
