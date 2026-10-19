# Fresh Claude continuation of the real project

This records one actual Claude Opus 5.5 call using only a native Continuum context rendering and a short neutral task request. It is an observational trial, with a retrospective coordinator assessment. It is not a controlled comparison, an automatic provider runner, or a claim of general model performance.

## Exact source and exposure

The source snapshot contains all 70 tracked regular files at local Git commit `4fec33bf2cc910fc02b254bc36f9dbe724e78336`, totaling 690,497 source bytes. The [source index](source-index.json) binds each path to its exact raw SHA-256, native Blob identity, and byte count. Native Snapshot v1 retains paths and bytes, not executable file modes. The source commit predates this trial, avoiding a self-reference.

| Item | Identity or scope |
|---|---|
| Native source Snapshot | `sha256:40533f98d5945bee13e1ee83c72fd4c7b1ffa39127a4d5c3fb4ccf74c8f8a0a9` |
| ContextPack | `sha256:788a3edebfeb8a4bc8d2f44c8a425e73983463eaf17d1fee8429518e59e60f0b` |
| Exact model context | [context.jsonl](context.jsonl), 8,321 UTF-8 bytes |
| Selection | All 12 declared records included; no declared record omitted |
| Source exposure | The rendering contains source references. Referenced source files and receipt bytes were not supplied to Claude. |
| Previous conversation | None supplied; the service reports no server memory |
| Request | [claude-04.json](../../docs/collaboration/requests/claude-04.json) |
| Provider metadata and exact returned text | [claude-04-response.json](../runs/claude-04-response.json) |

The supplied record retained an important actual change in user instruction: GitHub had briefly been deferred, then explicitly authorized again after the user returned to the desktop. At capture, account verification was still pending and repository creation had not been dispatched. The source-review counts likewise describe their capture time; later reviews are separate observations. The pack does not pretend to be live state.

The objective, constraints, attempts, decisions, and uncertainties are coordinator-authored. The retained local verification record has its own commands and source hashes. This trial does not promote every authored field into independently established fact.

## Native path exercised

All source files were inserted as exact Blobs, then assembled into the source Snapshot. The [WorkState](work-state.json), its [state Snapshot](state-snapshot.json), and its [acceptance request](accept.json) established a local trial head. The [preparation request](prepare.json) bound the pack to that exact WorkState at generation 1. A new CLI process inspected the rendering and verified its current anchor.

The receiving Claude call had no database, filesystem, browser, or external-effect tools. It returned orientation text and an acknowledgement. The full visible response is retained unedited in the response record and its [readable projection](../../docs/collaboration/2026-10-19-claude-04.md).

Claude wrapped its JSON in a Markdown code fence despite a JSON-only request. The coordinator removed the outer fence and extracted the exact acknowledgement-object substring. The object was not reserialized. Its raw SHA-256 and extraction method are retained in the [assessment](assessment.json). The coordinator submitted those bytes through `acknowledge-handoff` as a proxy, then used another CLI process to run `verify-handoff`.

The native acknowledgement identity is `sha256:e92192b61674445a628011c32ed4f16e826eb3814530eb4b99ec7196bd485685`. The [verification result](acknowledgement-verification.json) reports reference consistency true and recipient authentication, understanding, and external-effect verification false.

## Observed result and retained correction

The response recovered the project objective and reported test boundary, kept the old deferral historical and the latest authorization current, avoided claiming a published repository, and identified the uncertain authentication result. It explicitly acknowledged not having inspected the source or receipt itself.

One next-step detail needs qualification: a fresh local expected-head check does not make a later GitHub action atomic, authorize it at GitHub, or provide external idempotence. The external effect needs its own supported authorization, outcome observation, and reconciliation. This prototype has no external dispatch ledger.

There was one call, without randomization, a blinded control condition, or a statistical estimate. The exact request is retained so its wording and source exposure can be inspected. Future evaluation should compare ordinary narrative handoffs, raw typed facts, and facts with guidance under comparable budgets. The wider [representation experiment](../../docs/architecture/representation-experiment.md) describes those controls.

## Reading and replay boundaries

The JSON inputs, source manifest, accepted-head observation, generated rendering, model response, extracted acknowledgement, and CLI outputs are retained here. The referenced source commit is in the local Git history included with the repository's recoverable archive. A source-only ZIP without that history cannot independently resolve a local commit identifier; use the supplied Git bundle when restoring that archive.

After publication to GitHub, the same exact source tree is also available at public commit `256f37c2f92a0f79da2e1859e9c7e1be64a792a1`. The [publication map](../publication/source-commit-map.json) relates this public commit to the retained local source commit. Their Git tree identities match; their commit metadata and parent links differ. The original trial records have not been rewritten to substitute a later public commit ID.

The repository's [synthetic context example](../../examples/context_handoff.py) provides a turnkey local replay of the same custody and staleness mechanics. Re-executing this Claude call would be a new model sample and potentially a new paid operation. It is not required to inspect or verify the retained records, and it is not performed automatically.
