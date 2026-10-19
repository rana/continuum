# Complete builder code revision comparison

This Research Delta reads all 75,434 bytes of `research/owned-stack/2026-10-16/native-builder-slice/artifact-r1/builder.instructions.txt` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `aaf15d0dd5176532d394d6989c380461f112d479`. The [ledger](base12-coverage-builder-code-revision-comparison.json) binds the exact source; the [validation record](../../research/runs/base12-builder-code-revision-comparison/validation.json) records the complete comparison.

## Full historical reading, not a selected-row check

All 1,589 R1 rows were read, including every offset, byte span and annotation. A lossless projection reuses the already read R2 annotation dictionary and adds three historical operand spellings. Exact reconstruction reproduces the entire R1 source, including spacing and final newline. Length, Git blob and SHA-256 checks bind those bytes to the pinned tree.

Both complete listings cover 9,644 contiguous code bytes with identical instruction offsets and lengths. The original finite declared-family field reader passes on every row of each revision. Streaming each listing's bytes matches its respective pinned `builder.code.bin` length and Git identity. R1's derived code SHA-256 is `b22d3d5f9b9d811baf414ff644b64786b98f948fc27b450edcd00666cc58daed`; R2 retains `f1ed3e878d6beaba79c9317147ecace63f8bb2e6e9c2ea811a27fd6be2f6dd96`.

Neither native code file was acquired, emitted or executed. These are complete text-derived code-byte comparisons tied to pinned artifact identities, extending the earlier selected R2 witness checks.

## Exactly six code bytes differ

Across the complete code spans, six bytes differ. Each is the final displacement byte of a four-byte load, and each increases by eight. All 1,583 other rows are identical in bytes and annotation. No instruction boundary moves, and every one of the 479 branch/call fields remains identical and agrees with the already held R2 address map.

| Changed code-byte offset | R1 displacement | R2 displacement |
| --- | --- | --- |
| 92 | 8 | 16 |
| 108 | 16 | 24 |
| 124 | 24 | 32 |
| 140 | 16 | 24 |
| 148 | 24 | 32 |
| 163 | 8 | 16 |

All offsets are decimal code offsets. Adding the fixed 4,096-byte code prefix gives exactly the six file offsets in the earlier saved full-ELF difference declaration. The corresponding R2 instruction rows also match all six expected/observed correction witnesses. Thus the six selected corrections are now confirmed as the only differences within the complete identified code spans.

All changed fields precede the first syscall site. That locates the correction in argument preparation rather than changing syscall opcodes or later parser/publication code. It does not by itself establish what happened during any invocation.

## Source and byte changes now connect

The earlier complete source AST comparison isolated three expanded validation-loop loads and three scalar argument loads, plus a separate source-snapshot write in the bootstrap's main function. The six expanded native load sites agree with the complete code comparison. The snapshot write is a bootstrap publication change; it is not an extra native code-byte change.

Both revisions' saved structural checks had the same instruction/patch counts, syscall inventory and buffer observations despite the argument-offset defect. The complete code comparison explains how: six equal-width displacement changes preserve those structural properties. Their unchanged structural PASS verdicts cannot establish correct argument selection. This remains a static explanation tied to source and bytes, not a newly observed R1 failure or R2 execution result.

## The exclusive result has a code boundary

The historical record calls these the only R1-to-R2 ELF changes. The new evidence verifies that statement for the complete 9,644-byte code spans and agrees at the six declared file offsets. The full ELF headers and padding remain unacquired, so this unit does not newly verify exclusivity across all 13,740 ELF bytes. Identical saved readelf fields and unchanged packaging source support narrower metadata/source relations; they do not provide missing byte custody.

For Continuum, the useful progression is from selected witnesses to a complete, identity-bound comparison with an explicit domain. A complete code difference is stronger than six matching examples, while its domain still matters. Preserving that boundary lets a successor reuse the result without silently broadening it to an unexamined container or to runtime correctness.

No upstream source was imported, native artifact emitted or executed, external disassembler run, model consulted, live process scanned, workstation worker activated or upstream result accepted.

Semantic reading reaches **532 distinct blobs / 4,711,395 bytes**, plus **77 identical alias paths**. The remaining gap is **4,984 paths / 3,897 distinct blobs**. Historical global acquisition overlap remains unresolved; whole-repository reading remains incomplete.

Next: complete the 53,163-byte `artifact-r1/builder.layout.json` and join its historical metadata to the source, both listings and R2 layout. Reconcile fresh main and ownership first; no recipient has accepted that next unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
