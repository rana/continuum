#!/usr/bin/env python3
"""Disposable filesystem/process checks; no production data or provider calls."""
import fcntl
import hashlib
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
from check import read_image


def inspect(path):
    if (path / 'WRITE-IN-PROGRESS').exists():
        raise ValueError('quarantined write intent')
    if (path / 'boundary.pending').exists():
        raise ValueError('pending publication')
    marker = (path / 'boundary').read_bytes()
    if len(marker) != 80 or marker[:8] != b'CTJBD002':
        raise ValueError('boundary format')
    length, = struct.unpack_from('<Q', marker, 8)
    if length > 1048576:
        raise ValueError('bound')
    image = (path / 'journal').read_bytes()
    if len(image) != length or hashlib.sha256(image).digest() != marker[16:48]:
        raise ValueError('boundary image')
    if hashlib.sha256(b'continuum:boundary:v2\0' + marker[:48]).digest() != marker[48:]:
        raise ValueError('boundary checksum')
    return read_image(image)


def files(path):
    return {p.name: p.read_bytes() for p in path.iterdir()}


def main():
    binary = pathlib.Path(sys.argv[1]).resolve()
    counts = dict(clean_reopens=0, interrupted=0, corruption_refusals=0)
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        def call(command, path, *args):
            return subprocess.run([str(binary), command, str(path), *args], capture_output=True)
        def init(name):
            path = root / name
            assert call('journal-init', path).returncode == 0
            assert call('journal-append', path, 'none', 'source').returncode == 0
            assert inspect(path) == [b'source']
            assert call('journal-read', path).stdout == b'1 committed frames\n'
            counts['clean_reopens'] += 1
            return path
        def refuse(path):
            before = files(path)
            assert call('journal-read', path).returncode != 0
            assert call('journal-append', path, 'none', 'unsafe').returncode != 0
            try:
                inspect(path)
            except (ValueError, FileNotFoundError):
                pass
            else:
                raise AssertionError('independent reader accepted ambiguous image')
            assert before == files(path)
        healthy = init('healthy')
        # Cooperating independently started writers cannot bypass an owned lock.
        before = files(healthy)
        with (healthy / 'lock').open('r+b') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            assert call('journal-append', healthy, 'none', 'contender').returncode != 0
            assert files(healthy) == before
        assert call('journal-append', healthy, 'none', 'proposal').returncode == 0
        assert inspect(healthy) == [b'source', b'proposal']
        print('PASS: exclusive initialization, independent reopen and writer contention')
        for fault, code in [('after-intent', 78), ('after-data', 74), ('pending', 75), ('after-commit', 76), ('after-rename', 77)]:
            path = init(fault)
            result = call('journal-append', path, fault, 'proposal')
            assert result.returncode == code and result.stdout == b''
            if fault == 'after-commit':
                assert inspect(path) == [b'source', b'proposal']
                assert call('journal-read', path).stdout == b'2 committed frames\n'
            else:
                refuse(path)
            counts['interrupted'] += 1
        uncertain = init('uncertain')
        result = call('journal-append', uncertain, 'sync-error', 'proposal')
        assert result.returncode == 0 and b'reads and writes refused' in result.stdout
        refuse(uncertain)
        print('PASS: five process exits; only completed fence-cleared images recover; ambiguous tails/pending refuse; injected sync uncertainty poisons handle')
        # All destructive controls use copies, never the healthy original.
        original = files(healthy)
        def damaged(name, edit):
            path = root / name
            shutil.copytree(healthy, path)
            edit(path)
            refuse(path)
            counts['corruption_refusals'] += 1
        damaged('missing-boundary', lambda p: (p / 'boundary').unlink())
        damaged('missing-journal', lambda p: (p / 'journal').unlink())
        for index in range(80):
            def flip(p, index=index):
                data = bytearray((p / 'boundary').read_bytes())
                data[index] ^= 1
                (p / 'boundary').write_bytes(data)
            damaged(f'marker-{index}', flip)
        for cut in range(len(original['journal'])):
            damaged(f'cut-{cut}', lambda p, cut=cut: (p / 'journal').write_bytes(original['journal'][:cut]))
        # A valid older marker paired with a newer image is refused.
        damaged('old-marker', lambda p: (p / 'boundary').write_bytes(before['boundary']))
        assert files(healthy) == original
        print(f"PASS: {counts['corruption_refusals']} missing/corrupt/cut/old-boundary controls; refused images unchanged")
        # Explicit undetectable counterexample: wholesale coherent rollback.
        rollback = root / 'whole-rollback'
        shutil.copytree(healthy, rollback)
        for name, value in before.items():
            (rollback / name).write_bytes(value)
        assert inspect(rollback) == [b'source']
        assert call('journal-read', rollback).returncode == 0
        print('LIMIT: coherent rollback of journal plus matching older boundary is undetectable; fault model must exclude loss of successful synced history')
    print('COUNTS', counts)


if __name__ == '__main__':
    main()
