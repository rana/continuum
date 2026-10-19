# Actual Claude collaboration

The initial historical briefs contain earlier preserved Claude exchanges. This directory records three further actual Claude Opus 5.5 exchanges on 2026-10-19 UTC.

| Exchange | Actual exposure | Result |
|---|---|---|
| [1](2026-10-19-claude-01.md) | Entire current user transcription and subsequent full-repository-review request, plus coordinator design and source summaries | Proposed context-linked decisions and targeted review; challenged scope; initially preferred Git as source authority |
| [2](2026-10-19-claude-02.md) | Actual supplied Prime/Base12 excerpts, implementation facts and coverage limits, coordinator corrections, previous visible answer | Accepted the native-source direction and explicit publication operations; proposed durable effect attempts and distinction-pair experiments |
| [3](2026-10-19-claude-03.md) | Latest user deferral of GitHub, implemented foundation, proposed context shapes, source-review findings and limits | Identified provenance and freshness risks; proposed controls for a discriminating context experiment |

The [user wording](2026-10-19-user-brief.md), exact supplied [first request](requests/claude-01.json), [second request](requests/claude-02.json), [third request](requests/claude-03.json), and [execution metadata](../../research/runs/) are retained. Responses are unedited except for surrounding provenance notes. Claude had no direct filesystem, browser, or repository tools in these exchanges.

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

