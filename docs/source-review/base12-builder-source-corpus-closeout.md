# Builder fixture-source corpus closeout

This Research Delta fully reads `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/inputs/02.b12s` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Its 3,614 bytes have Git blob identity `c44a6b71c7fe31fbe3b3e3159ffe1f9c35ae5547` and SHA-256 `1e6b201da0a06933d6dfb5a0194f2813acfce36c1bd6dc76d5a0d2b685c74351`. This chat owns the read-only contribution based on Continuum main `82354c23af60522be69207a29df787654965fb26`. The [additive ledger](base12-coverage-builder-source-corpus-closeout.json) and [validation record](../../research/runs/base12-builder-source-corpus-closeout/validation.json) preserve identities, finite checks and limits.

## Complete vector composition

The complete 312-line source contains all 73 nonrelocating encoding vectors, in their frozen witness order, followed by all 14 concrete relocation vectors. An original literal composition reproduces every source byte, including comments, label names, padding and final LF. No upstream materializer was imported or executed.

Each nonrelocating statement retains its witness spelling. Negative zero and leading-zero immediate spellings therefore remain present instead of being replaced by normalized integers. This complements the earlier numeric-input review: a spelling accepted in one instruction position does not establish acceptance of the same spelling in every other position.

The relocation section assigns each vector a unique bounded label name. Forward cases place padding after their branch, backward cases place padding before it, and self/zero-displacement cases retain their respective target positions. The 122 one-byte padding instructions preserve each original vector's instruction-to-target relation after composition into one source.

All 14 signed displacement fields agree with the renamed labels and the end of the four-byte patch field. These relations are calculated from supplied literal bytes and source positions. They do not depend on invoking a parser, assembler or candidate. The four abstract range witnesses in the relocation specification are not source program cases; this source does not turn unreachable extreme displacements into executable coverage.

## Source, map and saved records

The source has 209 instructions, 15 labels and 14 relocations, producing 224 expected map rows and 538 supplied code bytes. Source length, checksum-list identity, LF/physical-line counts and authored counts all agree with the frozen case manifest. The declared ELF length is 4,634 bytes, consistent with its fixed 4,096-byte prefix plus code-length arithmetic.

An original literal map buffer built from source line numbers, row kinds, file offsets and instruction lengths matches the expected 7,200-byte map digest. Supplied instruction bytes are hashed as a stream; no complete code file or ELF is emitted. Neither a matching map identity nor the streaming digest constitutes acquisition of the saved native output.

The saved successful case status, publication-valid flag, output lengths, modes and hashes agree with the manifest. This is a relation between historical records. No new candidate invocation, syscall trace or output publication occurred here. The encoding source includes control transfers and operations that make its explicit never-execute restriction consequential; encoding completeness supplies no executable-safety evidence.

## Scoped closure and research lesson

All **62 `.b12s` paths / 166,612 path bytes** under this fixture input directory have now been reconciled by pinned-tree identity. Its **61 nonempty paths / 47 distinct nonempty blobs** have full semantic reading or identical-blob credit, including repeated input variants whose contents were read earlier. The remaining empty input15 retains its earlier mechanical classification. This closes the source-text corpus without granting semantic credit to every empty blob elsewhere or claiming that each path has an independently reviewed surrounding execution context.

The transferable lesson is that composition needs its own evidence. Correct isolated vectors can be misjoined through target collisions, padding changes, lost lexical spelling or wrong source-line accounting. Exact whole-source reconstruction and a source-position map check test that join while preserving the distinction between authored expectations and observed execution.

Cumulative semantic reading reaches **578 distinct blobs / 5,039,589 bytes**, plus **79 identical alias paths**. **4,936 paths / 3,851 distinct blobs** still lack full semantic-reading credit. Whole-repository reading remains incomplete, and historical global acquisition overlap remains unresolved. Native fixture files, expected layouts/maps and private raw execution evidence retain their own reading/custody gaps. No model consultation, live scan, workstation activation or upstream recipient acceptance occurred.

Next: fully read `preparation-01/fixtures/expected/02.layout.json`, 27,040 bytes, and join its complete metadata to this source's labels, rows, coverage and patch positions. Reconcile fresh main and ownership first; the owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
