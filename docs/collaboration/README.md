# Actual Claude collaboration

The initial historical briefs contain earlier preserved Claude exchanges. This directory records the next two actual Claude Opus 5.5 exchanges on 2026-10-19 UTC.

| Exchange | Actual exposure | Result |
|---|---|---|
| [1](2026-10-19-claude-01.md) | Entire current user transcription and subsequent full-repository-review request, plus coordinator design and source summaries | Proposed context-linked decisions and targeted review; challenged scope; initially preferred Git as source authority |
| [2](2026-10-19-claude-02.md) | Actual supplied Prime/Base12 excerpts, implementation facts and coverage limits, coordinator corrections, previous visible answer | Accepted the native-source direction and explicit publication operations; proposed durable effect attempts and distinction-pair experiments |

The [user wording](2026-10-19-user-brief.md), exact supplied [first request](requests/claude-01.json), [second request](requests/claude-02.json), and [execution metadata](../../research/runs/) are retained. Responses are unedited except for surrounding provenance notes. Claude had no direct filesystem, browser, or repository tools in these exchanges.

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

These are design decisions, not a claim that the unimplemented capabilities already exist.

