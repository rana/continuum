# Builder capacity expected layouts

This Research Delta fully reads `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/07.layout.json` and `11.layout.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The two files total 107,982 bytes. This chat owns the read-only contribution based on Continuum main `5eb5f8b2516728f6e6ce511fa7b5b6b832723b74`. The [ledger](base12-coverage-builder-capacity-layouts.json) binds both source identities; the [validation record](../../research/runs/base12-builder-capacity-layouts/validation.json) retains lossless reading projections and actual checks.

## Complete repeated structure

The entire contents were read through explicit lossless projections. Every scalar and empty field remains explicit. Named label sequences, map rows, literal code fields and relocation records are represented by complete bounded formulas, including their order and endpoints. Expanding those representations reproduces every parsed field and the complete JSON bytes, including formatting.

Layout07 is 65,928 bytes, Git blob `f8c4cc845c7275f4c1f9127dff280acd686da037`, SHA-256 `282599d930877f24d37a23e2ab2b84377a80b2a350945c8a767192a69407218f`. Layout11 is 42,054 bytes, Git blob `7e70f1071e5638ec6c47b80708ea7e8493215ba5`, SHA-256 `88573c21e46682f6d345dccecf707eaf30b32756ae4740ee078eb3d3309e76d4`.

Original bounded source compositions also reproduce the previously read inputs exactly. Source hashes, authored counts, checksum-list entries, layout declarations and saved successful case metadata all agree. These relations establish static consistency rather than fresh candidate behavior or resource measurements.

## The map maximum is an aggregate

Layout07 names the entry followed by 127 numbered labels, all at the initial code offset. Its first 128 map rows are zero-length label rows, with physical source lines 1 through 128. The next 1,024 rows are one-byte instructions, whose source lines start at 129 and code offsets increase by one.

The resulting 1,152-row map is exactly the fixed 32-byte header plus 1,152 records of 32 bytes: 36,896 bytes. Its literal-record reconstruction matches the declared digest. The supplied code field consists of 1,024 identical one-byte instruction values; its digest also matches. The declared 5,120-byte ELF length agrees with its fixed prefix plus code length.

The maximum map count therefore comes from instruction and label counts together. Distinct names sharing an address still consume label records. A code-byte count or distinct-address count alone cannot recover map capacity. This confirms the earlier source-boundary finding against every field of the complete expected layout without claiming an observed native allocation or boundary run.

## Repeated statements have changing relative fields

Layout11 contains one entry label and 256 five-byte unconditional branches back to it. Instruction row index `i=0..255` has physical source line `i+2`, file offset `4096+5*i` and length 5. Its patch starts at `4097+5*i`; its signed displacement is `-5*(i+1)`.

Every one of the 256 four-byte little-endian fields agrees with that formula, the named target and the end of its patch field. The values range from −5 through −1,280. Every complete instruction has the same opcode and source statement, while every displacement differs because its position differs. Treating the instruction bytes as one repeated five-byte block would lose the relocation semantics.

The complete code field contains 1,280 bytes. Its 257-row expected map has 8,256 bytes. Both literal identities match; the declared 5,376-byte ELF length also agrees arithmetically. Empty coverage lists remain empty rather than acquiring synthetic witness entries. A looping encoding fixture supplies no evidence that executing it is useful or safe, and no output was run.

## Evidence boundaries and continuation

The lesson is to compress repetition only with a representation that preserves all varying fields. A lossless affine record projection can make a large expectation inspectable while keeping source lines, offsets, label multiplicity and relative patch arithmetic explicit. Exact whole-file reconstruction then checks that the projection omitted no exceptional record.

ELF hashes are copied from the frozen case manifest, not recomputed from unacquired headers/padding. Literal map checks do not acquire raw map files. No upstream module was imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation activated or upstream recipient acceptance obtained.

Semantic reading reaches **594 distinct blobs / 5,193,872 bytes**, plus **94 identical alias paths**. **4,905 paths / 3,835 distinct blobs** still lack full semantic-reading credit. Whole-repository reading and historical global acquisition overlap remain incomplete.

Only `expected/01.layout.json`, 45,963 bytes, remains without full reading or identical-blob credit among this fixture directory's expected layouts. Next: complete that runner layout, join it to the held runner source/migration records, and close the expected-layout corpus within static scope. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
