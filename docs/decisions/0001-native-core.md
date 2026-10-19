# ADR 0001: a native core with interoperable edges

Status: accepted design direction for the research prototype  
Date: 2026-10-19 UTC  
Owner: project design coordination under the user's native-first direction

## Problem

A continuing investigation needs more durable structure than a branch name and chat transcript. Starting with a universal workflow engine would make it hard to distinguish essential invariants from speculative conveniences. Starting with a Git-dependent data model would constrain the native experiment before testing it.

## Decision

Build a small Rust library and CLI. Use mature SQLite transactions and SHA-256 through established crates. Give exact source bytes, snapshots, and declared evidence native identities. Record local acceptance transitions and retry receipts atomically.

Git remains the public development and distribution host for this implementation. Future Git import/export is an adapter. A native object may record its upstream Git commit and path without having two independently writable authoritative homes.

The initial binary object encoding is explicit, domain-separated, versioned, and independent of compiler memory layout. JSON is a human and tool-facing input projection. Future structured record codecs must declare their canonicalization; hashing arbitrary differently formatted JSON is not semantic equality.

## Alternatives

- **Git as permanent source authority:** the lowest adoption cost, supported as a future adapter. Rejected as the mandatory core because the user wants to test a native source/work model. Claude proposed this narrower default; the disagreement is preserved in the collaboration record.
- **New storage engine immediately:** provides control but adds unnecessary durability and recovery work before a workload justifies it.
- **Assembly throughout:** makes portability and development harder without measured evidence that instruction-level work is the limiting cost.
- **Database server from day one:** useful for some deployment patterns but not needed to test local transactions and continuation.
- **Universal AST or IR source authority:** useful for selected languages; unsuitable as a universal replacement for exact files, binary inputs, and existing language tooling.

## Consequences

SQLite is an implementation choice, not the wire format. Its standard WAL implementation serializes writers and expects same-host shared memory. Keep write transactions short; do not mount one writable WAL database across hosts. Source: [SQLite WAL documentation](https://www.sqlite.org/wal.html).

Rust is the preferred initial language because it supports native code, explicit resource ownership, and systems integration. It does not automatically deliver speed, eliminate all bugs, make dependencies memory-safe, or prove concurrency correctness. Bundled SQLite includes a native C dependency.

The first release makes no comparative throughput claim. Reopen this decision if measured metadata contention, storage layout, memory amplification, or portability costs dominate representative workloads.

