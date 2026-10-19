# Builder all-vector expected layout

This Research Delta fully reads `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/02.layout.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The 27,040-byte file has Git blob identity `1b723a61c5c0cf66422c4e1e79f1cd3f4f6f7efe` and SHA-256 `b9b10e0df79aa2be567e8d4f6c531acb8fdef2630b47e148bbeb4d5508432348`. This chat owns the read-only contribution based on Continuum main `7dc25450660260080bc44fcc86d52e89933f8e70`. The [ledger](base12-coverage-builder-vector-layout.json) and [validation record](../../research/runs/base12-builder-vector-layout/validation.json) retain source identity and exact observed checks.

## Complete metadata joins

The entire JSON was read, including all 13 top-level fields, 224 map rows, 15 named labels, 14 relocation records, 87 witness-coverage entries and the complete literal code field. An original reconstruction using the [fully read source composition](base12-builder-source-corpus-closeout.md), held vector literals and frozen manifest metadata reproduces the entire file byte for byte. That includes field order and formatting rather than merely equal parsed values.

Every map row agrees on kind, physical source line, file offset and length. The rows preserve strictly increasing source lines while allowing equal file offsets for zero-length label rows. Their instruction lengths sum to 538 supplied code bytes across 209 instructions. The corresponding literal map buffer matches the declared 7,200-byte map identity without acquiring or writing the raw expected map file.

Every coverage entry binds its witness identifier, source line, file offset and literal instruction bytes. The 73 nonrelocating entries and 14 concrete relocation entries cover the selected witnesses; padding instructions contribute map rows and code bytes without acquiring invented witness identities. Streaming the supplied code literals reproduces the declared code digest. This checks the complete embedded field, not custody of an upstream standalone code artifact.

## Address equality and endpoint semantics

All 14 four-byte displacement fields lie wholly inside exactly one instruction row. Their signed values agree both with the literal field bytes and with target offset minus the end of the patch field. Ten displacements are forward, three backward and one zero. Named target identity remains part of the check rather than being replaced by an address alone.

Two distinct labels share one offset: the preceding forward-call target and the following backward-branch anchor occupy the same boundary. This is consistent with the complete source, whose separate label declarations consume no code bytes. Uniqueness of names does not require uniqueness of addresses, and a checker that rejected all shared label addresses would reject valid authored structure.

The final zero-displacement conditional branch targets a label exactly at code end. The source contract permits that position. Structural acceptance and correct displacement arithmetic therefore do not imply that taking the branch leads to an executable instruction. This distinction matters especially for an encoding witness explicitly designated never to execute.

## Evidence limits and lesson

The declared 4,634-byte ELF length agrees with the fixed prefix plus code length. Its digest is copied from the already held case manifest; it was not recomputed from unacquired ELF headers and padding. Complete reconstruction of the expectation JSON does not independently authenticate its ELF declaration. Saved successful status/output metadata remain historical relations, as recorded in the preceding source review.

Two draft checker assertions were corrected before producing the retained record: relocation key order for exact serialization, and a top-level field count of 13. Parsed structure already agreed at the first serialization failure. The final reconstruction and all field joins pass; these repairs are recorded rather than presented as upstream failures.

The transferable lesson is to preserve several kinds of identity simultaneously: label names, shared offsets, source positions, literal bytes and artifact declarations. Collapsing any one into another can reject legitimate source structure or overstate what a metadata check established. Source-derived reconstruction is useful consistency evidence, with correlated authored inputs and explicit runtime limits.

No upstream module was imported, materializer/candidate executed, native artifact emitted, raw map/ELF acquired, model consulted, live process scanned, workstation worker activated or upstream recipient acceptance obtained.

Semantic reading reaches **579 distinct blobs / 5,066,629 bytes**, plus **79 identical alias paths**. **4,935 paths / 3,850 distinct blobs** still lack full semantic-reading credit. Historical global acquisition overlap and whole-repository reading remain incomplete.

Next: fully read fourteen small expected layouts for inputs03/04/05/09/13/31/32/33/35/37/39/41/43/45, totaling 19,952 bytes, and join their complete metadata to held source and witness data. The larger runner/capacity layouts and remaining identical layout paths retain separate gaps. Reconcile fresh main and ownership first; the owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted the next unit.
