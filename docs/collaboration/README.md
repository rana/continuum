# Actual Claude collaboration

The initial historical briefs contain earlier preserved Claude exchanges. This directory records six further actual Claude Opus 5.5 exchanges on 2026-10-19 UTC.

| Exchange | Actual exposure | Result |
|---|---|---|
| [1](2026-10-19-claude-01.md) | Entire current user transcription and subsequent full-repository-review request, plus coordinator design and source summaries | Proposed context-linked decisions and targeted review; challenged scope; initially preferred Git as source authority |
| [2](2026-10-19-claude-02.md) | Actual supplied Prime/Base12 excerpts, implementation facts and coverage limits, coordinator corrections, previous visible answer | Accepted the native-source direction and explicit publication operations; proposed durable effect attempts and distinction-pair experiments |
| [3](2026-10-19-claude-03.md) | Latest user deferral of GitHub, implemented foundation, proposed context shapes, source-review findings and limits | Identified provenance and freshness risks; proposed controls for a discriminating context experiment |
| [4](2026-10-19-claude-04.md) | Only an 8,321-byte native context rendering for the real project plus a short task request; no prior exchange or source objects | Recovered reported completion, renewed publication authorization, pending authentication, and a bounded next step; supplied an acknowledgement that passed native reference checks |
| [5](2026-10-19-claude-05.md) | Full latest user request for unattended progress, verified project/runtime facts, candidate operating model | Favored useful bounded units, explicit schedule/run/progress evidence, and a release workload; ownership and timing claims needed correction |
| [6](2026-10-19-claude-06.md) | Full timer request and Base12 follow-up, recovered workflow/model recommendations, actual setup observations, and coordinator corrections | Favored repository Research Deltas and decision-point review; correctly distinguished continuity from execution, but understated the active chat's capabilities |

The [user wording](2026-10-19-user-brief.md), exact supplied [first request](requests/claude-01.json), [second request](requests/claude-02.json), [third request](requests/claude-03.json), [fourth request](requests/claude-04.json), and [execution metadata](../../research/runs/) are retained. Responses are unedited except for surrounding provenance notes. Claude had no direct filesystem, browser, or repository tools in these exchanges.

The [fifth](requests/claude-05.json) and [sixth](requests/claude-06.json) public request files are explicitly redacted projections because their supplied context included private operating state from another project. Exact request fields and actual responses are retained in the owner's private `Continuum_Continuation_Private_Checkpoint.json`. The public projections preserve request digests and state their encoding; they are not represented as complete reproducers. The complete visible responses and returned metadata remain in this repository.

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

