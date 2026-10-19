# Learn the design by using Continuum

Status: first checkpoint adapter, actual successor review, and [independent CSV requirement handoff](../../research/runs/independent-csv-pilot/README.md) completed; [evidence and limits](../../research/runs/project-checkpoint-pilot-1/README.md). Continuing pilot, not a completed adoption study or workstation deployment. This plan follows the user's 2026-10-19 UTC request to discover design improvements through actual use, and [Claude exchange 7](../collaboration/2026-10-19-claude-07.md).

## Question

Does using Continuum make a real investigation easier to resume and improve, or does maintaining its records consume more effort than it saves? Defect detection is only one part of the answer. Observe missing concepts, awkward interfaces, useful workarounds, abandoned steps, and questions that appear only when another agent tries to continue.

The existing [fresh-model trial](../../research/continuation-trial/README.md) showed one actual continuation from a generated pack. The [release baseline](../../research/runs/release-baseline-2026-10-19/README.md) measured small local operations. Neither establishes ongoing usefulness. This pilot makes the program a tool in real development and preserves what using it teaches us.

## First consumers

1. **Continuum's own development.** Use the current real next unit, its source, decisions, result, and next handoff. This provides authentic work and a public evidence path without enrolling another project's private execution or data.
2. **A small independent public example.** After the first feedback, use a tiny CSV-inspection CLI in a sandbox: well-defined input/output behavior, missing-value cases, tests, one changed requirement, and a handoff. Keep it a sample workload rather than another product platform. Its different vocabulary should expose assumptions that fit Continuum's internal development but not ordinary projects.
3. **Selected Base12 or Prime Radiant work.** Later, choose a bounded useful read or research contribution with the current work owner and existing authorization. Keep private sources and results in their actual private homes. Adoption is incremental; no repository migration is required.

Using Continuum to develop itself may hide friction because its designers know the missing context. The second consumer is a deliberate check on that bias. The first few uses are qualitative observations, not a benchmark of general model quality.

## Where it runs

The current executable runs in the coordinating Chat task's Linux executor. GitHub holds durable public code, documentation, and permitted evidence. A task-local filesystem is not proof of persistence across scheduled runs; each run must reconstruct required inputs or use an actually persistent retained store.

A connected Linux workstation is the preferred next place for a persistent single-user pilot. Use a normal user-level executable and local project data, with no daemon or public server needed initially. Suggested layout:

- A source checkout for development.
- Separate retained build directories named by exact source/build identity.
- A local data directory for each pilot project, outside the source checkout.
- A trial-evidence directory containing input/output manifests, observations, and safe backups.

These are deployment recommendations. No user-workstation installation or running worker is established by this document. The next Codex task should verify its actual host, paths, toolchain, access, and existing task ownership before describing local activation.

## Updating the tool while preserving the investigation

Record the exact source revision, any source changes used, toolchain, build command, executable digest, and the formats supported by the candidate. A source build is legitimate; the important property is identifiable bytes and a repeatable provenance record, rather than relying on a moving branch name.

Keep the software build and project data separate. Run a candidate against a fresh disposable store first. Before a retained store is used across upgrades, add an explicit supported-store-format check and a tested preservation/restore path. The current prototype has versioned object/context formats but does not yet provide a complete installation, migration, and rollback contract.

For SQLite WAL, a live database may have committed content in its WAL file. Copying only the main database file is not a complete live-backup method. Use the SQLite online backup API or another supported consistent-snapshot method; check the result and verify recovery on a separate destination. A cold-copy procedure must establish that writers are stopped and all required state is preserved. See [SQLite's backup documentation](https://www.sqlite.org/backup.html) and [WAL documentation](https://www.sqlite.org/wal.html).

Keep the prior data and binary available when testing an incompatible candidate. Do not silently rewrite retained evidence, delete newer accepted work to roll back software, or overwrite a historical trial. For the initial experiment, a new store beside the old one is a simple way to test a format change. A general migration engine is later work if actual use requires it. Record build identity in the trial manifest now; adding version fields to every core receipt requires an explicit contract change rather than retroactively editing them.

## First useful implementation unit

Create a small repeatable entry point for one real project checkpoint using the existing CLI. It should capture an exact source snapshot, an authored WorkState for the selected real unit, the prepared context and its coverage, and the build/run manifest. Use the existing context example as implementation guidance; do not build a general execution platform.

Run one genuine successor handoff. The receiver gets a declared context package and any permitted links or tools, resumes the selected task, and records what it actually needed. Preserve its input exposure, result, and any extra retrieval. An offered request does not count as a completed handoff. If the original conversation or a broad startup prompt was also visible, record that exposure rather than claiming the pack alone supplied everything.

For this first unit, keep the store disposable unless its upgrade/backup requirements have been implemented and tested. Preserve the bytes and references needed to reconstruct the trial in their appropriate durable home. A digest alone does not retain missing input bytes.

Done means a real successor has continued a useful unit from an identified checkpoint, the evidence is recoverable, and at least the observed friction or usefulness has been recorded. No design improvement needs to be invented if the first use reveals none.

## What to observe beyond defects

| Observation | Design question it can answer |
|---|---|
| The receiver needs a missing fact or source | Is the selection rule or record model omitting something decisive? |
| A large included section is never used | Can the representation become smaller without hiding important constraints? |
| The same question is asked after several handoffs | Should the answer become a durable field or a better retrieval operation? |
| An agent bypasses the CLI or maintains a parallel note | Is the interface inconvenient, or does the native model lack a useful concept? |
| WorkState forces an awkward description | Are the categories aligned with real work? |
| An old negative finding prevents a repeated attempt | What information actually produced the saved effort? |
| Writing and reconciling records rivals doing the task | Which ceremony or duplicate representation should be removed? |
| A current-looking pack still leads to a stale decision | Is freshness being observed at the wrong boundary, or is an evidence dependency missing? |

Track time to a correct next action, extra retrieval, repeated work, omitted decisive facts, and upkeep time when those are actually observable. Distinguish agent-authored estimates from measured durations. Token totals without an applicable billing route do not establish cost. A successful completion can still leave useful design friction.

Use a short note for a substantive observation: checkpoint; task and receiver exposure; what was needed; what was present or missing; actual consequence; proposed change; evidence that would support the change. Start in the existing research records. Build a new native record type only if repeated use shows its value.

## Learning cadence and comparison

Review after the first real handoff and again after a few uses; three handoffs is a useful initial checkpoint, not a statistical sample-size claim or an end to the continuing program. Choose the next change from the observed friction. Keep a result that shows the current design was sufficient, and preserve a result that recommends removing part of it.

The simplest comparison is ordinary `CURRENT.md`, GitHub source, and a concise handoff. A later controlled trial can give comparable fresh workers the same task/evidence with different context preparation, record their full input exposure, and compare recovery and upkeep. Do not treat a richer prompt, a more capable model, extra history, or an easier task as evidence that the storage representation improved performance.

## Emerging possibility: learn from context gaps

Claude proposed recording what a receiver needed but did not have, linked to the exact received pack. This is useful feedback about the context interface. It does not automatically prove that the sender should have included the fact or that a model's complaint is correct. Inspect the actual downstream consequence.

If the same gap repeatedly changes action, it may justify a new field, a retrieval operation, a selection rule, or a different unit of context. That would make the design respond to observed continuation needs. Begin with a few plain records; let experience determine the mechanism.
