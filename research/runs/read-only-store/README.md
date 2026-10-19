# Existing-only read-only Store and CLI

## Research Delta

Question: remove the demonstrated reader/writer opening conflict without weakening writable initialization, validation or snapshot consistency. Owner: the active desktop Codex coordinator, resumed by the 2026-10-19 07:26:01.984 UTC heartbeat. Input main: `cedade61fbc377519dce68829679c954399bc854`. The separate owned-storage finite-model lane remains unchanged.

Implemented `Store::open_existing_read_only` and routed exactly eight pure-read CLI commands through it. [Operation instructions](../../../docs/operations/read-only.md) define snapshot lifetime, lost-pin errors and WAL bookkeeping limits. Writable opening and all mutation/backup routes retain the existing initialization, WAL and FULL synchronization behavior. Native object encodings and database schema are unchanged.

The constructor uses `SQLITE_OPEN_READ_ONLY` without create, begins a deferred transaction and validates application/schema identity inside it. The handle keeps that snapshot; all public read entry points check that the transaction has not silently ended. Missing/empty/unsupported databases are rejected without initialization. Supported DELETE-journal exports can be read without journal conversion. Native object validation and context projection/reference checks are reused.

## Executed tests and comparison

**31 tests passed locally**: the prior 25 integration scenarios, five new read-only integration scenarios and one snapshot-loss guard unit test. Formatting, strict all-target/all-feature Clippy and the default-feature build also passed. [validation.json](validation.json) identifies commands, source hashes, compiler and native/probe binaries.

[tests/read_only.rs](../../../tests/read_only.rs) checks all eight CLI reads against exact baseline stdout while an independent `BEGIN IMMEDIATE` remains held. It audits `verify-handoff` as read-only: its implementation loads/checks the acknowledgement and pack and observes the head; only the separate acknowledgement command stores a new Blob. No speed threshold substitutes for held-transaction synchronization.

Other cases establish pinning during **open**, before the first public read; a later WAL commit remains invisible to that handle and becomes visible after reopening. A failed unsupported mutation leaves the original pin intact. Missing/empty/wrong-identity/future-version and corrupt native-object cases fail. A standalone DELETE-journal source retains exact main bytes and mtime with no WAL/SHM creation.

The Unix recovery-permission case copies a dead-process WAL into fresh directories without SHM. In a restricted directory it fails without a writable fallback; in a writable directory it creates bookkeeping and reads the committed generation 2. Main bytes remain unchanged. Local execution as uid 1000 enforced the denied-permission branch. The test explicitly reports that denial assertion as unavailable under privileged processes rather than claiming a permission test that root can bypass.

The [final probe](result.json) repeats the earlier controlled fixture with the new CLI. All three formerly blocked commands now complete successfully while the reservation remains held; held observations were about 0.0011–0.0019 seconds in this local debug-build run. Their stdout equals the earlier uncontended baseline byte for byte. The [historical baseline](../read-writer-reservation/result.json) retains its three roughly five-second locked failures. This establishes the controlled availability change, not a throughput/capacity or general production speedup. The characterization example's expectations now match the intended new behavior. [Pre-review outcomes](pre-review-result.json) remain separately retained.

## Actual review and corrections

The [Claude request](claude-request.json) supplied the initial constructor, route, audit summary and five passing tests. The [actual response](claude-response.json), `claude-opus-5-5`, low effort, `end_turn`, no truncation, identified a real missing boundary: SQLite can automatically roll back a transaction after certain statement errors. [SQLite's autocommit contract](https://sqlite.org/c3ref/get_autocommit.html), consulted 2026-10-19, confirms this possibility. The final implementation rejects reads when the read-only handle has returned to autocommit. The unit test forces `ROLLBACK` internally, commits newer state separately and checks all four public read entry points fail closed until reopening. This tests guard behavior, not an actual injected I/O or memory fault.

The review's conditional suggestion that a failed mutation might roll back the existing pin did not occur: rusqlite constructs its transaction guard only after BEGIN succeeds, and the integration test checks the old snapshot after the rejected mutation. Its claim that writer commits during a WAL read pin were untested was also too broad: that was already exercised by the snapshot integration test. Its broader warning about long-lived readers remains useful and is now explicit in the API and operating docs. Identity/version validation is not claimed to prove complete schema or physical integrity; damaged tables may fail at the actual read.

The review used 1,378 input / 1,804 output tokens. Exact requests/replies remain intact; model interpretation is separate from executed tests. No automatic retry or further inference was performed.

## Publication, limits and next action

Hosted CI retains all core/pilot checks, executes the new integration/unit tests, and runs the now-fast reservation probe plus its archived comparison. No timer, worker activation, migration, source-writer fence, authentication or power-loss guarantee is added. A library handle sees a pinned point in time; drop/reopen it for later observations. Backup still uses its original writable source opening path in this scoped change.

Next useful research unit: resume one bounded unread group from the existing Base12/Prime Radiant source-review ledgers after reconciling exact pinned source availability and current ownership. The practical backup/read fixes are complete; do not manufacture another CSV implementation or inference round. Keep private upstream bytes private, distinguish full semantic reading from inventory, and publish only original lessons and precise coverage. The owned-storage finite model remains a separate research lane. No recipient has accepted that next unit.
