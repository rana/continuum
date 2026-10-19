# Recovered Chat first-use evidence — 2026-10-19 UTC

## Research Delta and scope

Rana explicitly requested recording this chat's work in Git so Codex can recover it without the user carrying messages. This contribution preserves the previously attachment-only source comparison and its report, reruns its actual checks, and reconciles the older handoff against fresh public main. Recovery started at `6f2a11465bc610276495de636c85071e2424d1c9`; the publication precondition then detected main advancing to `7c35f9a0de7d17bec539ae1508aef72cffb16240`. The contribution was rebuilt on that newer tree without changing the concurrent work. The current Chat session owns this evidence-recovery contribution only. No implementation worker was dispatched or acknowledged, and live desktop worker activity was not established by this session.

The input archive is `Continuum_First_Use_Pilot_Research_2026-10-19.zip`. Its three text members are preserved byte-for-byte here: [original report](original-research-delta.md), [experimental comparator](examples/verify_checkpoint_sources.py), and [original five tests](tests/test_checkpoint_source_comparison.py). [Verification](verification.json) records the archive digest, exact member digests, path mapping, executor, command, and original stdout/stderr from this new execution. Its remote-base field records the initial observation, not the later publication parent. The separately attached report matched the archive member exactly. No private upstream source or operational state is included.

## Reconciliation: the older next action is superseded

The old report began at `3d15a37fa7faeb53dde9f7ad517c72d99b9b771b`. Its exploratory branch still points to `1fe2e359b63c7289fa4f99698e165c836adc6582`; that example's native execution was not verified by this chat. Do not merge it over the newer maintained adapter.

Fresh remote recovery found merged [PR #1](https://github.com/rana/continuum/pull/1) and [PR #2](https://github.com/rana/continuum/pull/2), rather than an unfinished first checkpoint. The authoritative successors are the [first project-checkpoint pilot](../project-checkpoint-pilot-1/README.md), [independent CSV pilot](../independent-csv-pilot/README.md), and [maintained adapter contract](../../../docs/operations/project-checkpoint.md). They retain actual model requests/replies and executor evidence; the CSV [visible implementation reply](../independent-csv-pilot/implementation-response.json) was inspected during this recovery. Those pilot results were not independently rerun here. Neither pilot establishes a completed adoption study or comparative benefit over GitHub and notes.

At entry, CURRENT selected minimal object-closure import. During publication, merged [PR #3](https://github.com/rana/continuum/pull/3) completed that unit, and [CURRENT.md](../../../CURRENT.md) selected a real fresh-receiver continuation using its resulting context with bounded retrieval of referenced Blobs. That is newer work, not a result produced by this evidence recovery. The remote comparison showed disjoint changes, including that import and a storage research contribution. This publication preserves all of them and leaves CURRENT, native code, maintained tools, workflows and schedules unchanged. The old report's next action is historical, not another task to launch. CURRENT remains authoritative over dated startup prose.

## Finding retained, experiment kept separate

Native current-anchor verification observes the accepted SQLite head; it does not establish that a live Git checkout or upstream branch still has the same source. A context rendering can also reference source without supplying its bytes. The maintained adapter explicitly documents both boundaries. This recovery preserves the earlier independent investigation without presenting it as a new defect in that contract.

The recovered comparator only accepts the exploratory `continuum.real_checkpoint_observation.v1` report. The current adapter instead emits `continuum.project_checkpoint.v1`, with source files nested under `source.files`. The old comparator is therefore **historical experiment code, not a supported validator for the current adapter**. It compares selected file bytes only, not native objects, trust, Git tree identity, complete checkout equivalence, or receipt validity. It is not hardened against concurrent hostile filesystem mutation.

## Verification and negative findings

From this directory:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

All five original tests passed in the current task's Linux container on Python 3.13.5: matching bytes, changed bytes, symlink refusal, parent traversal rejection, and duplicate-path rejection. These use synthetic reports; no Rust CLI or recipient continuation was run. This local test result is distinct from any hosted CI result on the publication PR.

The attachment ZIP was flat, while the test file expects a sibling `examples/` directory above its `tests/` directory. Restoring that layout makes the original tests runnable without editing their bytes. A direct Git clone in this container failed because `github.com` could not be resolved. The connected GitHub route successfully read the repository and created this scoped branch; that is not a missing user authorization.

The original report summarizes an earlier Claude consultation, but neither its actual request nor its response/returned metadata exists in the recovered attachments. That provenance gap remains explicit; the summary cannot substitute for those artifacts or borrow provenance from the separate successor trials. No new Claude call was needed merely to publish historical evidence.

## Next action and ownership

This Chat session integrates this scoped publication using fresh remote-head checks and non-forced writes. The next active implementation owner should recover fresh CURRENT and existing worker activity before continuing the recorded-attempt receiver trial selected at the latest observed main. No acceptance is inferred from a branch, PR, schedule, or elapsed lease. GitHub provides the recoverable evidence, but this record does not wake Codex or establish that Codex has read it. No scheduler or other project's responsibilities were changed.
