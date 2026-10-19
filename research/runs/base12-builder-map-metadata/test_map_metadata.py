import struct
import unittest

from map_metadata import decode_map, MAX_MAP_BYTES


def packet(rows=((2, 1, 4096, 0), (1, 2, 4096, 1)), code_bytes=1):
    return (b'B12MAP01' + struct.pack('<QQQ', 1, len(rows), code_bytes)
            + b''.join(struct.pack('<QQQQ', *row) for row in rows))


class MapMetadataTests(unittest.TestCase):
    def test_complete_little_endian_fields(self):
        rows = ((2, 3, 4096, 0), (1, 257, 4096, 10))
        decoded = decode_map(packet(rows, 10))
        self.assertEqual((decoded.version, decoded.code_bytes, decoded.rows), (1, 10, rows))

    def test_shared_offsets_and_code_end_label(self):
        rows = ((2, 1, 4096, 0), (2, 4, 4096, 0),
                (1, 5, 4096, 1), (2, 6, 4097, 0))
        self.assertEqual(decode_map(packet(rows)).rows, rows)

    def test_exact_maximum_record_capacity(self):
        rows = tuple((2, i + 1, 4096, 0) for i in range(128))
        rows += tuple((1, i + 129, 4096 + i, 1) for i in range(1024))
        data = packet(rows, 1024)
        self.assertEqual(len(data), MAX_MAP_BYTES)
        self.assertEqual(len(decode_map(data).rows), 1152)

    def test_truncation_trailing_and_oversized_payloads(self):
        data = packet()
        for altered in (b'', data[:31], data[:-1], data + b'\0', b'\0' * (MAX_MAP_BYTES + 1)):
            with self.subTest(size=len(altered)), self.assertRaises(ValueError):
                decode_map(altered)

    def test_header_mutations(self):
        base = packet()
        alterations = [b'WRONGMAG' + base[8:]]
        for offset, value in ((8, 2), (16, 1), (16, 1153), (24, 0), (24, 10241)):
            data = bytearray(base)
            struct.pack_into('<Q', data, offset, value)
            alterations.append(bytes(data))
        # Big-endian header fields are not accepted as little-endian values.
        alterations.append(base[:8] + struct.pack('>QQQ', 1, 2, 1) + base[32:])
        for data in alterations:
            with self.subTest(header=data[:32]), self.assertRaises(ValueError):
                decode_map(data)

    def test_invalid_record_fields(self):
        for row in ((3, 2, 4096, 1), (1, 2, 4096, 0), (1, 2, 4096, 11),
                    (2, 2, 4096, 1), (1, 1, 4096, 1), (1, 2, 4097, 1)):
            with self.subTest(row=row), self.assertRaises(ValueError):
                decode_map(packet(((2, 1, 4096, 0), row)))

    def test_span_mismatch_and_missing_initial_label(self):
        for data in (packet(code_bytes=2), packet(((1, 1, 4096, 1), (2, 2, 4097, 0)))):
            with self.subTest(data=data), self.assertRaises(ValueError):
                decode_map(data)

    def test_individual_count_limits_below_map_maximum(self):
        too_many_labels = tuple((2, i + 1, 4096, 0) for i in range(129)) + ((1, 130, 4096, 1),)
        too_many_instructions = ((2, 1, 4096, 0),) + tuple((1, i + 2, 4096 + i, 1) for i in range(1025))
        for rows, code_bytes in ((too_many_labels, 1), (too_many_instructions, 1025)):
            with self.subTest(count=len(rows)), self.assertRaises(ValueError):
                decode_map(packet(rows, code_bytes))


if __name__ == '__main__':
    unittest.main()
