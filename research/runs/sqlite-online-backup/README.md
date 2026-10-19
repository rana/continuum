# SQLite online backup and pinned-cut restore

## Research Delta

Question: does a supported consistent backup of the existing WAL-backed store retain exact objects, accepted heads and historical retries while a separate native writer commits during the copy? Owner: the desktop Codex coordinator, started by the 2026-10-19 06:56:31.904 UTC heartbeat. Input source: `4fc43550866a2794c1bdd492a4b1a79b0883faa4`. Before publication, reconciled `7a67fe3b184219a70083b9b538a8d3f1900a3583` and its separate owned-storage research decision. That contribution preserves this practical pilot's ownership; this unit does not implement or reserve its finite recovery-model work.

[run.py](run.py) is a disposable experiment using Python's SQLite Online Backup API and the existing native CLI, not a new backup command or persistent-store installation. The [final result](final/result.json) passed: seven exact objects, generation-2 head and three events/receipts were restored, including accepted and precondition-failed exact retries. A separate native writer advanced the live store to generation 3 between unfinished backup steps; that later operation and its two objects remained outside the pinned restore. Main-file-only copying retained the schema but lost all those WAL-held rows.

## Mechanism and expected outcomes

Official sources consulted 2026-10-19: [SQLite backup overview](https://sqlite.org/backup.html), [C API contract](https://sqlite.org/c3ref/backup_finish.html), and [Python Connection.backup](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup). They describe consistent online copying with incremental steps. The experiment additionally holds an explicit source read transaction and reads the logical inventory before backup; its actual unchanged cut is checked independently of a generic claim about concurrent backup restart behavior. No byte identity to a moving live file is expected.

The harness:

1. Initializes a fresh native store; holds an idle SQLite connection open before the native acceptance demo so the WAL survives between native processes.
2. Observes a 107,152-byte WAL. Copies only the main file as a deliberately inadequate control. Before native opening, immutable read-only inspection finds the correct application ID, version and schema but no object/head/event rows. Native opening then returns a null head. The review's hypothesis that opening might silently initialize a schema-less copy did **not** occur in this run.
3. Opens a separate read-only source connection, begins a read transaction and records the complete schema/objects/heads/events inventory. Backs up one page per step to a separate connection.
4. After the first unfinished step, a callback invokes distinct native processes to insert a late Blob/Snapshot and accept generation 3. Eight pages copy with monotonically decreasing remaining counts; no observed restart. This is controlled between-step interleaving, not a stress test or simultaneous writes inside one page-copy call.
5. Closes the destination, checks that its WAL is absent, and copies only that completed backup into a new restore directory. Checks pre-open byte identity with the completed backup; integrity and foreign-key checks pass. Schema, exact canonical rows, heads and receipts equal the pinned cut.
6. Uses native `get` to validate and compare all seven objects. Retries the initial accepted, later accepted and stale rejected requests: exact original receipts, all `replayed=true`. Changed-request operation-ID reuse is rejected even when its different candidate is absent. Retries/conflict leave the restored inventory unchanged.
7. Confirms that the late receipt and objects are absent. Retrying that later acknowledged operation against the restore fails specifically because its candidate is missing, and creates no receipt. Live state still has generation 3, nine objects and four events.

The last observation matters: restoring an old cut rolls back later acknowledged work. It must not be mistaken for resuming the newest live operation history. Reconciliation/restore policy belongs above this completed-copy experiment.

## Review, refinements and evidence

The exact [Claude request](claude-request.json) supplied the initial script and observed result. The [actual response](claude-response.json), `claude-opus-5-5`, medium effort, `end_turn`, no truncation, prompted stronger negative-control inspection, exact missing-object errors, backup/restore byte identity, monotonic page checks and late-operation retry observation. Schema retention was separately added before that reply; the final run includes it. `initial-pass/` preserves the reviewed execution; `observed/` preserves the intermediate schema/row-retention refinement; `final/` preserves the revised run. These are deliberate changed local checks, not retries of unknown external effects or three independent corroborations. Only one inference call was made.

[execution.json](execution.json) identifies the final command and script digest. Native [build provenance](build-provenance.json) identifies the retained default-feature binary reused from the CSV pilot. Python reported SQLite **3.46.1**; this is the backup connection library, not a claim about rusqlite's bundled version. The same exact native binary wrote and read the restored store, at schema version 1. The native SQLite runtime version was not queried, so no general cross-version compatibility claim follows.

Raw native stdout/stderr/exit codes, all request JSON inputs, SQL inventories and page progress remain in each run's projection. Transient database/WAL/SHM files stay outside Git. The cut inventory includes exact canonical object and request bytes as hex, plus original receipt JSON. The final source and all retained projections are identified in the artifact manifest.

Run a new experiment in a fresh directory:

```sh
python3 research/runs/sqlite-online-backup/run.py \
  --binary /absolute/path/to/continuum --output /absolute/path/to/new-run
```

Validate the archived observation without database execution:

```sh
python3 research/runs/sqlite-online-backup/verify_records.py
```

The archival verifier passed locally. Hosted CI executes both the archive check and a new disposable online-backup run with its hosted binary. No unchanged Rust suite was rerun locally; the hosted workflow retains its Rust and existing pilot gates.

## Limits and next action

This establishes completed-copy behavior on one local platform with one controlled writer, not crash-safe backup publication, arbitrary load, WAL-growth bounds, live in-place restore, schema upgrades, hostile mutation, physical power loss or an installed backup responsibility. Partial-output cleanup and source/restore fencing are deliberately outside this disposable harness. A callback deadline and per-child timeout bound this small run; they are not product resource guarantees.

Next practical unit: implement a narrow native same-schema backup export, using a consistent source cut and refusing destination overwrite, with staged publication and process-interruption tests before describing it as a usable backup. Keep in-place restore and migrations out of that first command. Reconcile remote ownership first; the separate owned-storage finite model remains a distinct research lane. No recipient has accepted this next unit.
