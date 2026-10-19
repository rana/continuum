# Continuing research and implementation

This is the operating method for developing Continuum with several AI sessions. It uses the existing repository and host capabilities. The native core is the subject of the research; it does not yet run this operating method itself.

## Desired outcome

A later session can recover what matters, continue useful work, and explain its result without the user transporting context between applications. Optimize for completed useful units, sound decisions, recovery from interruption, and time to the next verified result. Activity, token use, and commit counts are not substitutes.

The selected next unit and current capability status belong in [CURRENT.md](../../CURRENT.md). Consequential decisions retain their existing authoritative homes. This document defines a method, not another backlog or status dashboard.

## Roles and model preferences

| Role | Responsibility | Starting preference |
|---|---|---|
| Research conversation | Frame questions, recover evidence, integrate findings, choose the next useful direction | Keep the ongoing research conversation; use its actual available model |
| Codex / code-capable Work task | Implement, execute, debug, test, and publish scoped changes | GPT-6.1 Sol, Standard speed, initially Medium reasoning where the client offers these settings |
| Claude consultation | Challenge consequential interpretations, methodology, and architecture choices | Actual configured Claude collaborator; include the necessary source context on every call |
| Dot | Coordinate or continue tasks through its connected computer/cloud environment, once that route is verified for this project | Use its actual supported configuration; do not invent a selectable model or dispatch capability |

These are preferences, not claims that settings have been changed. Model selection, execution environment, and task scheduling are separate choices. Increase reasoning effort for a concrete difficult question when it helps; no routine need to use the highest setting or invoke every model for every unit. Record actual returned model and effort metadata where available. A model name neither authenticates a worker nor establishes the truth of its output.

Chat and Codex do not need identical conversation histories. They need access to the same relevant durable facts. Preserve decisions, evidence, rejected approaches, uncertainties, and next actions in GitHub so either session can reconstruct them. An uncommitted experiment or a thought left only in a private conversation may be invisible to another session.

This method adapts the established Base12 research/implementation bridge. It carries over the method, not that project's private operational records, permissions, owners, or schedules.

## One continuing work cycle

1. Read current user direction and fresh remote `main`, then `AGENTS.md`, `CURRENT.md`, and this document. Inspect relevant open/merged PRs, run evidence, and actual recipient replies since the last reliable checkpoint. Recover material changes before relying on an old summary.
2. Select one useful bounded unit from current priorities. State its question, expected contribution, completion condition, needed capabilities, and owner. Use an isolated checkout/branch or explicit ownership of disjoint files. A recent ongoing task should be reconciled before starting overlapping work.
3. Perform the work using capabilities actually present. This may be implementation, an experiment, source reading, a derivation, or a design contribution. A scheduled research session with repository access can still make useful contributions when a separate Codex worker is unavailable. Do not label unexecuted code as tested.
4. Check the result proportionately. Use relevant tests and original evidence. Seek an actual Claude perspective when it can change a consequential decision; supply enough context and record its exposure and limits. Additional model agreement is not an empirical result.
5. Preserve the Research Delta and meaningful evidence in the repository, using the existing [Research Record](../../protocols/research-record.md) method. Publish a coherent scoped change under existing authority, verify the resulting remote state, and inspect applicable CI.
6. Reconcile the selected next action in `CURRENT.md` when it materially changes. Leave a sufficient partial-work checkpoint at an interruption. Continue another ready unit when the active execution environment allows it, or let the configured continuation mechanism resume later.

Roughly 15 minutes is a checkpoint target within active work, not a command to launch another worker. Finish at a coherent boundary; do not create an empty checkpoint commit just because time elapsed. The currently exposed recurring scheduler supports hourly wakeups. A shorter recurring interval requires a separately verified capable host; this repository does not install one.

## Research Delta

At a substantive unit's closure, preserve a concise record with:

- Unit/question, actual owner where known, input source revision, and resulting artifact or PR.
- What changed and what was learned, with commands, raw results, source references, or CI links supporting each material claim.
- Negative findings, rejected approaches, uncertainties, untested conditions, and any unresolved external effect.
- The next useful action, its expected contribution, and whether an actual recipient has accepted it.

Use an existing appropriate decision or run record instead of duplicating it. The PR can summarize and link the durable record. Ordinary edits need not manufacture research findings, and unchanged status does not require a new file.

## Ownership, publication, and interruption

Keep one accountable integration owner for overlapping changes. Parallelize disjoint contributions or useful independent reviews. Fresh branch checks and non-forced expected-head updates prevent some publication races; they do not lock remote execution or confer worker authority.

A note saying “leased,” a timestamp, or an expired claim is cooperative information. It is not enforced fencing and does not prove that an earlier worker stopped. Inspect actual task state and reconcile overlapping work. If execution state remains unknown, choose a disjoint safe contribution or preserve the blocker rather than start the same external effect again.

Use stable operation identities and recipient-supported idempotency when available. A timeout may mean an effect happened without its acknowledgement. Inspect the receiver or retained receipt before retrying. Do not automatically repeat an uncertain model invocation or uncertain publication. A known local implementation failure can be diagnosed and followed by a separately identified corrected attempt.

Investigate broken main-branch checks before expanding dependent code. Repeated unproductive units call for a different question, reconciliation, or an unblocked alternative. They do not silently terminate the user's continuing objective or justify constant status churn.

Use available compute and existing authorized services. Record measured resource use when available. Do not infer live workstation utilization from a task label, nor invent numerical spending limits. New infrastructure, material new spending, or broader effects retain their actual authorization requirements.

## Scheduling and evidence of operation

Use one Continuum continuation responsibility. Reuse or update a matching task when one exists; inspect its repository and objective rather than just its title. Existing responsibilities for other projects are not Continuum workers.

Three different observations matter:

| Observation | What it establishes |
|---|---|
| Scheduler confirms an enabled task and schedule | A continuation responsibility was saved |
| A scheduled run has a real execution record | That run started or completed under its recorded conditions |
| Its linked contribution and validation support a useful result | That particular run made verified progress |

A successful manual setup run does not prove unattended execution. A completed scheduled run does not by itself complete the research objective. Review the first unattended result; state failures and missing capabilities precisely.

For local execution, keep the relevant computer reachable and its required application running. Web scheduling does not preserve a local worktree between runs. Reconstruct from the repository rather than relying on a task-container path. Dot can coordinate work on supported connected hosts or configured cloud environments, but a repository message alone cannot wake it.

Favor quiet routine operation while the user sleeps. Preserve material results, then report a concise meaningful progress update or an actionable blocker. Do not repeatedly notify about unchanged administrative state. Notification delivery still follows the application's settings.

## Ready Codex startup prompt

The [complete Codex handoff](../../CODEX_HANDOFF.md) is the authoritative startup prompt for a new implementation task. It includes the mission, implemented core, design reasons, selected next unit, collaboration, validation, and continuation contract. It is an original Continuum adaptation. Saving or pasting the prompt does not by itself change the model setting or install a recurring worker.

Read [Understanding Continuum](../orientation.md) for an explanation of the vision and information architecture before starting, when orientation is useful.

## Current product references

Checked 2026-10-19. These describe product capabilities, not this project's activation state:

- [Scheduled tasks](https://learn.chatgpt.com/docs/automations): recurring task context, connected tools, and local execution requirements.
- [Dot tasks and memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory): separate tasks, follow-up, and configured computer/cloud environments.
- [Dot computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps): cloud and local access are distinct.
- [Chat, Work, and Codex](https://learn.chatgpt.com/docs/use-chatgpt): interface roles.
- [Model selection](https://developers.openai.com/api/docs/guides/model-selection) and [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol): starting guidance, to be evaluated on actual work.
