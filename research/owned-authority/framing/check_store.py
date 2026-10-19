#!/usr/bin/env python3
"""Owned semantic journal tests, independent byte reader and finite oracle bridge."""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
from check_journal import inspect, files

ORACLE = pathlib.Path(__file__).resolve().parent.parent / 'oracle'
sys.path.insert(0, str(ORACLE))
from oracle import Request, evaluate
spec = importlib.util.spec_from_file_location('finite_checks', ORACLE / 'check.py')
finite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finite)


def request_bytes(request):
    result = b'continuum.accept\0\0\x01'
    for name in ('acceptor', 'target', 'operation_id'):
        data = request[name].encode()
        result += struct.pack('>I', len(data)) + data
    expected = request['expected']
    result += b'\0' if expected is None else b'\x01' + bytes.fromhex(expected['root'][7:]) + struct.pack('>Q', expected['generation'])
    return result + bytes.fromhex(request['candidate'][7:])


def decode_object(data, objects):
    if data[:19] != b'continuum.object\0\0\x01':
        raise ValueError('object envelope')
    kind, cursor = data[19], 20
    def take(size):
        nonlocal cursor
        value = data[cursor:cursor + size]
        cursor += size
        if len(value) != size:
            raise ValueError('short object')
        return value
    def integer():
        return struct.unpack('>I', take(4))[0]
    def variable():
        return take(integer())
    def reference(expected):
        value = 'sha256:' + take(32).hex()
        if objects.get(value) != expected:
            raise ValueError('missing or wrong-kind object')
    if kind == 1:
        variable()
    elif kind == 2:
        paths = []
        count = integer()
        if count > 4096:
            raise ValueError('snapshot bound')
        for _ in range(count):
            path = variable().decode()
            if not path or '\\' in path or '\0' in path or len(path.encode()) > 4096 or any(p in ('', '.', '..') for p in path.split('/')):
                raise ValueError('path')
            paths.append(path)
            reference(1)
        if paths != sorted(set(paths), key=lambda p: p.encode()) or any(p.startswith(q + '/') for p in paths for q in paths):
            raise ValueError('path ordering/alias')
    elif kind == 3:
        reference(2)
        if take(1) not in (b'\0', b'\x01', b'\x02'):
            raise ValueError('evidence outcome')
        variable().decode()
        tag = take(1)
        if tag == b'\x01':
            reference(1)
        elif tag != b'\0':
            raise ValueError('evidence output')
    else:
        raise ValueError('object kind')
    if cursor != len(data):
        raise ValueError('trailing object bytes')
    return kind


def independent(path):
    objects, history = {}, ()
    for payload in inspect(path):
        event = json.loads(payload)
        if event['record'] == 'ObjectV1':
            canonical = bytes(event['canonical'])
            identity = 'sha256:' + hashlib.sha256(canonical).hexdigest()
            if identity in objects:
                raise ValueError('duplicate object event')
            objects[identity] = decode_object(canonical, objects)
        elif event['record'] == 'AcceptanceV1':
            receipt = event['receipt']
            request = receipt['request']
            if bytes(event['request_bytes']) != request_bytes(request) or objects.get(request['candidate']) != 2:
                raise ValueError('request identity/candidate')
            expected = request['expected']
            symbolic = Request(operation=request['operation_id'], candidate=request['candidate'],
                               expected=None if expected is None else (expected['root'], expected['generation']),
                               acceptor=request['acceptor'], target=request['target'])
            history, response = evaluate(history, symbolic)
            if response == 'conflict' or response[1]:
                raise ValueError('repeated evaluated identity')
            projected = dict(response[0], request=request)
            for key in ('observed', 'resulting'):
                head = projected[key]
                projected[key] = None if head is None else dict(root=head[0], generation=head[1])
            if receipt != projected:
                raise ValueError('historical receipt differs from oracle')
        else:
            raise ValueError('event version')
    return objects, history


def main():
    binary = pathlib.Path(sys.argv[1]).resolve()
    records = json.loads((ORACLE / 'result.json').read_text())
    traces = [[Request(**dict(r, expected=tuple(r['expected']) if r['expected'] else None))
               for r in witness['trace']] for witness in records['mutants'].values()]
    traces.append([Request(**dict(r, expected=tuple(r['expected']) if r['expected'] else None)) for r in records['aba_trace']])
    comparisons = sum(finite.sqlite_trace(binary, trace) for trace in traces)
    print(f'PASS: owned Rust journal matches finite oracle on {len(traces)} retained traces / {comparisons} acceptance invocations')
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        path, input_file = root / 'owned', root / 'input.json'
        def call(command, *args, target=path):
            return subprocess.run([str(binary), command, str(target), *map(str, args)], capture_output=True)
        assert call('init').returncode == 0
        def put(value):
            input_file.write_text(json.dumps(value))
            result = call('put', input_file)
            assert result.returncode == 0, result.stderr
            return json.loads(result.stdout)['id']
        snapshots, observations, sources = [], [], []
        for expression in ('value >= 0', 'value > 0'):
            source = f'def positive(value):\n    return {expression}\n'.encode()
            namespace = {}
            exec(compile(source, 'positive.py', 'exec'), namespace)
            actual = [namespace['positive'](n) for n in (-1, 0, 1)]
            outcome = 'pass' if actual == [False, False, True] else 'fail'
            output = put(dict(type='blob', bytes=list(json.dumps(dict(inputs=[-1, 0, 1], observed=actual, expected=[False, False, True])).encode())))
            blob = put(dict(type='blob', bytes=list(source)))
            snapshot = put(dict(type='snapshot', entries=[dict(path='positive.py', blob=blob)]))
            put(dict(type='evidence_record', candidate=snapshot, outcome=outcome,
                     provenance='Executed three declared inputs in this local Python check; caller-authored evidence', output=output))
            sources.append((blob, source))
            snapshots.append(snapshot)
            observations.append(outcome)
        assert observations == ['fail', 'pass']
        for identity, source in sources:
            assert json.loads(call('get', identity).stdout) == dict(type='blob', bytes=list(source))
        request = dict(acceptor='local', target='positive', operation_id='choose-B', expected=None, candidate=snapshots[1])
        input_file.write_text(json.dumps(request))
        lost = call('accept', input_file, 'after-commit')
        assert lost.returncode == 76 and lost.stdout == b''
        # Fresh process, only directory bytes: no prior native response supplied.
        receipt = call('receipt', 'local', 'choose-B')
        assert receipt.returncode == 0
        receipt = json.loads(receipt.stdout)
        assert receipt == dict(sequence=1, request=request, outcome='accepted', observed=None,
                               resulting=dict(root=snapshots[1], generation=1))
        before = files(path)
        retried = call('accept', input_file)
        assert json.loads(retried.stdout) == dict(receipt=receipt, replayed=True)
        assert files(path) == before
        # Move forward, then recover original historical acceptance and stale receipt.
        stale = dict(request, operation_id='stale-A', candidate=snapshots[0])
        input_file.write_text(json.dumps(stale))
        rejected = json.loads(call('accept', input_file).stdout)
        assert rejected['receipt']['sequence'] == 2 and rejected['receipt']['outcome'] == 'precondition_failed'
        move = dict(request, operation_id='advance', expected=receipt['resulting'], candidate=snapshots[0])
        input_file.write_text(json.dumps(move))
        moved = json.loads(call('accept', input_file).stdout)
        assert moved['receipt']['sequence'] == 3 and moved['receipt']['resulting']['generation'] == 2
        for old, original in ((request, receipt), (stale, rejected['receipt'])):
            input_file.write_text(json.dumps(old))
            before = files(path)
            assert json.loads(call('accept', input_file).stdout) == dict(receipt=original, replayed=True)
            assert files(path) == before
        input_file.write_text(json.dumps(dict(request, candidate=snapshots[0])))
        before = files(path)
        assert call('accept', input_file).returncode != 0 and files(path) == before
        objects, history = independent(path)
        assert len(objects) == 8 and len(history) == 3
        print('PASS: exact source for two approaches; actual negative/pass evidence; lost-reply acceptance recovered; accepted/stale retries survive later movement without new bytes')
        print(f'PASS: independent byte/semantic reader validated {len(objects)} canonical objects and {len(history)} complete evaluated outcomes')
        # Missing closure and wrong-kind acceptance fail without journal writes.
        for bad in (dict(type='snapshot', entries=[dict(path='lost', blob='sha256:' + '00' * 32)]),):
            input_file.write_text(json.dumps(bad))
            before = files(path)
            assert call('put', input_file).returncode != 0 and files(path) == before
        input_file.write_text(json.dumps(dict(request, operation_id='wrong-kind', candidate=sources[0][0])))
        before = files(path)
        assert call('accept', input_file).returncode != 0 and files(path) == before
        # A self-consistent physical journal with an invented semantic receipt
        # must still refuse; rehashing bytes is not authority to invent history.
        damaged = root / 'invented'
        shutil.copytree(path, damaged)
        from check import read_image
        payloads = read_image((damaged / 'journal').read_bytes())
        event = json.loads(payloads[-1]); event['receipt']['sequence'] = 99
        payloads[-1] = json.dumps(event, separators=(',', ':')).encode()
        image, previous = b'', bytes(32)
        for ordinal, payload in enumerate(payloads):
            frame = struct.pack('<8sIQ32s', b'CTJFR001', len(payload), ordinal, previous) + payload
            previous = hashlib.sha256(b'continuum:journal-frame:v1\0' + frame).digest()
            image += frame + previous
        marker = b'CTJBD001' + struct.pack('<Q', len(image)) + hashlib.sha256(image).digest()
        marker += hashlib.sha256(b'continuum:boundary:v1\0' + marker).digest()
        (damaged / 'journal').write_bytes(image); (damaged / 'boundary').write_bytes(marker)
        before = files(damaged)
        assert call('head', 'local', 'positive', target=damaged).returncode != 0 and files(damaged) == before
        try:
            independent(damaged)
        except ValueError:
            pass
        else:
            raise AssertionError('invented receipt accepted')
        print('PASS: missing closure and self-consistent but invented receipt refuse without mutation')
    print('LIMIT: selected semantic traces and local process exit; no retained-data adoption, export/restore, full power-loss model or receiver acceptance')


if __name__ == '__main__':
    main()
