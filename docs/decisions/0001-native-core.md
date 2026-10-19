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

## Why Rust is useful for this experiment

The decision starts with the work the core must do: preserve exact identities, represent operation states explicitly, and recover the same local acceptance result after an interrupted acknowledgement. Rust lets us express parts of that contract as types while compiling the implementation to native machine code. The implementation uses a dedicated object-ID type, enums for states and outcomes, explicit fallible results, and a clearly owned storage connection. These checks help agents change the core coherently; they do not establish that an authored claim is true or prove a distributed protocol correct.

Rust's ownership rules are checked by the compiler rather than a tracing garbage collector. Its usual compiler backend is LLVM, with an established optimization pipeline. These properties support the choice, but they are not a measured performance result for Continuum. Sources: [ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html), [compiler code generation](https://rustc-dev-guide.rust-lang.org/backend/codegen.html).

The retained 20 local scenario tests exercise correctness and process-crash recovery in the test profile. The [first release workload](../../research/runs/release-baseline-2026-10-19/README.md) now records three repetitions of a small single-worker workload with raw operation timings and checked outcomes. It establishes no representative high-load or comparative language result. Further investigation candidates include transaction frequency, writer contention, object loading and hashing, allocation and copying, and repeated context rendering. These are profiling candidates, not diagnosed bottlenecks. At the workflow level, avoided repeated investigation and reliable continuation also belong in the performance objective.

Assembly remains available for a bounded, measured need. Rust supports inline assembly on supported targets, so a useful optimized kernel would not require rewriting the whole project. Before introducing one, require a representative CPU profile, an end-to-end improvement over an appropriate optimized baseline, and preserved object, error, and recovery semantics. Source: [Rust inline assembly reference](https://doc.rust-lang.org/reference/inline-assembly.html).

The longer-lived commitment is the documented data format and behavioral contract. SQLite, implementation language, and selected kernels can change behind those contracts when evidence justifies the change.

