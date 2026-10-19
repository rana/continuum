# Version-2 pre-write quarantine

The disposable owned journal now persists an intent **before** journal mutation and refuses any surviving intent across process restart. This replaces the version-1 policy that could expose uncertain outcomes after fresh sync calls. The change addresses a program-level recovery boundary; it does not certify a filesystem/device against actual writeback failure.

Sources: journal/review at `ccd9c170138465186ceb005aed2a9f0aac71d28e`, [focused review and primary sources](../../runs/owned-journal-review-01/README.md), ADR 0002 and separately owned successor design in PR 112. Owner: this continuing Codex engineering session. Fresh main/instructions/open PRs were reconciled before this disjoint unit. No provider call, retained-store migration or device manipulation occurred.

## Current protocol and compatibility

Boundary metadata is now exactly 80 bytes with magic `CTJBD002`, the existing u64 length and image SHA-256, and a final SHA-256 over `continuum:boundary:v2` + NUL + preceding marker bytes. Framing, canonical v1 objects, request identities, event payloads and historical receipts are unchanged. Version-1 and version-2 raw stores reject each other's boundary metadata; there is no permissive fallback or in-place rewrite. An older writer therefore cannot bypass the new fence by simply ignoring its filename.

The [current journal contract](../framing/JOURNAL.md) specifies the write sequence. An exclusively created empty `WRITE-IN-PROGRESS` file is synced, then its directory entry is synced through a directory descriptor already held before mutation. Only then may journal bytes change. The descriptor stays open through marker rename, core publication and fence clearing, rather than being reopened separately for each metadata sync.

Journal data and pending marker are synced, the marker is renamed, and the directory is synced. Only after that **completed core commit** may the intent be removed; a second directory sync completes fence clearing before ordinary success/reply. The live handle stays poisoned on every error. Present intents are never automatically removed, repaired or overridden; they block reads, acceptance/retry, export and append before startup resynchronization. A prior backup or separately qualified forensic repair is needed to regain availability. No such repair API is implemented.

Initialization/restore keeps its separate RESTORING guard. It now syncs the lock file and retains the parent descriptor from before directory creation; the guarded directory and parent entry are synced before payload writes. The directory descriptor remains open throughout installation. Export similarly retains its parent descriptor across staging, link/unlink and final sync. These descriptor-lifetime changes reduce error-observation gaps; they are not a claim of complete kernel writeback qualification.

If the final **fence-clear** sync fails, the preceding data/marker/directory commit has already succeeded. Surviving absent intent can recover that already committed image; a reappearing intent refuses. This distinguishes cleanup uncertainty from an unresolved data/marker write. Lost-reply injection `after-commit` now occurs only after the complete fence-cleared boundary. `after-rename` now quarantines, deliberately changing version-1 availability behavior. New `after-intent` exits before payload writes.

Image-archive container version `CTJEX001` and exact journal bytes are unchanged. Explicit restore of a known earlier archive into a new directory installs version-2 metadata; it preserves original object IDs and receipts. This is isolated image transport, not an automatic in-place upgrade, general migration or a way to certify/repair a genuinely failed legacy store. Quarantined current stores cannot export through the normal API.

## Executed Research Delta — 2026-10-19

Linux/Rust 1.91.1/Python 3.14. [result.json](result.json) preserves exact binaries, operation-stage fsync traces, expected refusals and compatibility observations. It uses the original [libc fsync interposer](../recovery-sync/fail_sync.c), compiled in a temporary directory and loaded only into our own single-threaded CLI. The chosen call returns EIO without performing underlying fsync; other calls reach the real function. No kernel/device fault or persistence loss was induced.

The before binary is the version-1, canonical-guard/startup-barrier implementation at the source above. After injected post-rename directory EIO it still returns the original receipt following four successful startup barriers. That is the old observed behavior, not demonstrated physical data loss.

The after trace has four startup barriers followed by intent sync (5), intent-directory sync (6), journal sync (7), pending-marker sync (8), committed-marker directory sync (9), and fence-clear directory sync (10):

- **Five write-stage EIO cases (5–9)** preserve a write intent. Independent CLI processes for receipt, exact retry and export all refuse, make **zero** fsync attempts and leave every byte unchanged. Failures at 5/6 occur before journal mutation; this shows the explicit availability cost even when old content remains intact.
- **Fence-clear EIO (10)** returns an error/no reply, but the prior successful core commit is recoverable if the removed guard remains absent. Exact retry returns its original receipt after four startup barriers without byte changes.
- **Completed commit before lost reply** exits 76 after all ten successful calls. Four separately injected startup barrier errors prevent acknowledgement. With those barriers successful, exact retry returns sequence 1/generation 1 without appending bytes.
- **Compatibility controls** use a separately created, cleanly acknowledged version-1 store. In-place cross-version opens refuse without changing bytes. Explicit old-image export/new-directory restore creates `CTJBD002`, preserves original objects/receipt, and makes the old writer refuse that destination. This is not a failed-store recovery claim.

Five Rust tests (including 2,380 finite codec sequences), strict Clippy/formatting, five journal process exits, 265 copied-image integrity controls, seven selected native semantic traces, archive negative/positive controls and offline restoration of both actual-successor evidence archives pass with protocol 2. Historical validation files retain their original policy/build observations; current CI replaces the barrier-only runner with this stronger quarantine runner.

## Reproduce and practical limits

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/prewrite-fence/check.py --binary research/owned-authority/framing/target/debug/owned-store
```

Optional `--before PATH` compares a separately built `ccd9c17` binary and runs the cross-version controls. No historical executable is committed. CI exercises current quarantine, safe-boundary retry and startup failures without rebuilding the historical program.

The safety argument still assumes successful intent/file/directory synchronization is honored, trusted paths, cooperative ownership and atomic rename. Coherent rollback, malicious users, silent/cross-file storage corruption and actual filesystem/device writeback behavior remain unqualified. This fence does not make a later successful sync prove that old failed data was repaired; it refuses that route instead. Failure can indefinitely quarantine otherwise recoverable bytes. There is no automatic repair, compaction, GC, multi-host service or retained-data adoption.

Next: independent review of the version-2 boundary and its cleanup/availability cases, followed by a bounded operating-cost investigation. Keep real device fault testing isolated from the user's workstation and separate from synthetic control-flow evidence.
