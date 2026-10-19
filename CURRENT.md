# Current state

Last reconciled: 2026-10-19 UTC (2026-10-18 America/Los_Angeles).

## Selected direction

Continuum is a native work and evidence engine for continuing AI engineering. The first implementation is a small Rust core, with exact source custody and durable local acceptance receipts. Git is the intended public development host and a future interoperability edge; the core has no Git runtime dependency.

## Completed locally

- Both original DOCX briefs converted faithfully to Markdown, including their full historical appendices, five tables, and 37 source hyperlinks. Visible-text round trips match after whitespace normalization.
- Rust library and JSON CLI compiled on Rust 1.99.1.
- Exact-byte Blob, restricted source Snapshot, and untrusted EvidenceRecord objects.
- Domain-separated versioned SHA-256 object IDs.
- Local SQLite expected-root/generation acceptance, operation identity binding, durable retries, and receipt queries.
- Four agent-guided protocols: Progress Brief, Holographic Walk, Research Record, Bounded Research Loop.
- Versioned digest-pinned registry, protocol schemas and fixtures, and a proposed execution-metadata schema.
- Seven further actual Claude Opus 5.5 exchanges, with supplied-input custody, visible responses, metadata, adopted proposals, and retained corrections. The fourth uses only a generated context pack for a fresh continuation of this project; the fifth and sixth review unattended work and the Base12 continuity pattern; the seventh selects a real-use pilot. Private cross-project context in requests five and six is explicitly redacted from the public projections and retained privately. The original briefs also retain their historical exchanges.
- Exact WorkState records, bounded whole-record context selection, retained rendered packs, historical and current-anchor verification, and explicit handoff acknowledgement-reference checks.
- A reproducible context example using independently started CLI processes.
- One actual fresh Claude continuation from an 8,321-byte pack, with an exact model-authored acknowledgement whose references passed native verification.
- Current architecture, native-core decision, research experiment, and phased roadmap.
- A reproducible release-build workload covering nine core operation groups, with raw results from three separately started processes, 100 samples per group in each run, and identical deterministic semantic fingerprints.
- A [continuing work method and ready Codex prompt](docs/operations/continuation.md) for preserving research movement across Chat and implementation tasks through GitHub.

## Validation

The current Rust code passes formatting, strict Clippy, and 20 scenario tests: nine context cases, nine invariants, and two child-process recovery cases. Recovery was checked immediately before commit and after commit before acknowledgement. The coordinating agent independently reran these checks after the implementation was frozen.

The checks establish the specified local process-failure behavior. They do not establish physical power-loss durability, authenticated multi-user operation, semantic evidence truth, replication correctness, or comparative high-load performance.

The [first release baseline](research/runs/release-baseline-2026-10-19/README.md) is measured in this Chat task's Linux executor on an observed overlay filesystem, not on the user's workstation. It checks deterministic object, acceptance, retry, and context outcomes while retaining individual in-process timings. This is a small single-worker workload; no language, Git, Scion, cold-cache, or concurrent-capacity comparison is established. The new CI smoke invocation checks workload outcomes without a timing threshold.

The acceptance demo demonstrates one accepted competing candidate, one stale rejected candidate, and an exact retry returning its historical receipt after the current head moves. The context example preserves different declared dispatch states for the same source, and distinguishes an intact old pack from current accepted state. Acknowledgement checks establish reference consistency, not identity, understanding, or external execution.

See the historical [foundation verification](research/runs/foundation-verification.json), current [context verification](research/runs/context-verification.json), and [example result](research/runs/context-example.json) for commands and artifact identities.

## Repository review coverage

Base12's full pinned tree has 5,593 files / 180,332,790 bytes. The cumulative review acquired 539 exact file paths and completed semantic reading of 161 distinct blobs (1,226,434 bytes), with 46 additional byte-identical alias paths. It distinguishes full inventory, programmatic inspection, and actual semantic reading. The requested whole-repository reading is incomplete; the [extended ledger](docs/source-review/base12-coverage-extended.json) preserves the precise remaining scope.

Prime Radiant's live checkout was not discovered through available repository access. The current retained research kit was reviewed instead: 193 files / 8,984,055 uncompressed bytes, with complete archive identity verification. The latest checkpoint has 86 complete semantic readings, seven separate complete historical source diffs, and two separately classified generated-manifest checks. All eight retained dialogue captures, eight associated receipts, three prose reports, and all 159 source-inventory records were read. The [latest audit](docs/source-review/prime-audits.md) keeps the 98 remaining numerical, visual, and binary files explicit; authored annotations in numerical records are among the gaps.

The precise source scope and transferable findings live in [research lessons](docs/research-lessons.md). No upstream code was executed or imported into this public project.

## Publication status

The original project is published at [rana/continuum](https://github.com/rana/continuum), a public MIT repository. GitHub sign-in completed, and connected read/write operations created the repository and published all 95 prepared files. The first published project commit is `3439f61989d344ff89df1b0cad4ea7fd119918e7`.

All three local development snapshots were imported with identical Git tree identities. The GitHub API assigned new commit metadata and parent links, so the public commit IDs differ from the local research IDs. The [source-commit map](research/publication/source-commit-map.json) records the exact correspondence, including the source used by the fresh Claude continuation. Original local history remains in the recoverable archive and the local `local-research-history` branch. Historical context packs and transcripts retain their original capture-time claims.

The first [GitHub Actions run](https://github.com/rana/continuum/actions/runs/39199405358) completed successfully on that project commit: formatting, strict Clippy, all-feature tests, and the acceptance demo. This confirms those checks on GitHub's hosted runner; it adds no high-load or comparative performance evidence. No packaged release or remotely deployed service is claimed.

## Next useful unit

The first release workload and [first real-use checkpoint unit](research/runs/project-checkpoint-pilot-1/README.md) are complete locally. The [checkpoint adapter](docs/operations/project-checkpoint.md) captures committed regular Git source through the existing CLI, authored WorkState, context coverage and build provenance in a disposable store. Six Python integration tests cover exact capture/reconstruction and failure boundaries; the existing Rust gates and 20 scenarios passed in this executor. One actual Claude successor received a 3,140-byte pack plus two explicitly supplied source documents, completed a custody review, and prompted concrete path-alias and binary-replacement protections. This is a qualitative observation with extra source exposure, not a pack-only performance result. See the run record for exact source, visible reply, corrections, validation and limits.

The [independent CSV pilot](research/runs/independent-csv-pilot/README.md) is now complete locally. A real Claude successor received a 3,737-byte native pack, requested three exact source files, and returned the missing-token requirement implementation. Applied without edits, it passed 11 CLI tests, an independently authored nine-scenario acceptance oracle, and concrete sample checks. Both independent source revisions and actual exchanges are retained; fresh reconstruction from the source bundle reproduced the snapshot and pack identities. Build-digest rejection also caught an all-feature test build replacing the measured default binary; reuse of the retained runtime succeeded.

Next, implement and test minimal explicit object-closure import for an existing recorded attempt in a fresh project-checkpoint store. Both real-use pilots had to keep request/receipt history in exact sidecar evidence because the adapter cannot import those references. Preserve the small core and disposable-store boundary; no general model runner is selected. A future external worker has not accepted this follow-up. Stores remain disposable; no ongoing adoption study or store upgrade/backup contract is completed.

Controlled context-history scaling remains a follow-up when use identifies the need. Keep mandatory facts, byte budget, environment, omission coverage, and expected outcomes explicit. If the selected unit's execution capability is unavailable, advance the next bounded source-review group from the coverage ledgers instead of writing another unchanged status recap.

The [fresh-model trial](research/continuation-trial/README.md) is complete. The full upstream reading request and a controlled model-performance comparison remain open.

Before adding a remote executor or model runner, specify durable dispatch and uncertain-outcome reconciliation. Add resource measurements before a fleet scheduler.

## Continuation setup

The operating method, complete Codex handoff, orientation, workload, and raw observations were published in `8e400c1946838be4e601261ae35c3cc81750c042`. Its [GitHub CI run](https://github.com/rana/continuum/actions/runs/39204429362) passed, including the new workload smoke invocation.

The recurring **Advance Continuum** task was confirmed created and enabled at 2026-10-19 05:29:22 UTC. It requests hourly flexible scheduling in `America/Los_Angeles`, with a start anchor of 2026-10-18 22:45. The creation response provided no precise next-run timestamp and no completed run. The [setup observation](research/runs/continuation-setup-2026-10-19.json) preserves that distinction. Read actual task history before claiming unattended progress. That was the continuation responsibility observed at that historical setup; it does not establish exclusive current ownership.

GitHub read/write and the supplied-context Claude collaborator were verified in this session. No direct Dot dispatch or user-workstation Continuum worker was verified. A ready startup prompt is available in the operating document. Existing responsibilities for other projects are separate and were not changed.

The current local desktop chat has a confirmed active **Continue Continuum** heartbeat at a one-minute cadence, requested by the user. Its [configuration observation](research/runs/independent-csv-pilot/heartbeat-observation.json) is not evidence of a completed unattended run. The older cloud task's live status/cancellation is unavailable through this app; the local prompt requires remote and ownership reconciliation before overlapping work. Keep this computer and app running for local continuation. Native builds and disposable checkpoint runs were observed in the current desktop shell; no persistent worker installation is claimed.
