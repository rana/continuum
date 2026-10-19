# Source review checkpoint

This directory records what was actually inspected while designing Continuum. It preserves the remaining reading task alongside the completed work. A source review, a byte-identity check, a saved experimental result, and a fresh execution are different kinds of evidence.

The architecture lessons are in [research-lessons.md](../research-lessons.md). The detailed [Base12 coverage ledger](base12-coverage.json) contains aggregate coverage and metadata for the 88 directly read files. It contains source paths, content identities, byte counts, and review status. The complete private-tree inventory is retained separately; it is not needed in the public implementation.

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
