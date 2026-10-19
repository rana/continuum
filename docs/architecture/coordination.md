# Missions, directives, cues, and work streams

Status: design contract above the initial core.

## Different structures answer different questions

| Record | Question it answers | What it must not silently become |
|---|---|---|
| Mission | Why does this project exist? | An unlimited permission grant |
| Objective | What outcome are we pursuing? | A claim that work is complete |
| Directive | What instruction applies in this scope and time? | An immutable instruction after its authority changes |
| Grant/policy reference | Who permits or restricts this effect? | A confidence score or model preference |
| Protocol | What reusable procedure helps? | A new source of authority |
| Skill adapter | How does a particular host expose the method? | A separately maintained fork of its meaning |
| Prompt | What concrete inputs and wording invoke a computation? | A reliable state database |
| Cue | What should be noticed or considered? | A required dependency or automatic command |
| Priority signal | What work is more valuable now, under which source? | A global truth or permission override |
| Receipt | What state or effect was actually recorded? | Evidence that every downstream consequence occurred |

A directive needs provenance, applicability scope, validity conditions, and a supersession relationship. Preserve the original and append a successor; derive the active view from actual authority and scope.

A cue can point to a weak signal, unresolved inconsistency, surprising result, resource opportunity, or new model capability. Preserve its uncertainty. Promotion to a framed investigation supplies a question and completion/revisit conditions; an imaginative seed need not pretend to be an executable experiment.

## Work graphs are not all dependency graphs

Base12's possibility-map method distinguishes prerequisites from relationships such as informs, contrasts, tests, and motivates. Continuum adopts that distinction.

Only execution prerequisites impose scheduling order. Evidence dependencies, assumptions, authority grants, context exposure, and contrastive ideas have their own semantics. An exploratory graph can contain cycles even when the selected prerequisite graph must be acyclic. Iteration can create new attempts rather than self-dependent tasks.

Staleness cannot be propagated solely along scheduling prerequisites. A changed assumption or withdrawn evidence record can affect a decision even when it is not a task's requires edge. Use typed reverse indexes and explicit propagation rules. A suggestion that merely informs a decision is not automatically an invalidation.

## Parallel work

Choose parallelism when tasks have independent inputs or when distinct approaches can resolve a consequential disagreement. Use explicit ownership of mutable workspace files, immutable candidate snapshots, and small coherent integration units.

A work stream is a view over objective, attempt, dependency, and receipt records. It is not another canonical copy of all those records.

The future scheduler should distinguish ready, blocked-on-input, awaiting-external-reconciliation, resource-limited, and paused-by-authority work. Priority can combine user direction, critical-path value, uncertainty reduction, deadlines, cost, and age. These dimensions should remain inspectable rather than disappearing into one unexplained score.

More models or machines can increase contention and correlated error. Evaluate useful accepted outcomes, recovery, and cost before raising concurrency.

## Handoffs

An offered handoff references an exact checkpoint, objective, remaining uncertainty, proposed responsibility, resource bound, and needed capabilities. Receipt confirms arrival. Acceptance means the named recipient actually takes responsibility under its existing authority. Completion and external effect confirmation are further records.

A repository can store and transport these records. Waking a chat, scheduling a worker, or installing a plugin requires a real supported integration. No document can create that capability by declaring a handoff complete.

## Next external-effect invariant

Before introducing a model runner or remote executor, design a durable dispatch record with operation ID, effect digest, destination, relevant authority epoch, and a reconciliation contract.

The safe ordering must cover the gap between recording dispatch and the external service receiving it:

1. Persist preparation and an outbox entry atomically with the selected dispatch decision.
2. Before sending, persist a may-have-been-sent state under the dispatcher's current fenced ownership.
3. Send with the recipient's supported idempotency key when available.
4. Append observations of acknowledgement, failure, or unresolved outcome.
5. On recovery, reconcile ambiguous attempts. Never infer that a timed-out request was not performed.

Marking dispatched only after the network call would leave a crash gap. Marking it before sending can conservatively produce an unknown outcome even when nothing was sent; that is a recoverable limitation, not permission to guess. An outbox alone cannot guarantee exactly-once effects at an arbitrary receiver.

A future context pack should expose unresolved relevant attempts or mark that closure as unestablished. A model response cannot resolve unknown execution merely by sounding certain.

