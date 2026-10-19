# Source review checkpoints

This directory records what was actually inspected while designing Continuum. It preserves the remaining reading task alongside the completed work. A source review, a byte-identity check, a saved experimental result, and a fresh execution are different kinds of evidence.

The architecture lessons are in [research-lessons.md](../research-lessons.md). The [initial Base12 ledger](base12-coverage.json) preserves the original 88-file checkpoint; the [extended cumulative ledger](base12-coverage-extended.json) records 161 directly read distinct blobs. They contain aggregate coverage, reviewed source paths, content identities, byte counts, and review status. The complete private-tree inventory is retained separately; it is not needed in the public implementation.

## Latest additive checkpoint

The [stage-A static-review return](base12-stage-a-static-review.md) fully reads five files / 39,483 bytes and recomputes coefficient bounds without execution. Cumulative semantic coverage is **245 distinct blobs / 1,658,584 bytes**, plus **49 byte-identical alias paths**. The [latest ledger](base12-coverage-stage-a-static-review.json) retains identities and the remaining **5,299 paths / 4,184 distinct blobs**. It preserves scoped-proof assumptions and distinguishes deterministic production from unique accepted bytes. Payload validation remains partial. The earlier acquisition aggregate remains historical because its full private overlap index was not recovered.

Preceding additive reviews remain dated checkpoints: [stage-A result](base12-stage-a-result.md) reached 240 blobs, [stage-A launcher](base12-stage-a-launcher.md) reached 237, [stage-A receipts](base12-stage-a-execution.md) reached 230, [stage-A records](base12-stage-a-records.md) reached 224, [stage-A source](base12-stage-a-codec.md) reached 215, [corpus-preservation](base12-corpus-preservation.md) reached 208, [next-experiments](base12-next-experiments.md) reached 201, [alignment-pilot](base12-alignment-pilot.md) reached 196, [learning-performance](base12-learning-performance.md) reached 185, [signal-readiness](base12-signal-readiness.md) reached 182, [native-boundary](base12-native-reset.md) reached 177, and [decision-gate](base12-decision-gate.md) reached 171. Their source scopes, checks and limitations remain in those reports.

## Later completed review groups

The [rounded-operation and native-launch follow-up](base12-followup.md) adds 47 new semantic readings; the [immediate native research-loop review](base12-research-loop.md) adds 26. Together with the initial 88, this gives 161 distinct fully read blobs, totaling 1,226,434 bytes. Another 46 paths contain byte-identical content. Exact local acquisition now covers 539 paths, 530 distinct blobs, and 4,536,603 bytes across paths. These cumulative counts were reconciled against the pinned tree and local byte identities.

The remaining 5,386 paths, representing 4,268 distinct blobs, have no complete semantic-review claim. The generated 144,160-byte native static inventory received full mechanical relation checks, which remain separate from semantic reading. Source reading, binary inspection, numerical evidence interpretation, and reproduction are still distinct tasks.

The [Prime follow-up](prime-followup.md) records complete reading of all eight retained dialogue captures, eight associated receipts, and three prose reports. The [subsequent audit](prime-audits.md) completes the authored source audits, preparatory contracts, all 159 source-inventory records, and the historical automation receipt. Latest mutually exclusive kit coverage is 86 complete semantic readings, seven complete source diffs, two separately classified generated-manifest checks, and 98 remaining numerical, visual, or binary files. The live checkout remains unavailable.

## Initial checkpoint retained below

The following counts describe the original checkpoint, not the later cumulative review. They remain useful for reconstructing how coverage advanced.

## Base12 at the pinned commit

The checkpoint uses commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The complete recursive tree response was not truncated. Review date: October 19, 2026.

| Evidence | File paths | Distinct Git blobs | Bytes across file paths |
| --- | ---: | ---: | ---: |
| Complete tree inventory | 5,593 | 4,429 | 180,332,790 |
| Source/document filename heuristic | 1,587 | 1,404 | 14,201,063 |
| Exact local acquisition, verified against Git blob identity | 477 | 476 | 4,100,899 |
| Complete text directly read by a reviewer | 88 | 88 | 876,422 |
| Additional paths with the same blob as a directly read file | 35 | 12 | 319,090 |

The inventory contains 1,164 repeated blob occurrences. Counting each distinct blob once gives 175,097,688 bytes for the repository and 12,371,893 bytes for the source/document heuristic. That heuristic selects common documentation and source extensions. It does not establish human authorship: generated fixtures and frozen source copies can match, while other file formats are excluded.

Direct reading covered governance and continuity; the research map; the transparent reference interpreter, encoding and cost accounting, and tests; acquisition, structural and history experiment protocols and results; transfer, operator witness, restart and validation-risk protocols and implementations; and selected compiler, assembler, bootstrap, runtime and GPU compiler sources. The ledger identifies each actual path. Three governance/collaboration files were read completely through the source connector without retaining a local byte-verified copy; the ledger keeps those two statuses separate.

The 35 matching alternate paths are content-equivalent to directly read files. Their surrounding directory context was inventoried, and they are not counted as 35 additional semantic readings. No completeness is inferred from a directory name, a README, or a link to another file.

## Programmatic inspection

All 477 exact local files were read as bytes and verified against the pinned Git blob SHA-1 and byte count. Their SHA-256 identities were also recorded. The non-executing structural pass parsed 160 Python files into syntax trees, scanned headings throughout 276 Markdown files, and checked 41 other UTF-8 source files. These operations describe full-file mechanical inspection; they do not imply that a reviewer understood every function or claim.

Two deliberately malformed parser-fixture files did not survive the connector's byte transport faithfully. Their local copies failed the pinned Git hash check and are excluded from exact acquisition counts. They remain explicitly marked as transport mismatches. No repository source was imported or executed during this review, and no original experiment or benchmark was rerun.

## Work still open

**The requested full Base12 repository reading is incomplete.** Beyond directly read content and its byte-identical aliases, 5,470 paths representing 4,341 distinct blobs have no full semantic review claim in this checkpoint. Most generated JSON/JSONL evidence, arrays, executables and compressed material were inventoried rather than downloaded and interpreted. Significant source and documentation also remains unread. A complete audit would need continued source reading, declared treatment of generated material, and a byte-faithful acquisition route for the malformed fixtures.

Prime Radiant has a different access boundary: the accessible fourth-edition research kit was reviewed and all 193 archive entries were integrity checked, but an accessible live repository was not found. [Research lessons](../research-lessons.md#prime-radiant) records the exact kit identity, substantive reading, mechanical checks and remaining limits. The live-repository request remains open.

The ledger is a dated checkpoint. Later reviews should add a new provenance-bearing checkpoint or update its review date and actual statuses. Hash equality establishes byte identity; semantic reading establishes inspection coverage. Neither alone establishes correctness, execution authority, an independent observation, or a performance result.
