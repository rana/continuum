# Continue Continuum: research, implementation, and durable progress

Continue developing `https://github.com/rana/continuum` for Rana Ian. Treat this as an authorized ongoing engineering and research program. Make useful progress autonomously, make routine technical choices, implement, run relevant checks and bounded experiments, and publish coherent project contributions under the existing public MIT development authorization. Carry the work through a useful result; do not stop at a plan or repeatedly ask for permission already granted.

## Purpose and North Star

Continuum is a native work and evidence engine for continuing AI engineering across conversations, models, workers, interruptions, and eventually machines. Source code is one important artifact within a continuing investigation. Preserve the objective, exact artifacts, attempted actions, observations, decisions, alternatives, uncertainty, and the next useful move.

Optimize for time to a correct next action, useful completed work, reliable recovery, and less repeated investigation. Prefer a small working mechanism that demonstrably helps an agent over a large collection of speculative features. Preserve imaginative questions without turning every idea into a required task. The project is an independent design inspired by the need for AI-native work; it does not claim access to Anthropic's private Scion implementation.

## Model and working environment

The starting preference for this code-heavy task is GPT-6.1 Sol, Standard speed, Medium reasoning, where available in the current client. Use higher reasoning for a concrete difficult issue such as persistence, encoding, concurrency, or a consequential architecture tradeoff. These preferences do not prove which model is actually selected. Record actual model/tool metadata when exposed, and use the current session's real capabilities.

Use a fresh checkout or isolated worktree. Check the current remote head and preserve unrelated or uncommitted work. A tool executor is not automatically Rana's workstation. A repository handoff does not dispatch Dot, and a prompt does not install a scheduler. Continue through the active task's supported capabilities; coordinate any real host or recurring-task ownership explicitly.

## Recover current state efficiently

Read `AGENTS.md`, `README.md`, `CURRENT.md`, `docs/orientation.md`, and `docs/operations/continuation.md` at the current repository revision. `CURRENT.md` is the home for the selected next unit. Follow its links and read the relevant implementation, decision, protocol, and evidence. Check relevant open/merged PRs before duplicating work. This handoff is an orientation; newer verified repository state and current user direction may supersede its dated facts.

Do not spend the initial task rereading every historical transcript or designing a second coordination system. The broader request to study Base12 and Prime Radiant remains open with exact coverage ledgers; advance it in coherent groups when it is the selected useful work. Do not claim those whole repositories have already been read. Private upstream source and operational records must remain private.

## What already exists

The Rust core has exact-byte Blobs, restricted source Snapshots, and declared EvidenceRecords with explicit versioned, domain-separated SHA-256 identities. Snapshot links form a small Merkle DAG. The current format covers normalized relative UTF-8 file paths; it is not complete Git filesystem fidelity.

A local SQLite transaction conditionally advances an acceptor/target head using an expected root and generation, and atomically retains the operation's receipt. Exact retries return their historical result; the same operation ID with changed request content is rejected. Generation distinguishes a restored root from an unchanged state. Slow inference belongs outside that transaction.

The context path retains an exact WorkState and selects complete records into a byte-bounded rendering. It preserves objective, attempts, decisions, uncertainties, and an offered handoff. Historical verification and current-anchor observation are separate. An acknowledgement checks exact references; it does not authenticate a recipient, prove understanding, or establish an external effect.

The recorded foundation has 20 scenario tests, including process-crash recovery. One actual fresh Claude continuation from an 8,321-byte native context pack is preserved. It is an observational trial, not a general model-performance result. A release workload now measures nine operation groups in three separate 100-sample-per-group runs with checked outcomes and retained raw timing/provenance. Use `CURRENT.md` and the evidence records to verify whether these facts have since changed.

The repository contains original adaptations of Progress Brief, Holographic Walk, Research Record, and Bounded Research Loop. Select a method when it serves the question. A protocol is a procedure, a skill is a host adapter, and a prompt invokes work; none grants authority, supplies a runtime, or makes a claim true.

## Implementation direction

Retain the small native Rust core, explicit portable formats, and short durable transactions. SQLite and existing cryptographic libraries provide the current foundation. The project is hosted and developed on GitHub; the native runtime has no Git dependency. Future Git interoperability belongs at an adapter boundary.

Choose further machinery from observed needs. The first prototype does not yet implement a general model runner, remote execution, authenticated multi-user acceptance, replication, a public server, a fleet scheduler, garbage collection, or a complete semantic dependency graph. Avoid describing proposed capabilities as shipped. Assembly, a new compiler, a custom database, or replacement networking should earn their complexity through a concrete requirement and measurement.

## Select the next useful unit

Start from current priorities and actual ownership. Rana's latest direction is to learn the product's design by actually using it. Read `docs/experiments/real-use-pilot.md`. The first consumer is Continuum's own development; a small independent public example follows to expose assumptions that only fit this project.

The next useful implementation is a small repeatable project-checkpoint entry point using the existing CLI: exact source, authored WorkState, prepared context with coverage, and build/run provenance. Use it in one real successor handoff, recording what the receiver needed, what was missing or unused, extra retrieval, and actual consequence. Keep the first store disposable unless the preservation/upgrade path is ready. A workstation installation must be observed on the actual host. For persistent use, separate binary and data, identify exact builds, reject unsupported store formats, and test consistent SQLite backup/restore; copying only the main file of an active WAL database is insufficient.

Context-history scaling remains a useful follow-up: hold mandatory facts, byte budget, omission coverage, environment, and expected outcomes explicit. Choose it when actual use identifies the relevant need. Do not optimize storage before identifying the relevant cost.

If newer evidence makes a different unit more useful, explain the choice and proceed. If execution is unavailable, advance an actionable source-review, derivation, or design unit instead. Genuine negative findings and clarified constraints count as progress. Repeated unchanged recaps do not.

## Collaborate without losing research continuity

The research conversation remains a place for framing, synthesis, and user steering; this Codex task is an implementation environment. GitHub carries the durable exchange. Do not require Rana to copy progress messages between chats.

For each substantive unit, preserve a concise Research Delta in the appropriate existing repository record: question and source revision; what changed; what was learned with exact evidence; negative findings and rejected approaches; untested conditions and unresolved effects; and the next action with its actual ownership. Link it from the PR. Update `CURRENT.md` when the selected next action or verified capability changes. Preserve one authoritative home per fact instead of creating another live dashboard.

Use an actual Claude consultation when it can change a consequential interpretation, experimental method, or architecture choice and the collaborator is available. Supply the relevant user direction and source context; Claude cannot be assumed to read the repository or remember another exchange. Preserve the actual visible reply, metadata, input exposure, and any corrections. Do not simulate Claude, treat agreement as empirical proof, or automatically retry an invocation with an unknown outcome. Useful independent work can continue when a collaborator is unavailable.

Use Dot only through an actual connected route or established repository exchange. Offered, received, accepted, completed, and effect-confirmed are different states. Do not claim a recipient accepted ownership without its actual response. Parallelize disjoint work or focused independent review; reconcile overlapping integration ownership.

## Verify, publish, and continue

Use the relevant existing checks. For code changes, the normal gates are `cargo fmt --all -- --check`, `cargo clippy --locked --all-targets --all-features -- -D warnings`, and `cargo test --locked --all-features`. Run the appropriate example or bounded experiment when it addresses the changed behavior. The workload smoke test checks correctness without a timing threshold. Do not add tests that merely restate implementation or prose.

Record source identities, commands, observed results, environment and resource limits, and missing evidence. Keep build success, local execution, hosted CI, workstation execution, publication, and activation distinct. Preserve raw evidence that is needed for recovery and interpretation, without credentials or private upstream material.

Use a scoped branch and reviewable contribution, or the repository's established authorized integration route. Recheck the current remote head and use non-forced updates with actual preconditions. A branch conflict requires inspecting the new work. A lease note is not a distributed lock; an expired claim does not prove an earlier worker stopped. Reconcile uncertain external effects before retrying them.

Work in coherent bounded units, checkpointing roughly every 15 minutes during long work when there is meaningful state to retain. Complete the unit's relevant validation and publication, then choose the next ready unit while this active task can continue. Do not install a competing timer or silently stop the continuing objective after an arbitrary quota of checks. At an actual execution boundary, preserve enough context for the next supported run.

Finish each useful result with its source/PR links, evidence, what changed in our understanding, the important limitation, and the single best next action. Begin now by recovering the current state, selecting the highest-value ready unit, and doing the work.
