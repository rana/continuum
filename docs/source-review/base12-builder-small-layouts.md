# Builder small expected layouts

This Research Delta fully reads fourteen files under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/`: layouts03/04/05/09/13/31/32/33/35/37/39/41/43/45. They total 19,952 path bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution based on Continuum main `307fc2e82e664412f77ba6b58c8c2bd723c5fc1d`. The [ledger](base12-coverage-builder-small-layouts.json) pins every selected path and repeat; the [validation record](../../research/runs/base12-builder-small-layouts/validation.json) preserves actual finite checks and evidence limits.

## Every field joins its source

All thirteen top-level fields in each complete layout reconstruct byte for byte, including formatting and key order. Original source-position accounting supplies instruction and label rows; held tiny-program witnesses, endpoint literals and simple fixed instruction fields supply expected code. The tiny source inputs are recovered through previously held byte-identical witness sources, without claiming fresh acquisition of those fixture paths.

Every map row agrees on physical source line, kind, file offset and length. Counts, named labels, code lengths/digests, empty coverage lists and all map lengths/digests agree. The two richer relocation records in layout04 retain source lines, target names and offsets, signed displacement and patch hex; both patch fields fit the source instruction and match the supplied literal bytes.

All fourteen case-manifest references agree on layout hash and length. Their saved successful status, publication flag and ELF/map metadata also agree with frozen expectations. These are complete metadata and literal-field checks. No upstream materializer, native parser or candidate ran, and no raw map or ELF was acquired or emitted. ELF digests remain manifest declarations rather than recomputed native artifact identities.

## Equal result metadata, different source conditions

Layouts05 and32 are the same complete 691-byte blob. Their source files differ: one reaches the whole-input byte ceiling using a long comment; the other omits its final LF. Their executable statement and relevant map positions coincide, so the expected result metadata does too. Normalizing away those distinct source conditions would lose the reason the two fixtures exist.

The fourteen fully read paths therefore contribute **thirteen new distinct blobs / 19,261 bytes**, with one separately recorded repeat. Coverage accounting does not add the shared blob twice.

Layouts05,09,13 and32 share one supplied code identity while describing different label/map structure. Layout09 places 128 distinct label names at the same code offset, followed by one instruction. Layout13 similarly preserves the longest permitted name as its own zero-length label row. Label capacity is a count of names and records, not a count of distinct instruction addresses.

Conversely, layouts31/33/35 have one expected-map identity and three code identities; layouts37/39 form another such map pair, and41/43/45 another triple. Identical source-position structure does not identify instruction contents. These complete layouts substantiate the earlier endpoint-map finding with every metadata field now read.

## Identical layouts across fault contexts

Fourteen additional expected-layout paths for cases49/50/53–64 share the complete layout03 blob. Pinned tree identities and each case's layout declaration agree. Together with layout32, these add fifteen alias paths to the cumulative reading ledger; they do not create fifteen new distinct semantic blobs.

That content equality does not equate the surrounding cases' runtime setup, expected exit status or publication outcome. Several fault cases retain the hypothetical complete source layout despite expecting absent, partial or invalid outputs. Full source-layout metadata must not be mistaken for observed parser progress or a successful publication. The saved manifest and earlier case review retain those distinctions; this unit submits no new fault run.

The transferable lesson is that source, expected result, map shape, code content and runtime case are separate identities. Deduplicate byte content for custody/reading accounting while keeping the source conditions and case outcomes that give it meaning. The same layout can be correct in several contexts without demonstrating the same behavior in each.

No model consultation, live process scan, workstation activation or upstream recipient acceptance occurred. Semantic reading reaches **592 distinct blobs / 5,085,890 bytes**, plus **94 identical alias paths**. **4,907 paths / 3,837 distinct blobs** retain full-reading gaps. Historical global acquisition overlap and whole-repository reading remain incomplete.

Next: complete the two capacity layouts07/11, totaling 107,982 bytes, using complete lossless repeated-structure reading and source-position/patch joins. The runner layout01 remains separate. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that unit.
