# CLI reads under a writer reservation

## Research Delta

Question: does the current native CLI read path unnecessarily compete for SQLite's writer reservation? Owner: the active desktop Codex coordinator, resumed by the 2026-10-19 07:19:31.983 UTC heartbeat. Input main: `5f4acabe58158c6f1bf95ae06fa2a537673373e6`. The [owned-storage decision](../../../docs/decisions/0002-owned-storage-research.md) had identified this open-time reservation as an investigation; the separate finite-model lane remains untouched. No competing PR was observed at selection or publication preparation.

One [controlled native probe](../../../examples/probe_reader_reservation.rs) found a concrete availability limit. A separate connection holds `BEGIN IMMEDIATE` without changing data. Native CLI `get`, `head` and `receipt` each wait about five seconds and fail with `database error: database is locked`, even though a same-build read-only SQLite connection successfully reads the committed head, complete receipt JSON and canonical-object byte length while that reservation remains held. All three CLI commands return their exact baseline stdout after rollback. No core implementation or read-only Store API was changed in this unit.

## Evidence and mechanism

[Exact outcomes](result.json) retain argv, return codes, raw stdout/stderr and per-invocation elapsed observations for baseline, held-reservation and released phases. The three held observations were 5.0115, 5.0113 and 5.0108 seconds. The read-only control's three SQL reads took about 0.00035 seconds. Baseline/released CLI invocations were about 0.0016–0.0023 seconds. These small single-run observations support the controlled lock distinction, not a throughput, capacity or production performance comparison. No timing threshold is asserted by the harness.

The probe and CLI use the same Rust dependency/build path and bundled SQLite **3.53.2**. This avoids conflating a Python SQLite version with the native engine. The read-only control uses `SQLITE_OPEN_READ_ONLY`; it directly compares the committed head/receipt and obtains the Blob's canonical-byte length. It does not bypass native validation and then claim equivalent full object validation. Both baseline and released native `get` perform the usual native object checks.

At the source baseline, `Store::open` in `src/store.rs:82–122` requests `TransactionBehavior::Immediate` before inspecting application/schema identity, even for an already valid database. `src/main.rs` calls that constructor for every command. The five-second busy timeout is set immediately before this gate. The observed lock behavior and source path are consistent with initialization/validation acquiring a writer reservation before the requested read can run. The held transaction makes no object, head or event changes and is explicitly rolled back. The original probe head and sole receipt remain unchanged.

[execution.json](execution.json) identifies the actual command, native/probe binary digests, compiler and source hashes. Transient database files remain outside Git. The example currently characterizes the baseline busy outcomes; an intentional read-path change must update its expected behavior while retaining this historical observation. CI compiles/lints it and verifies archived outcomes; it does not add a recurring 15-second lock wait to every build.

## Actual consultation and selected boundary

The [Claude request](claude-request.json) supplied the observed outcomes, exact opening sequence, command categories and missing implementation. The [actual response](claude-response.json) reported `claude-opus-5-5`, low effort, `end_turn`, no truncation; usage was 754 input / 1,050 output tokens. It supported a separate existing-only read-only opening route, keeping writer initialization and its WAL/FULL semantics unchanged. This is supplied-context design advice, not execution or independent empirical corroboration.

Adopt for the next bounded implementation:

- Route only the eight audited pure-read commands through a separate existing-only read-only Store path. Reuse native object/context validation. Keep init/demo, all mutations, prepare/acknowledge and backup on their existing paths initially.
- Validate application/schema identity without a writer reservation, and define one consistent read snapshot for the command's lifetime. A long-lived handle's snapshot will become old; document reopening for freshness rather than claiming current action authority.
- Test held-writer completion and identical outputs, invalid identities/versions and corrupted objects, no database creation or main-file modification, mixed-read snapshot consistency and unchanged writer behavior. Prefer held-transaction synchronization to a fragile speed threshold.
- Exercise WAL sidecar/read-permission failure behavior. Do not silently fall back to writable opening. Read-only SQLite may still need to access or initialize shared WAL bookkeeping, so distinguish no main-database mutation from a universal promise that no sidecar can ever appear. The review's blanket no-sidecar/mtime tests need that fixture-specific qualification, and concurrent writers can legitimately change file metadata.

No read-only API is implemented by this contribution. Actual `verify-handoff` code must be audited for writes before routing it. No authentication, network, source-format migration or alternative storage engine is selected. The current library opening behavior remains the baseline.

## Validation and next action

The probe executed once successfully after a local JSON-macro compilation correction. Formatting and strict all-target/all-feature Clippy passed. [Archived verification](verify_records.py) passed without database or inference execution. The unchanged Rust scenario suite was not repeated locally for this example/data-only unit; hosted CI retains it and the existing pilot checks.

Reproduce the baseline in a fresh output directory at this contribution's source:

```sh
cargo build --locked
cargo run --locked --example probe_reader_reservation -- \
  --binary target/debug/continuum --directory /absolute/path/to/new-probe
```

Next practical unit: implement and test that separate existing-only read-only Store/CLI path, preserving writer behavior and the baseline evidence above. Reconcile newer work and ownership before editing shared core code. No recipient has accepted this next unit; the independent owned-storage finite model is separate.
