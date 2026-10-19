# Exact builder capacity-boundary inputs

This Research Delta reads inputs05–14 under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/inputs/` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The ten files total 152,328 bytes. This chat owns the read-only contribution, based on Continuum main `d6fdb6f581bf293aa2782248007b304c88592054`. The [ledger](base12-coverage-builder-capacity-inputs.json) binds every source; the [validation record](../../research/runs/base12-builder-capacity-inputs/validation.json) records original finite checks and their limits.

## Complete repeated source structure

Every source was read through a lossless repeated-byte or repeated-line projection. All distinct lines, label names, terminators and repetition counts are explicit. Reconstructing those projections reproduces each complete file. Separate bounded source compositions also reproduce the exact bytes without calling the materializer.

Lengths, Git blob identities, SHA-256 hashes, fixture-list identities, LF counts and physical-line counts agree with the frozen manifest. Authored instruction/label/relocation counts agree throughout, as do all corresponding saved case status/output declarations. Five accepted and five rejected expectations remain specification and metadata relations rather than fresh native tests.

| Pair | Accepted boundary | Rejected neighbor |
| --- | --- | --- |
| 05/06 | 65,536 source bytes | 65,537 source bytes |
| 07/08 | 1,024 instructions | 1,025 instructions |
| 09/10 | 128 labels | 129 labels |
| 11/12 | 256 relocations | 257 relocations |
| 13/14 | 31-byte label token | 32-byte label token |

## Whole-input size differs from token size

Inputs05/06 share a minimal label/instruction prefix followed by an unterminated comment. Their comment bodies contain 65,518 and 65,519 copies of the same printable byte. The second file is exactly the first plus one comment byte. Both have only two LF bytes but three physical lines.

This source shape isolates the whole-input size distinction without creating a long token. Removing comments before checking source size would erase the difference these payloads are meant to test. The original source and frozen notes also qualify the expected rejection: the stable oversized regular file reaches the earlier fstat size check. This pair does not demonstrate the later read overflow-probe path.

That remains a source-derived path explanation. No candidate call or trace was produced here.

## Capacity interactions and first guards

Input07 has 128 unique labels and 1,024 one-byte instructions. Their sum reaches the implied 1,152-row map maximum, producing a declared 36,896-byte map. Input08 adds one instruction while other relevant counts remain within bounds. The source checks instruction capacity before encoding and adding its map row; a hypothetical extra row is not observed parser progress.

Inputs09/10 isolate the label-count endpoint using short unique names and one instruction. Inputs11/12 use repeated backward branches to the entry label, reaching 256/257 relocations while instruction, label, token and input-size counts remain below their own ceilings. Encoding acceptance of the looping source supplies no executable-safety evidence; no such output was run.

Inputs13/14 differ only in a label token's length. The 32-byte token exceeds the lexer limit before the later name validator. These two guards must not be counted as independently exercised runtime paths merely because both express a related bound. The original source order and frozen qualification agree on that limit.

## Expected maps bind actual source structure

Original literal-record reconstruction matches all five accepted expected-map hashes. The maps have 2, 1,152, 129, 257 and 3 rows, respectively. Their byte lengths agree with the fixed header plus 32 bytes per row; declared ELF lengths agree with the authored code-length arithmetic. These are expected-map identity checks, not acquisition of raw maps or new ELF generation.

The transferable lesson is to name the guard actually distinguished by a fixture, preserve the full payload domain before normalization, and keep interacting bounds explicit. Complete source bytes strengthen an earlier case-table review without converting its intended coverage into observed execution coverage.

No upstream module was imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation worker activated or upstream result accepted.

Semantic reading reaches **577 distinct blobs / 5,035,975 bytes**, plus **79 identical alias paths**. The remaining gap is **4,937 paths / 3,852 distinct blobs**. Historical global acquisition overlap remains unresolved; whole-repository reading remains incomplete.

Next: complete `inputs/02.b12s`, 3,614 bytes, and join its complete encoding/relocation-vector source composition to the held witness specifications. It is the only remaining nonempty source path in this fixture input corpus without reading/identical-blob credit; input15 retains its separate mechanical empty-file classification. Reconcile fresh main and ownership first; no recipient has accepted that unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
