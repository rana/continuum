#!/usr/bin/env python3
"""Independent byte reader plus disposable subprocess cross-checks; stdlib only."""
import hashlib
import pathlib
import struct
import subprocess
import sys
import tempfile


def read_image(image):
    # Deliberately parse through a cursor/struct rather than translate Rust slices.
    cursor, last, records = 0, bytes(32), []
    while cursor < len(image):
        start = cursor
        if len(image) - cursor < 84:
            raise ValueError('short frame')
        magic, size, ordinal, previous = struct.unpack_from('<8sIQ32s', image, cursor)
        if magic != b'CTJFR001' or size > 65536:
            raise ValueError('version/size')
        if ordinal != len(records) or previous != last:
            raise ValueError('order/chain')
        cursor += 52
        payload = image[cursor:cursor + size]
        cursor += size
        last = image[cursor:cursor + 32]
        cursor += 32
        expected = hashlib.sha256(b'continuum:journal-frame:v1\0' + image[start:cursor - 32]).digest()
        if len(payload) != size or last != expected:
            raise ValueError('payload/digest')
        records.append(payload)
    return records


def main():
    binary = pathlib.Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp) / 'journal'
        payloads = ['exact source', 'approach A failed', 'approach B proposed']
        exited = subprocess.run([str(binary), 'create-exit-before-reply', str(path), *payloads], capture_output=True)
        assert exited.returncode == 73 and exited.stdout == b''
        original = path.read_bytes()
        assert read_image(original) == [p.encode() for p in payloads]
        assert subprocess.run([str(binary), 'read', str(path)], capture_output=True).returncode == 0
        # Exclusive creation never overwrites an existing successful or ambiguous image.
        again = subprocess.run([str(binary), 'create', str(path), 'replacement'], capture_output=True)
        assert again.returncode != 0 and path.read_bytes() == original
        boundaries, offset = {0}, 0
        for p in payloads:
            offset += 84 + len(p.encode())
            boundaries.add(offset)
        refused_cuts = 0
        for cut in range(1, len(original)):
            try:
                read_image(original[:cut])
                assert cut in boundaries
            except ValueError:
                assert cut not in boundaries
                refused_cuts += 1
        for index in range(len(original)):
            corrupt = bytearray(original)
            corrupt[index] ^= 1
            try:
                read_image(corrupt)
            except ValueError:
                pass
            else:
                raise AssertionError(f'accepted byte flip {index}')
        # Each reader independently refuses the same actual damaged file, unchanged.
        damaged = bytearray(original)
        damaged[-1] ^= 1
        bad = pathlib.Path(temp) / 'damaged'
        bad.write_bytes(damaged)
        assert subprocess.run([str(binary), 'read', str(bad)], capture_output=True).returncode != 0
        assert bad.read_bytes() == damaged and path.read_bytes() == original
        print(f'PASS: process exit 73 after file sync; {len(payloads)} recovered frames; '
              f'{refused_cuts} partial-frame cuts refused; {len(original)} byte flips refused; '
              'exclusive-create and preserved-corruption controls passed')
        print('LIMIT: complete-frame suffix loss is undetectable; no acceptance receipts, '
              'commit selection, writer takeover, power-loss or directory-durability qualification')


if __name__ == '__main__':
    main()
