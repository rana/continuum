# Embedded storage choices for Continuum

Status: researched comparison and proposed evaluation; no replacement engine has been executed, benchmarked, or adopted. Inspected 2026-10-19 UTC / 2026-10-18 America/Los_Angeles. The source audit used `3d15a37fa7faeb53dde9f7ad517c72d99b9b771b`. During review, PR 1 merged at `2e3a9ae26ef97af5bbeb22a874da343fab40eca1`; its checkpoint adapter and trial were incorporated, and the audited native source, dependencies, Rust tests, and measurement harness were unchanged.

PR 2's independent-example work at `6f2a11465bc610276495de636c85071e2424d1c9` was also reconciled before publication; those audited native paths remain unchanged. [CURRENT.md](../../CURRENT.md) retains the advancing project priority.

The [source audit and research provenance](../../research/runs/storage-survey-2026-10-19.json) retain local source identities, the bundled dependency observation, exact collaborator request identity, primary-source links, and execution limits.

## Recommendation

Keep SQLite as the operational baseline while learning from real use. Evaluate **redb** as the first focused Rust key-value alternative and **Turso Database** as the SQL-preserving alternative. They answer different questions. Add **Fjall** when sustained ingest, compression, or large values make its LSM design relevant. No measured Continuum result currently selects a speed or footprint winner.

The valuable commitment is our object and acceptance contract. A Rust storage implementation may reduce the database language boundary and offer a more direct API; it does not establish better recovery or throughput by itself. Select a concrete candidate/version/configuration and test the full contract before migration. The [native-core decision](../decisions/0001-native-core.md) remains in force.

## What the current storage contract actually needs

The authoritative implementation is [store.rs](../../src/store.rs), with [object](../../src/object.rs) and [context](../../src/context.rs) validation above it. SQLite currently holds three tables: immutable objects, current target heads, and immutable acceptance events. The core does not use SQL joins, JSON queries, text/vector search, or analytical SQL.

Acceptance begins an immediate transaction. It checks the retained operation identity and request bytes; an exact retry returns the historical result. Otherwise it validates the candidate, compares the expected root and generation, allocates a database-wide sequence, records either acceptance or a stale-precondition receipt, and conditionally changes the head. The receipt and head change commit together. An atomic write batch without isolated conditional reads is insufficient.

| Priority | Requirement | What a candidate must preserve |
|---|---|---|
| Essential | Exact bytes and object identity | Retain and validate the same canonical bytes and public IDs. |
| Essential | Atomic conditional acceptance | Couple the condition, root/generation, operation binding, receipt, and ordered event. |
| Essential | Historical retry | Same request recovers the original outcome even after later head changes; changed request with the same operation identity fails. |
| Essential | Durable rejected outcomes | Stale preconditions also receive retained, replayable receipts. |
| Essential | Integrity and type checks | Prevent invalid references, altered immutable content, duplicate operation identities, and invalid generations. SQL is one enforcement mechanism; centralized Rust logic is another. |
| Essential | Stated persistence boundary | A successful durable acknowledgement follows the configured persistence barrier; filesystem/device assumptions remain explicit. |
| Essential | Explicit process model | Distinguish independent local processes, threads sharing a handle, and remote clients. |
| Essential | Format recognition and errors | Refuse unsupported/unrelated stores and preserve distinct conflict, busy, I/O, corruption, and uncertain-outcome behavior. |
| Before retained use | Backup, restore, and upgrade | Demonstrate a consistent independent backup and recovery; an in-file savepoint is not a backup. |
| Measure | Resource and maintenance costs | Include startup, resident memory, disk growth, background work, commit/recovery latency, and build footprint. |
| Conditional | Search, compression, replication, async | Add when a real consumer benefits; these do not replace acceptance correctness. |

The implementation currently uses STRICT tables, compound keys, UNIQUE, CHECK, a foreign key, a secondary event index, UPSERT, and immutability triggers with RAISE(ABORT). There is no WITHOUT ROWID. Some reference and canonicalization checks already live in Rust. A KV implementation would move further enforcement and index maintenance into that same small trusted core.

## Candidate feature matrix

The entries below describe upstream documentation. Only the existing SQLite adapter has been exercised by Continuum. Moving `latest` and upstream `main` documents can describe different states from a released crate; freeze the exact candidate before an experiment.

| Feature | SQLite through rusqlite | redb | Fjall | Turso Database |
|---|---|---|---|---|
| Implementation and interface | C engine; Rust binding; relational SQL | Rust engine; typed ordered KV; copy-on-write B+trees | Rust engine; ordered KV; LSM trees | Rust engine; SQLite-compatible SQL |
| Atomic read/check/write across collections | Existing transaction implementation | Write transaction across tables | Use transactional database API, not plain write batch | SQL transactions; exact adapter untested |
| Writer concurrency | One writer, concurrent read snapshots in WAL | One active write transaction | Serialized or optimistic serializable mode | Immediate writer mode; separate MVCC concurrent mode |
| Separate processes opening one writable store | Established local WAL coordination | Multi-process feature remains experimental | Concurrent process opening prohibited | Multi-process WAL coordination experimental |
| Durability setting for our comparison | Current WAL + FULL | Immediate | Explicit SyncAll before durable acknowledgement | FULL documented; verify exact configuration |
| SQL constraints and indexes | Current schema enforces several invariants | Implement corresponding checks/indexes in Rust | Implement corresponding checks/indexes in Rust | Relevant SQL features documented; combinations need conformance tests |
| Independent backup | SQLite backup API available; not yet a Continuum command | Savepoints/compaction available; turnkey online backup not established in this review | Logical snapshot copy possible; efficient physical/incremental checkpoint backup still an open feature | VACUUM INTO documented; SQLite C backup API stubbed |
| Maintenance focus | WAL checkpointing, read lifetime, database growth | Retained versions/savepoints, compaction, recovery configuration | Memtables, journal, compression, background compaction | WAL/MVCC lifecycle and selected compatibility mode |
| Observed maturity | Current baseline and established SQLite ecosystem | Core stable; 4.4.0 released October 13, 2026; experimental features assessed separately | 3.1.12 released October 3, 2026; declared format migration policy | Upstream reports production users but remains pre-1.0 |
| Engine license | SQLite public domain; binding license separate | MIT OR Apache-2.0 | MIT OR Apache-2.0 | MIT |

Primary sources: [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite backup](https://www.sqlite.org/backup.html), [redb overview](https://github.com/cberner/redb), [redb changelog](https://github.com/cberner/redb/blob/master/CHANGELOG.md), [redb transactions](https://docs.rs/redb/latest/redb/struct.WriteTransaction.html), [redb durability](https://docs.rs/redb/latest/redb/enum.Durability.html), [Fjall released crate](https://docs.rs/crate/fjall/latest), [Fjall persistence](https://docs.rs/fjall/latest/fjall/enum.PersistMode.html), [Fjall backup issue](https://github.com/fjall-rs/fjall/issues/52), [Turso overview](https://github.com/tursodatabase/turso), [Turso compatibility](https://github.com/tursodatabase/turso/blob/main/COMPAT.md), and [Turso manual](https://github.com/tursodatabase/turso/blob/main/docs/manual.md).

### Two different Rust experiments

**redb asks whether a narrower transactional KV interface improves this core.** The conceptual collections are objects, heads, operation results, ordered events, and format/sequence metadata. Keep them in one atomic domain initially. Do not introduce independent blob storage while also changing the engine: that adds a separate object-before-head crash-consistency problem.

**Turso asks whether SQL continuity plus a new implementation provides value.** Test the actual schema and error behavior first. Documented STRICT, CHECK, triggers, UPSERT and relevant PRAGMAs make it a credible candidate; that is not proof that the precise combinations, process locks, or recovery paths match. Its limited WITHOUT ROWID behavior does not reject our current schema because we do not use that layout. The stubbed C backup API is a lifecycle consideration, not a failure in an existing Continuum backup path. Compare a supported preservation route such as VACUUM INTO on its own terms.

Turso's BEGIN CONCURRENT is documented as snapshot isolation with conflicts. Do not relabel it serializable or enable it as a transparent speed switch. First preserve the current immediate-transaction contract; any concurrency redesign needs a separate invariant analysis. Source: [transaction manual](https://github.com/tursodatabase/turso/blob/main/docs/manual.md).

### Native implementation and the complete dependency boundary

Removing SQLite's C implementation can be useful for code comprehension, shared tooling, cross-compilation, or a concrete target requirement. It does not automatically create a freestanding or entirely C-free program.

Current redb includes OS-locking dependencies and unstable feature flags; inspect the pinned [manifest](https://docs.rs/crate/redb/latest/source/Cargo.toml.orig). The reviewed Turso core 0.8.3 [manifest](https://docs.rs/crate/turso_core/latest/source/Cargo.toml) has auxiliary SIMD/crypto choices; its pure-rust-crypto feature forwards to Aegis's Rust implementation, while other configurations may compile native code. [Aegis documents that boundary](https://docs.rs/aegis/latest/aegis/). No all-Rust transitive configuration was built or audited here. Ordinary OS FFI is also different from embedding a large C database engine.

### Other useful comparators

| Option | Relevant role | Main distinction |
|---|---|---|
| [heed / LMDB](https://docs.rs/heed/latest/heed/) | Typed Rust access to a compact transactional KV design | Wraps LMDB C; SQL invariants move into Continuum. Its [environment API](https://docs.rs/heed/latest/heed/struct.Env.html) includes backup copying. |
| [RocksDB Rust binding](https://github.com/rust-rocksdb/rust-rocksdb) | A comparator for sustained writes and larger LSM workloads | Native C++ and compression dependencies; include build and maintenance cost. |
| [DuckDB](https://duckdb.org/why_duckdb) | Analysis of experiment histories and model/resource results | C++ analytical SQL engine; a potential companion workload rather than the first acceptance-store candidate. |
| [libSQL](https://github.com/tursodatabase/libsql) | SQLite-derived replication and remote access | Distinct from the Rust Turso rewrite; retaining the C SQLite lineage does not answer a C-engine-removal objective. |
| [sled](https://github.com/spacejam/sled) | Historically relevant Rust KV design | Current upstream warns of a rewrite and reliability/migration limits; not selected for this authoritative store. |

## Footprint and performance matrix we should measure

Source-package size, documentation size, a crate's name, and a generic vendor benchmark are not deployed Continuum measurements. No numeric comparative footprint is claimed here.

| Dimension | Matched measurement |
|---|---|
| Executable | Stripped release size with the same target/LTO/debug settings; include native objects and required shared libraries. |
| Build | Clean and incremental build time, peak build memory, toolchains and enabled dependency features. |
| Startup | Entire CLI process: open/validate/recover, one useful operation, close. |
| Working memory | Idle and peak resident memory, configured caches, retained values, and filesystem cache under stated conditions. |
| Background use | Threads, CPU, I/O, open files, and maintenance continuing after foreground work. |
| Durable work | Correct acceptances and stale receipts per second; p50/p95/p99 acknowledgement latency and error rate. |
| Read work | Object retrieval plus the canonical verification our caller actually needs. |
| Concurrency | One hot target versus disjoint targets; threads versus independently opened processes. |
| Stored size | Logical bytes versus physical database, WAL/journal, retained versions, and temporary maintenance space. |
| Recovery | Time to reopen and recover the exact prior receipt after an interrupted acknowledgement. |
| Lifecycle | Backup while active, restore verification, format refusal/upgrade, and recovery from disk-full/I/O failures. |

Match durability and batching. SQLite FULL, redb Immediate, and a Fjall sync covering every acknowledged operation are starting points, subject to platform assumptions. Group commit can amortize persistence while keeping acknowledgement after the covering barrier; returning success early is a different durability mode. Keep that distinction in both throughput and latency results.

The [existing baseline](../../research/runs/release-baseline-2026-10-19/README.md) measures small in-process calls with one connection, excluding startup/close and large-object/context-history behavior. Its 20 scenario tests include process-crash cases, not physical power-loss testing. A comparison needs workload-specific additions rather than treating those tests as proof of every engine guarantee.

## Source-level findings that may matter more than the engine

These are hypotheses to profile, not diagnosed bottlenecks:

1. Store opening reserves a writer while validating or initializing the format, including for CLI reads. A safe fast path must preserve initialization races and unsupported-store refusal; do not blindly replace it with a deferred transaction.
2. Exact acceptance retries and duplicate object puts also acquire a writer reservation before finding existing state.
3. Snapshot/reference validation loads and hashes referenced content inside write transactions. Many large files can extend that work far beyond the current tiny fixture.
4. Object IDs occupy text keys internally; compact internal keys could preserve public identities but require a store-format change.
5. Context selection can rerender repeatedly as history grows. Changing the database does not remove that CPU/allocation work.
6. All acceptance events share a sequence counter. A multi-writer engine does not eliminate that shared ordering requirement. Reconsider global versus per-target order only as an explicit contract redesign.

## Smallest useful evaluation

Use existing domain operations as a conformance interface: put/get, head, accept, historical receipt, and ordered event access. Keep object encoding, canonical validation, context projection and public outcomes shared. Add only the narrow storage adapter and deliberate error mapping needed for one candidate; no general backend framework is required first.

For a redb trial, evaluate the explicit process-ownership modes rather than hiding a service behind a KV benchmark. For a Turso trial, start with the exact current DDL and immediate transactions. Exercise successful and rejected paths, changed-operation reuse, rollback/retry, two competing connections, simultaneous CLI processes where supported, and reopen after interruption. For retained use, include consistent backup/restore before adoption. Then measure representative durable work with fixed resource limits and enough maintenance/recovery exposure to understand the result.

A one-owner service is a legitimate architectural option: include IPC, startup, lifecycle, and recovery in that comparison. Experimental direct multi-process access is another explicitly bounded option. Neither is silently equivalent to the current deployment. Slow model inference should remain outside storage transactions and long-lived database snapshots.

For larger future histories, distinguish authoritative receipts/artifacts from reconstructible search indexes or analytics. That may permit different maintenance and durability choices without weakening accepted work. Keep the initial experiment in one atomic store until this separation has a demonstrated consumer.

## Research Delta

- Question: which modern embedded Rust alternatives improve Continuum's actual work contract, functionality, footprint, or performance?
- Contribution: source audit, primary-source candidate matrix, explicit dependency/process/durability distinctions, and a reproducible evaluation design. No dependency or native code changed.
- Collaboration: [actual Claude exchange 8](../collaboration/2026-10-19-claude-08.md), exact supplied request and returned metadata, and [retained corrections](../collaboration/README.md#storage-review-corrections).
- Learned: the core's narrow use of SQL makes KV credible; direct process sharing and relocated invariants are consequential; a Rust engine can still include auxiliary native dependencies.
- Negative finding: available documentation and our SQLite-only baseline cannot establish a comparative winner. Advertised atomic batches, snapshot isolation, and durable acknowledgements must not be conflated.
- Current project continuation: preserve the merged [checkpoint pilot](../../research/runs/project-checkpoint-pilot-1/README.md), [independent example](../../research/runs/independent-csv-pilot/README.md), and the next unit selected in CURRENT.md. This assessment supplies a bounded storage experiment when that question is selected; it does not erase concurrent work or require another permission round for already-authorized R&D.
- Reopen adoption when a candidate preserves the contract and demonstrates a meaningful target, resource, operability, or performance benefit with acceptable migration cost. A throughput gain is one possible reason, not the only reason.
