# Current state

Last reconciled: 2026-10-19 UTC (2026-10-19 America/Los_Angeles).

## Selected direction

Continuum is a native work and evidence engine for continuing AI engineering. The first implementation is a small Rust core, with exact source custody and durable local acceptance receipts. Git is the intended public development host and a future interoperability edge; the core has no Git runtime dependency.

The [owned-storage research decision](docs/decisions/0002-owned-storage-research.md) now opens a separate purpose-built kernel and independent emitted-verifier investigation. Its first unit is a finite transition/recovery model. No custom engine, model execution, native-emitter target, migration or successor repository is claimed; the current practical pilot below keeps its existing ownership.

## Completed locally

- Both original DOCX briefs converted faithfully to Markdown, including their full historical appendices, five tables, and 37 source hyperlinks. Visible-text round trips match after whitespace normalization.
- Rust library and JSON CLI compiled on Rust 1.99.1.
- Exact-byte Blob, restricted source Snapshot, and untrusted EvidenceRecord objects.
- Domain-separated versioned SHA-256 object IDs.
- Local SQLite expected-root/generation acceptance, operation identity binding, durable retries, and receipt queries.
- Four agent-guided protocols: Progress Brief, Holographic Walk, Research Record, Bounded Research Loop.
- Versioned digest-pinned registry, protocol schemas and fixtures, and a proposed execution-metadata schema.
- Thirteen numbered further actual Claude Opus 5.5 exchanges, with supplied-input custody, visible responses, metadata, adopted proposals, and retained corrections. The fourth uses only a generated context pack for a fresh continuation of this project; the fifth and sixth review unattended work and the Base12 continuity pattern; the seventh selects a real-use pilot; the eighth reviews embedded storage alternatives; exchanges nine through eleven develop and correct the owned-storage research design; the twelfth considers a conditional successor repository; the thirteenth examines naming, worker transition and shared components. The project pilots also retain their own actual successor exchanges. Private cross-project context in requests five and six is explicitly redacted from the public projections and retained privately. The original briefs also retain their historical exchanges.
- Exact WorkState records, bounded whole-record context selection, retained rendered packs, historical and current-anchor verification, and explicit handoff acknowledgement-reference checks.
- A reproducible context example using independently started CLI processes.
- One actual fresh Claude continuation from an 8,321-byte pack, with an exact model-authored acknowledgement whose references passed native verification.
- Current architecture, native-core decision, research experiment, and phased roadmap.
- A reproducible release-build workload covering nine core operation groups, with raw results from three separately started processes, 100 samples per group in each run, and identical deterministic semantic fingerprints.
- A [continuing work method and ready Codex prompt](docs/operations/continuation.md) for preserving research movement across Chat and implementation tasks through GitHub.
- A [storage feature matrix and evaluation design](docs/experiments/embedded-storage-evaluation.md), grounded in the actual schema and current redb, Fjall, and Turso documentation. SQLite remains the baseline; no alternative-engine execution, performance comparison, or dependency migration is claimed.

## Validation

The current Rust code passes formatting, strict Clippy, and 31 tests: 30 integration scenarios (nine context, nine invariants, two acceptance recovery, five native backup and five read-only cases) plus a snapshot-loss guard unit test. Recovery was checked immediately before commit and after commit before acknowledgement. The coordinating agent independently reran these checks after the implementation was frozen.

The checks establish the specified local process-failure behavior. They do not establish physical power-loss durability, authenticated multi-user operation, semantic evidence truth, replication correctness, or comparative high-load performance.

The [first release baseline](research/runs/release-baseline-2026-10-19/README.md) is measured in this Chat task's Linux executor on an observed overlay filesystem, not on the user's workstation. It checks deterministic object, acceptance, retry, and context outcomes while retaining individual in-process timings. This is a small single-worker workload; no language, Git, Scion, cold-cache, or concurrent-capacity comparison is established. The new CI smoke invocation checks workload outcomes without a timing threshold.

The acceptance demo demonstrates one accepted competing candidate, one stale rejected candidate, and an exact retry returning its historical receipt after the current head moves. The context example preserves different declared dispatch states for the same source, and distinguishes an intact old pack from current accepted state. Acknowledgement checks establish reference consistency, not identity, understanding, or external execution.

See the historical [foundation verification](research/runs/foundation-verification.json), current [context verification](research/runs/context-verification.json), and [example result](research/runs/context-example.json) for commands and artifact identities.

## Repository review coverage

Base12's full pinned tree has 5,593 files / 180,332,790 bytes. The latest [stage-A records review](docs/source-review/base12-stage-a-records.md) brings full semantic reading to 224 distinct blobs (1,508,013 bytes), with 48 additional byte-identical alias paths. The earlier 539-path acquisition aggregate remains historical because its full private overlap index was not recovered. The [additive ledger](docs/source-review/base12-coverage-stage-a-records.json) separates nine full readings, partial manifest bindings and saved-count checks from execution; 5,321 paths / 4,205 distinct blobs still lack full semantic-reading claims. Whole-repository reading remains incomplete.

Prime Radiant's live checkout was not discovered through available repository access. The current retained research kit was reviewed instead: 193 files / 8,984,055 uncompressed bytes, with complete archive identity verification. The latest checkpoint has 86 complete semantic readings, seven separate complete historical source diffs, and two separately classified generated-manifest checks. All eight retained dialogue captures, eight associated receipts, three prose reports, and all 159 source-inventory records were read. The [latest audit](docs/source-review/prime-audits.md) keeps the 98 remaining numerical, visual, and binary files explicit; authored annotations in numerical records are among the gaps.

The precise source scope and transferable findings live in [research lessons](docs/research-lessons.md). No upstream code was executed or imported into this public project.

## Publication status

The original project is published at [rana/continuum](https://github.com/rana/continuum), a public MIT repository. GitHub sign-in completed, and connected read/write operations created the repository and published all 95 prepared files. The first published project commit is `3439f61989d344ff89df1b0cad4ea7fd119918e7`.

All three local development snapshots were imported with identical Git tree identities. The GitHub API assigned new commit metadata and parent links, so the public commit IDs differ from the local research IDs. The [source-commit map](research/publication/source-commit-map.json) records the exact correspondence, including the source used by the fresh Claude continuation. Original local history remains in the recoverable archive and the local `local-research-history` branch. Historical context packs and transcripts retain their original capture-time claims.

The first [GitHub Actions run](https://github.com/rana/continuum/actions/runs/39199405358) completed successfully on that project commit: formatting, strict Clippy, all-feature tests, and the acceptance demo. This confirms those checks on GitHub's hosted runner; it adds no high-load or comparative performance evidence. No packaged release or remotely deployed service is claimed.

## Next useful unit

The first release workload and [first real-use checkpoint unit](research/runs/project-checkpoint-pilot-1/README.md) are complete locally. The [checkpoint adapter](docs/operations/project-checkpoint.md) captures committed regular Git source through the existing CLI, authored WorkState, context coverage and build provenance in a disposable store. Six Python integration tests cover exact capture/reconstruction and failure boundaries; the existing Rust gates and 20 scenarios passed in this executor. One actual Claude successor received a 3,140-byte pack plus two explicitly supplied source documents, completed a custody review, and prompted concrete path-alias and binary-replacement protections. This is a qualitative observation with extra source exposure, not a pack-only performance result. See the run record for exact source, visible reply, corrections, validation and limits.

The [independent CSV pilot](research/runs/independent-csv-pilot/README.md) is now complete locally. A real Claude successor received a 3,737-byte native pack, requested three exact source files, and returned the missing-token requirement implementation. Applied without edits, it passed 11 CLI tests, an independently authored nine-scenario acceptance oracle, and concrete sample checks. Both independent source revisions and actual exchanges are retained; fresh reconstruction from the source bundle reproduced the snapshot and pack identities. Build-digest rejection also caught an all-feature test build replacing the measured default binary; reuse of the retained runtime succeeded.

The [recorded-attempt import unit](research/runs/checkpoint-object-import/README.md) now removes that transport gap. The checkpoint adapter accepts bounded explicit v1 Blob/Snapshot bundles, rejects missing/unrelated closure, verifies all native identities and preserves historical attempt references. Eleven adapter integration tests pass, including ambiguity, mismatch, closure, reconstruction and acknowledgement-as-receipt rejection. An actual earlier CSV model turn's seven objects were restored into two fresh stores, with exact retained request/response bytes, distinct historical/current source roots, identical packs and conditional guidance to inspect the receipt. This is authored historical reconstruction, not a new dispatch or native semantic request-response verification.

A [fresh receiver inspection](research/runs/recorded-attempt-receiver/README.md) now used that pack in four actual supplied-context Claude turns with three bounded retrieval rounds. It did not repeat the implementation and distinguished model output from execution evidence, but rediscovered a test-count correction already recorded outside the pack. Exact source comparison passed; causal avoided-work benefit is not established because the handoff explicitly forbade repeating the call. The inspection exposed missing native links to later execution outputs, unretained historical fixture bytes, and a connector message-field limit; exact exposure, failure and corrections are retained.

A [new source-bound CSV verification](research/runs/source-bound-verification/README.md) now retains exact source, chosen interpreter, fixed commands, every child input and raw output in a separate local attempt. Eleven tests and nine oracle cases passed, with 37 input observations retained. A deliberate scratch-worker exception verified that raw failure output and its failed native receipt survive absent worker result files. The historical model and new verification attempts travel together, with the known test-count correction explicit; restoring the exact artifacts repeated the pack identity. This is local observation under documented capture hooks, not authenticated execution or a full environment image.

A [bounded receipt-view continuation](research/runs/bounded-receipt-view/README.md) now supplied a fresh receiver a 7,136-byte identified projection of the 77,194-byte receipt, with complete selected/omitted subtree coverage and four corruption checks. Two actual Claude turns reused the recorded Linux result within its scope and declined to infer Windows/Python 3.11 support. Only the narrower verification inspection was accepted in model-authored text; the broader two-receipt offer has no full native acknowledgement. The raw/native digest distinction was explicitly prompted. No target-environment execution, general view API or comparative benefit is established.

A [SQLite online-backup experiment](research/runs/sqlite-online-backup/README.md) now restored a pinned generation-2 cut with all seven objects and three exact historical receipts while a separate native writer committed generation 3 between page-copy steps. Schema, rows, native object checks and retries matched; a main-file-only control retained the schema but lost WAL-held rows. Retrying the post-cut operation failed because its candidate was outside the restore. This is completed-copy behavior with the same native binary/schema, not crash-safe publication or a newest-history recovery guarantee.

The [native backup export](research/runs/native-backup-export/README.md) now implements a same-schema pinned cut, private staging, SQLite validation, file/directory sync and atomic no-overwrite linking on supported Unix filesystems. Five backup tests include ordinary failure cleanup, competing publishers and four process-exit boundaries; the default-build CLI smoke preserved exact retry behavior. Actual review identified the staging hard-link alias, now unlinked/synced before success and explicitly documented at the remaining crash gap. The returned review was truncated and is retained as partial. No power-loss, in-place restore or migration guarantee is established.

A [real checkpoint backup-use check](research/runs/checkpoint-backup-use/README.md) now exported the retained source-bound store and preserved all 17 objects, exact 5,420-byte context, generation-1 anchor and original receipt. Advancing only a disposable restored copy made current-anchor verification reject the old pack while historical projection verification and exact retry remained valid. Original source state and published export bytes stayed unchanged. No new inference, CSV execution, worker activation or receipt authentication is claimed.

A [controlled read-under-reservation probe](research/runs/read-writer-reservation/README.md) now observed `get`, `head` and `receipt` each fail after about five seconds under a held `BEGIN IMMEDIATE` with no data writes, while same-build SQLite read-only SQL returned committed rows. Baseline/post-rollback CLI outputs matched. Source inspection identifies the common `Store::open` immediate transaction before dispatch. This is one availability scenario, not a throughput comparison. Actual Claude advice and its limits are retained.

The [existing-only read-only Store/CLI path](research/runs/read-only-store/README.md) now routes all eight pure reads through a validated pinned snapshot without a writer reservation. Held-writer outputs match baseline, invalid identities/versions and corrupt objects fail, reopening observes later commits, and permission/sidecar behavior is explicit. A review-prompted guard rejects reads if SQLite loses the pin; its simulated rollback test passed. The final probe removes the three controlled locked failures. Writable initialization, mutations and backup opening remain unchanged. No throughput, activation or power-loss claim is added.

The [decision-gate source return](docs/source-review/base12-decision-gate.md) completed ten exact full readings without upstream execution. It separates artifact agreement from a decision about another target and identifies a conditional checked-bytes/parsed-path gap in the archive verifier. This is source-derived reasoning, not an observed exploit or historical failure. No private source bytes were published or upstream worker contacted.

The [native-boundary source return](docs/source-review/base12-native-reset.md) completed six full readings and four original-file manifest checks. It separates native runtime, native build and self-rebuild milestones, preserves distinct timing boundaries, and treats historical integration as authored evidence rather than fresh execution. No upstream invocation or private payload publication occurred.

The [signal-readiness source return](docs/source-review/base12-signal-readiness.md) completed five full readings. It records the conditional dictionary-overhead bound, separates shared work from per-arm timing, and preserves readiness failures and existing-owner coordination as attempt evidence. No upstream code, data, model or benchmark ran.

The [learning-performance source return](docs/source-review/base12-learning-performance.md) completed three full readings and two preservation checks. Recomputed arithmetic agrees with the reported totals and earlier bound; the original run was not reproduced. Lessons distinguish structurally constrained wins, net-saving denominators and recurrence-specific acceleration from measured whole-operation benefit.

The [alignment-pilot source return](docs/source-review/base12-alignment-pilot.md) completed eleven full readings, five source/result hash bindings and saved-count checks without execution. It separates identified relations from authored preservation of tied actions and finds a static mismatch: the runner imports backend modules before its documented digest gate. No exploit or historical failure was observed; raw run closure and inherited backend were not newly audited.

The [next-experiments source return](docs/source-review/base12-next-experiments.md) completed five full readings, four preservation checks and saved-data consistency checks without running the reference. It distinguishes exact recovery from summary sufficiency, equivalent formulations from experimental alternatives, and canonical identity from consumer benefit.

The [corpus-preservation source return](docs/source-review/base12-corpus-preservation.md) expanded from three wrapper files to four originals and their archive mapping. Seven texts were fully read; four archived payloads match the originals, and original/installed checksum mappings reconcile. Lessons preserve matched controls, rejected model claims, exposure and denominator provenance without claiming corpus acquisition or execution.

The [stage-A source return](docs/source-review/base12-stage-a-codec.md) completed seven full readings without importing code. It separates outer-checksum mutations from deeper rehashed-fault checks, exact reconstruction from multi-file publication, and numerical kernels from whole-application ownership. A possible partial output after interruption is source-derived, not an observed failure or an atomic-publication promise violation.

The [stage-A records return](docs/source-review/base12-stage-a-records.md) completed nine full readings and reconciled saved assertions/generated-code size. Thirteen of eighteen source-manifest entries and fourteen of forty-nine preservation entries match acquired bytes; the rest remain explicit. A failed local binding check exposed an older reading entry without a current byte copy; the corrected check admits only present exact payloads. No historical run or acquisition was repeated.

Next bounded review: six unread JSON records / 22,004 bytes under stage-A aum-run evidence: delivery manifest, intake acquisition receipt, execution receipt, input/code record, postrun verification and attempt record. Reconcile source and ownership; do not import code or replay historical instructions. Practical backup/read fixes are complete; avoid another CSV feature/inference round. The owned-storage finite model remains separate; full backup/upgrade guarantees remain open. No recipient has accepted this next unit.

Controlled context-history scaling remains a follow-up when use identifies the need. Keep mandatory facts, byte budget, environment, omission coverage, and expected outcomes explicit. If the selected unit's execution capability is unavailable, advance the next bounded source-review group from the coverage ledgers instead of writing another unchanged status recap.

The [fresh-model trial](research/continuation-trial/README.md) is complete. The full upstream reading request and a controlled model-performance comparison remain open.

Before adding a remote executor or model runner, specify durable dispatch and uncertain-outcome reconciliation. Add resource measurements before a fleet scheduler.

## Continuation setup

The operating method, complete Codex handoff, orientation, workload, and raw observations were published in `8e400c1946838be4e601261ae35c3cc81750c042`. Its [GitHub CI run](https://github.com/rana/continuum/actions/runs/39204429362) passed, including the new workload smoke invocation.

The recurring **Advance Continuum** task was confirmed created and enabled at 2026-10-19 05:29:22 UTC. It requests hourly flexible scheduling in `America/Los_Angeles`, with a start anchor of 2026-10-18 22:45. The creation response provided no precise next-run timestamp and no completed run. The [setup observation](research/runs/continuation-setup-2026-10-19.json) preserves that distinction. Read actual task history before claiming unattended progress. That was the continuation responsibility observed at that historical setup; it does not establish exclusive current ownership.

GitHub read/write and the supplied-context Claude collaborator were verified in this session. No direct Dot dispatch or user-workstation Continuum worker was verified. A ready startup prompt is available in the operating document. Existing responsibilities for other projects are separate and were not changed.

The current local desktop chat has a confirmed active **Continue Continuum** heartbeat at a one-minute cadence, requested by the user. Its [configuration observation](research/runs/independent-csv-pilot/heartbeat-observation.json) is not evidence of a completed unattended run. The older cloud task's live status/cancellation is unavailable through this app; the local prompt requires remote and ownership reconciliation before overlapping work. Keep this computer and app running for local continuation. Native builds and disposable checkpoint runs were observed in the current desktop shell; no persistent worker installation is claimed.

The first observed local heartbeat continuation arrived at 2026-10-19 06:06:01.672 UTC (2026-10-18 23:06 Pacific) and performed the [recorded-attempt import unit](research/runs/checkpoint-object-import/README.md). This links an actual wake-up to work and validation; the older setup-only observations retain their historical scope. Publication and hosted CI are recorded on that unit's PR.
