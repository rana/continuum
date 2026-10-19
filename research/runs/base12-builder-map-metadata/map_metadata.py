"""Read the frozen builder's metadata format; no code or ELF execution.

This checks map structure only. A map contains no label names, instruction
bytes, ELF digest, publication status or proof of an actual invocation.
"""
from dataclasses import dataclass
import struct

HEADER_BYTES = RECORD_BYTES = 32
MAX_INSTRUCTIONS = 1024
MAX_LABELS = 128
MAX_ROWS = MAX_INSTRUCTIONS + MAX_LABELS
MAX_MAP_BYTES = HEADER_BYTES + RECORD_BYTES * MAX_ROWS
CODE_FILE_OFFSET = 4096


@dataclass(frozen=True)
class MapMetadata:
    version: int
    code_bytes: int
    rows: tuple[tuple[int, int, int, int], ...]


def decode_map(data: bytes) -> MapMetadata:
    """Decode all bounded little-endian fields or raise ValueError.

    Record fields are kind, physical source line, file offset, encoded length.
    Label rows have zero length and may share an address or occur at code end.
    """
    if not HEADER_BYTES <= len(data) <= MAX_MAP_BYTES:
        raise ValueError('map byte length outside frozen bounds')
    if data[:8] != b'B12MAP01':
        raise ValueError('unexpected magic')
    version, count, code_bytes = struct.unpack_from('<QQQ', data, 8)
    if version != 1:
        raise ValueError('unsupported version')
    if not 2 <= count <= MAX_ROWS:
        raise ValueError('row count outside frozen bounds')
    if not 1 <= code_bytes <= 10 * MAX_INSTRUCTIONS:
        raise ValueError('code length outside frozen bounds')
    if len(data) != HEADER_BYTES + RECORD_BYTES * count:
        raise ValueError('record count does not consume exact input')
    rows = tuple(struct.iter_unpack('<QQQQ', data[HEADER_BYTES:]))
    cursor, previous_line, instructions, labels = CODE_FILE_OFFSET, 0, 0, 0
    for kind, line, offset, length in rows:
        if line <= previous_line or offset != cursor:
            raise ValueError('source lines or file offsets out of sequence')
        if kind == 1 and 1 <= length <= 10:
            instructions += 1
            cursor += length
        elif kind == 2 and length == 0:
            labels += 1
        else:
            raise ValueError('invalid record kind or length')
        previous_line = line
    if rows[0][0] != 2 or not 1 <= labels <= MAX_LABELS:
        raise ValueError('label structure outside frozen bounds')
    if not 1 <= instructions <= MAX_INSTRUCTIONS:
        raise ValueError('instruction count outside frozen bounds')
    if cursor != CODE_FILE_OFFSET + code_bytes:
        raise ValueError('record spans disagree with code length')
    return MapMetadata(version, code_bytes, rows)
