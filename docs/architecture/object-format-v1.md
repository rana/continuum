# Prototype object encoding, version 1

This document describes src/object.rs and src/store.rs. It is an experimental codec specification. The first implementation accepts only version 1. A later incompatible format must use a new version and explicit migration.

## Common envelope

All integers are unsigned big-endian integers. There is no native-ABI layout, padding, Unicode normalization, or platform byte order.

| Field | Bytes |
|---|---|
| Domain | 17 ASCII bytes: continuum.object followed by one NUL byte |
| Version | u16, value 1 |
| Kind | u8: 1 Blob, 2 Snapshot, 3 EvidenceRecord |
| Body | Fixed-order fields below |

The object ID is SHA-256 of the complete canonical envelope, rendered as sha256: followed by exactly 64 lowercase hexadecimal digits. Object references inside envelopes contain the raw 32-byte SHA-256 digest, not the display prefix.

A variable byte sequence is a u32 length followed by that exact number of bytes. The complete envelope is limited to 16 MiB. Reject unknown versions/kinds, invalid lengths, trailing bytes, and any encoding that differs from canonical re-encoding.

## Bodies

### Blob, kind 1

One variable byte sequence. All byte values are allowed.

### Snapshot, kind 2

A u32 entry count followed by each entry's variable UTF-8 path and raw 32-byte Blob ID. At most 4096 entries; paths have at most 4096 UTF-8 bytes and sort by their UTF-8 byte sequence.

Paths must be nonempty, relative, slash-separated, and contain no backslash or NUL. Empty, dot, and dot-dot segments are rejected. Duplicate paths and a file path that is also a directory prefix are rejected. Sorting is part of canonicalization; Unicode normalization is not performed.

The store requires every referenced object to exist and be a Blob. A decoded canonical snapshot must already have canonical ordering. This v1 file model has no executable bit, symlink, arbitrary non-UTF-8 filename, or submodule semantics.

### EvidenceRecord, kind 3

1. Raw candidate Snapshot ID.
2. Outcome u8: 0 unknown, 1 pass, 2 fail.
3. Variable UTF-8 provenance string.
4. Optional-output tag: 0 absent; 1 followed by a raw output Blob ID.

The store checks reference existence and kinds. It does not verify the provenance, run a test, or establish that pass/fail is true. Acceptance currently accepts a Snapshot, independently of this evidence record.

## Conformance vector

A Blob containing the six bytes hello followed by LF has this envelope in hexadecimal:

```text
636f6e74696e75756d2e6f626a656374000001010000000668656c6c6f0a
```

Expected ID:

```text
sha256:7f20ef2d93ca7c8efeccaea5ff2e66aad6bf88d8355e390d3a543e011c7e9838
```

The test compares this to a digest calculated independently with Python hashlib. The test also checks decoding, truncation, trailing data, future versions, and snapshot ordering.

## Acceptance request encoding

The durable deduplication request is domain-separated as the ASCII bytes continuum.accept, NUL, then u16 version 1. It encodes the variable UTF-8 acceptor, target, and operation ID in that order; an optional expected-head tag; and the raw candidate Snapshot ID.

Expected head is tag 0 for no existing head, or tag 1 followed by root ID and u64 generation. Generation is in 1 through the maximum signed 64-bit integer. Names contain 1–256 UTF-8 bytes, must not be all whitespace, and contain no control characters.

Operation identity is scoped by acceptor. The target is bound into the full request. An existing identical request returns its original receipt; a different request under that identity is rejected.

## Database and receipts

SQLite application_id is 0x434f4e54 and user_version is 1. Object and event updates/deletions are rejected by triggers under the ordinary schema. These are local data invariants, not protection against an administrator who can modify the database itself.

Each acceptance outcome receives a local event sequence. The target generation advances only on acceptance; rejected stale candidates also have durable operation receipts. Receipt JSON is a version-1 database representation, not yet a signed portable event format.

WAL with synchronous FULL is configured. The tests terminate child processes before commit and after commit before reply. They do not simulate a power failure, compromised storage, or a dishonest filesystem.

## Known engineering limits

Object and reference validation can hold a writer transaction, especially for many distinct large blobs. Repeated references to the same blob are deduplicated during validation. There is no streaming object transfer, garbage collection, multi-host protocol, receipt signature, authenticated API, or full repository checkout. These boundaries are deliberate and visible.

