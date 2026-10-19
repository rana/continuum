# Complete historical builder layout

This Research Delta reads all 53,163 bytes of `research/owned-stack/2026-10-16/native-builder-slice/artifact-r1/builder.layout.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `2590647f149c44c6cba812a0614c4f677e17d9d9`. The [ledger](base12-coverage-builder-historical-layout.json) binds source identity; the [validation record](../../research/runs/base12-builder-historical-layout/validation.json) records the complete metadata and listing joins.

## Full reading and exact revision relation

All eleven top-level fields, 163 labels, 479 relocation entries, 33 globals and seven buffers were read. A lossless projection preserves every address, target, displacement and capacity. Reconstructing the original JSON formatting and final newline reproduces the entire source. Length, Git blob and SHA-256 checks bind those bytes to the pinned tree.

The only top-level field differing from R2 is the declared ELF hash. Replacing that single hash value in the complete R1 text reproduces the complete R2 text byte-for-byte. Thus the equality covers all other nested values and their original textual representation, rather than a sample of totals.

The R1 hash declaration agrees with its own build and static records; R2 agrees with its separate records. Their distinct artifact declarations remain intact. Neither declared ELF hash was freshly computed from an acquired full ELF during this review.

## Both historical maps now bind their own listing

For each revision, all 163 label addresses coincide with starts of rows in its own complete listing. Every one of the 479 relocation records agrees with the corresponding annotated target, file offset and signed byte field in that revision's listing. All displacement equations, field bounds and nonoverlap checks pass. Both code streams again match their respective pinned code-blob identities.

This completes the historical-map dependency left by the previous code comparison, which had checked both listings against the held R2 map. The newly held R1 map has the same labels, targets, offsets and displacement values, and now has its own complete listing join.

The R1 source's literal constants, global-name order and buffer declarations match the layout through an original restricted AST reader. Its eight combined memory intervals agree with both saved static records and remain disjoint within the declared writable region. No upstream function was evaluated. The initial local checker omitted its regex import; that local implementation error was corrected before validation or publication files were written, and the corrected checks passed.

## A fixed map can describe different code

The unchanged layouts coexist with the already verified six changed code displacement bytes. Those changes occur in equal-length argument loads, so they preserve label positions and branch fields. The metadata relation explains the unchanged structural checks without establishing that either revision selects the right arguments at runtime.

This is a useful identity boundary for Continuum: an address map can be shared by artifacts with different code bytes and semantics. Structural equivalence can support reuse of position-based checks, while the artifact digest must remain part of any identity claim. Omitting the hash from a cache key or handoff assertion would erase the distinction this historical correction demonstrates.

That is an evidence-derived design lesson, not a change to Continuum's current object encoding or an observed cache defect. Source semantics, byte identity, historical reported behavior and recipient acceptance retain their separate homes.

## Artifact text coverage and next boundary

All seven R2 artifact text paths now have full reading or established identical-blob credit, totaling 275,947 path bytes. R1 has six of its seven text paths covered; its complete text set totals 275,865 path bytes. The remaining R1 text is the saved disassembly. The four code/ELF artifact paths retain separate binary coverage classes; streaming listed bytes does not add full semantic-reading credit to those paths.

Full ELF headers/padding and the exclusive full-ELF difference remain unverified here. No native artifact was acquired, emitted or executed, upstream module imported, external disassembler run, model consulted, live process scanned, workstation worker activated or upstream result accepted.

Semantic reading reaches **533 distinct blobs / 4,764,558 bytes**, plus **77 identical alias paths**. The remaining gap is **4,983 paths / 3,896 distinct blobs**. Historical global acquisition overlap remains unresolved; whole-repository reading remains incomplete.

Next: complete the 118,158-byte `artifact-r1/builder.disassembly.txt`, compare its saved decoding with the R1 listing and close the two artifact text groups within their explicit limits. Reconcile fresh main and ownership first; no recipient has accepted that unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
