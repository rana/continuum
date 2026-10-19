# Actual Claude collaboration

The initial historical briefs contain earlier preserved Claude exchanges. This directory records eight numbered further actual Claude Opus 5.5 exchanges on 2026-10-19 UTC. Separate project trials also retain their own actual collaborator records.

| Exchange | Actual exposure | Result |
|---|---|---|
| [1](2026-10-19-claude-01.md) | Entire current user transcription and subsequent full-repository-review request, plus coordinator design and source summaries | Proposed context-linked decisions and targeted review; challenged scope; initially preferred Git as source authority |
| [2](2026-10-19-claude-02.md) | Actual supplied Prime/Base12 excerpts, implementation facts and coverage limits, coordinator corrections, previous visible answer | Accepted the native-source direction and explicit publication operations; proposed durable effect attempts and distinction-pair experiments |
| [3](2026-10-19-claude-03.md) | Latest user deferral of GitHub, implemented foundation, proposed context shapes, source-review findings and limits | Identified provenance and freshness risks; proposed controls for a discriminating context experiment |
| [4](2026-10-19-claude-04.md) | Only an 8,321-byte native context rendering for the real project plus a short task request; no prior exchange or source objects | Recovered reported completion, renewed publication authorization, pending authentication, and a bounded next step; supplied an acknowledgement that passed native reference checks |
| [5](2026-10-19-claude-05.md) | Full latest user request for unattended progress, verified project/runtime facts, candidate operating model | Favored useful bounded units, explicit schedule/run/progress evidence, and a release workload; ownership and timing claims needed correction |
| [6](2026-10-19-claude-06.md) | Full timer request and Base12 follow-up, recovered workflow/model recommendations, actual setup observations, and coordinator corrections | Favored repository Research Deltas and decision-point review; correctly distinguished continuity from execution, but understated the active chat's capabilities |
| [7](2026-10-19-claude-07.md) | Full user real-use request, current public implementation and measurement summary, runtime limits, candidate consumers | Chose Continuum itself first, a small independent project second, and observations of context gaps; backup and upgrade advice required correction |
| [8](2026-10-19-claude-08.md) | Full user SQLite/Rust-alternatives question, actual schema and operation summary, current primary-document summaries | Prioritized atomic acceptance, durable receipts, process ownership and relocated invariants; overstrong compatibility, language, and permission claims were corrected |

The [user wording](2026-10-19-user-brief.md), exact supplied [first request](requests/claude-01.json), [second request](requests/claude-02.json), [third request](requests/claude-03.json), [fourth request](requests/claude-04.json), and [execution metadata](../../research/runs/) are retained. Responses are unedited except for surrounding provenance notes. Claude had no direct filesystem, browser, or repository tools in these exchanges.

The [fifth](requests/claude-05.json) and [sixth](requests/claude-06.json) public request files are explicitly redacted projections because their supplied context included private operating state from another project. Exact request fields and actual responses are retained in the owner's private `Continuum_Continuation_Private_Checkpoint.json`. The public projections preserve request digests and state their encoding; they are not represented as complete reproducers. The complete visible responses and returned metadata remain in this repository.

The [seventh request](requests/claude-07.json) is retained in full; it supplies current public project facts and the complete user request for learning by using the software.

The [eighth request](requests/claude-08.json) is retained in full. It preceded the later dependency inspection and concurrent checkpoint-pilot merge; those updates appear in the storage assessment rather than being retroactively inserted into Claude's exposure.

## Adopted design contributions

- Preserve the exact context of decisions, with known omissions.
- Use targeted re-evaluation instead of automatically replaying all historical work on a new model release.
- Keep model identity separate from evidence quality.
- Keep the trust-critical local transaction small.
- Treat protocols as versioned methods under existing authority.
- Develop context tests from histories that a summary conflates but a future action distinguishes.
- Put durable effect attempts and reconciliation before a general scheduler.

## Disagreements and corrections retained

Claude initially proposed that Git permanently own source. The coordinator retained the user's native-first experiment: the native store owns source on routes that adopt it; Git is an import/export edge. Claude accepted that revision. Neither design permits uncontrolled dual writes.

The coordinator also separated publication into storage, replication, discovery/sharing, acceptance, and activation. Sharing an unaccepted proposal is legitimate within its authority. Protocol adoption need not create a new approval ceremony for already authorized routine work.

Two details in the second reply require qualification:

1. Scheduling requires edges are not the only relationships relevant to staleness. Changed evidence, assumptions, or authority can also affect decisions. Propagation must be defined by edge kind.
2. An external-effect state machine must handle a crash between sending and recording that it sent. Persist possible dispatch before sending, retain uncertainty, and require recipient-supported idempotence or reconciliation. A simple state label or transactional outbox cannot establish exactly-once execution at an arbitrary receiver.

The proposed context experiment must evaluate whether the needed distinction is intelligible and supports the correct action. Different pack hashes alone do not establish useful context: a timestamp could change a hash while decisive information is still absent.

Cross-review is not automatically independent evidence. Preserve which inputs, tools, code, and previous model answers were shared. Model diversity is useful when it creates a discriminating perspective; agreement does not certify truth.

## Context review corrections

The third response usefully distinguishes exact custody, authored interpretation, and derived guidance. Context acknowledgements must not pretend to establish execution, authorization, understanding, or success. An immutable pack can be historically intact while stale relative to a moving accepted head; those require separate results.

The coordinator retained three qualifications to that response:

1. The existing operation log records local acceptance operations. It is not an external dispatch ledger, and cannot by itself verify a WorkState's external-dispatch claim. The prototype displays such claims as authored, with conditional guidance. A future runner needs an instrumented dispatch boundary before it can supply stronger evidence.
2. Absence of a send record proves nothing about actions outside a complete instrumented route. Do not label an operation never-sent merely because a lookup is empty. Opaque retained receipts likewise do not prove an operation/request binding unless the particular receipt format and issuer support that check.
3. A freshness observation can become stale immediately after it is read. It supports orientation; a later consequential operation must enforce its own current preconditions. Moving a head does not corrupt the original pack or erase its historical acknowledgement.

For experiments, a prompt containing the correct next-action label would confound representation with instruction following. The proposed evaluator should receive a neutral question, with hidden expected answers and separate raw-fact and guidance conditions. Small preserved trials can expose a specific failure; they cannot establish general model performance.

These are design decisions, not a claim that the unimplemented capabilities already exist.

## First real-project context continuation

The [trial record](../../research/continuation-trial/README.md) contains the exact native source snapshot, work state, prepared pack, returned response, acknowledgement, native validation result, and retrospective assessment. The receiver correctly kept the old publication deferral historical and the latest authorization current, while preserving the unknown authentication result. It qualified the reported test outcome rather than pretending to have inspected the source or receipt itself.

Two qualifications remain visible. The model returned a Markdown code fence despite a JSON-only request. The coordinator extracted the exact acknowledgement object substring, retained the full original response, and submitted the object as a proxy; it was not silently reserialized. The suggested fresh local expected-head check also cannot make a later GitHub action atomic or confer authority at that external service. The external effect needs its own supported preconditions, result observation, and reconciliation contract.

The trial is one observed continuation with supplied authored facts. It has no randomized control, blinded comparative grading, or model-performance estimate. Native acceptance of the acknowledgement establishes reference consistency, with recipient authentication, understanding, and external-effect verification explicitly false.

## Continuing research while implementation proceeds

Exchanges five and six informed the [continuing work method](../operations/continuation.md). Adopted contributions are a small durable Research Delta, one accountable owner for overlapping integration, actual execution evidence, decision-point consultation, and a useful first release workload. The method borrows the Chat/research, Codex/implementation, GitHub/continuity pattern already used in Base12.

Retained corrections:

1. A Git lease note is not an enforced distributed lock. Expiry does not prove a worker stopped, and an expected branch-head condition protects publication rather than remote execution. Unknown overlap requires reconciliation or disjoint work.
2. Two unproductive units or an arbitrary nightly count do not complete a continuing objective. Reassess the question, preserve a blocker, or advance another ready unit under the existing resource scope.
3. Cloud and CI measurements are real observations of their recorded environment. Unknown physical storage and competing load limit comparison; a user's workstation is not the only intrinsically valid place to measure.
4. Lack of a separate Dot/Codex dispatch tool does not imply that a code-capable research session can only summarize. This coordinating session actually implemented, built, tested, and measured a contribution through its available executor and GitHub connection. Future runs must establish their own capabilities; no unattended implementation is inferred merely from the saved schedule.
5. Inability to set a scheduled task's model to Sol does not demote its engineering judgment or make it authoritative. Evaluate all model output through its evidence. The actual scheduler interface did not expose a model-setting argument.
6. Repository continuity, a saved schedule, an observed scheduled run, a meaningful research result, and successful CI are distinct facts. A useful derivation or negative finding need not be code to count as progress; passing CI alone does not prove the result's meaning.

## Real-use pilot corrections

Exchange seven usefully frames the project as a tool to think with, selects self-use and an independent consumer, and proposes recording what the receiver needed but could not find. The [pilot](../experiments/real-use-pilot.md) adopts that direction with these corrections:

- A live SQLite WAL store cannot be backed up reliably by copying only the main database file. Use a supported consistent backup mechanism, check its completion, and exercise recovery on a separate destination. The [SQLite backup API](https://www.sqlite.org/backup.html) and [WAL documentation](https://www.sqlite.org/wal.html) establish the relevant boundary.
- A source build is acceptable when its exact inputs, toolchain, command, and executable are identified. A moving branch name alone is insufficient provenance. No new release ceremony is required for a disposable local trial.
- Binary version, store schema, object codec, and context schema are distinct compatibility surfaces. The proposed installation and migration behavior is not already implemented. Put build metadata in a trial manifest initially; changing core receipts requires an explicit compatible contract.
- Restoring an older store can discard accepted work created after that backup. Keep both histories when testing a candidate and reconcile before any destructive data rollback. Software rollback alone does not require erasing later evidence.
- Existing user authorization remains in effect. Coordinate a later Base12/Prime contribution with its actual current owner and scope without inventing another blanket permission gate.
- The first few handoffs are an early design-learning checkpoint. They are not a statistical quality estimate or an arbitrary end to continuing development. Administrative upkeep and missing context should be observed before adding a new native gap-record type.

## Storage review corrections

Exchange eight informed the [embedded storage assessment](../experiments/embedded-storage-evaluation.md). The visible answer is retained with these qualifications:

- Durable acknowledgement is a contract relative to a persistence barrier and the OS/filesystem/device model. The current process-crash tests do not demonstrate physical power-loss behavior.
- Required invariants need not be SQL constraints. A KV backend can enforce them through a small centralized Rust write interface; the comparison must include the implementation and verification of those responsibilities.
- Removing the SQLite C engine does not guarantee a single memory-safety or cross-compilation story. Later inspection found feature-dependent native crypto/SIMD dependencies in Turso's core manifest. Ordinary OS FFI is a different boundary from a C database engine, and neither observation alone decides performance or reliability.
- Turso documents partial compatibility; this does not establish that every use of SQLite tools on its files is unsafe. Test the relevant read/export/import path on retained copies. Do not assume simultaneous mixed-engine writers or experimental file features are interoperable. The stubbed backup API is not an existing Continuum-path failure, because no such backup command is implemented; VACUUM INTO is a separate documented option to validate.
- Experimental multi-process support is an evaluation gate, not proof that a daemon is the only possible architecture. Direct sharing under an explicitly tested mode, serialized exclusive use, and a single owner with IPC are distinct choices.
- The existing user's R&D authorization persists. Neither the coordinator's scope wording nor Claude's suggestion creates a new permission requirement for a bounded conformance experiment. No migration was performed in this review.
- Store::open taking an immediate transaction is a profiling candidate. A change must preserve initialization and format-validation races; no measured contention bottleneck or safe replacement path was established merely by reading it.
- Fjall needs persistence covering every durable acknowledgement; group commit is possible if acknowledgements wait for the covering barrier. It is not necessary to prescribe one physical sync per logical operation in every architecture.
- The supplied redb summary mentioned Eventual from older API knowledge. The freshly inspected 4.4.0 Durability documentation lists None and Immediate. The assessment uses Immediate and does not carry the obsolete variant forward.
- The consultation preceded the later checkpoint and independent-example pilot merges. Its suggestion to retain the pilot remains useful, but CURRENT.md owns the advancing next unit. Preserve the subsequent work instead of treating Claude's exposure as current repository state.

