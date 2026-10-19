# Builder revision source and saved structural checks

This Research Delta reads four complete texts / 30,443 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution, based on main `084f16fbb68ce03c3842eaa0d6c837c283012721`. Selected files under `research/owned-stack/2026-10-16/native-builder-slice/` are the R1 bootstrap snapshot, both `STATIC_CHECK.json` files and R2 `builder.readelf.txt`. The [ledger](base12-coverage-builder-revision-static.json) retains exact identities; the [validation record](../../research/runs/base12-builder-revision-static/validation.json) records source comparison and saved-metadata checks.

## Source correction and source custody are separate changes

The earlier bootstrap snapshot was read in full, then both revisions were syntax-parsed without import or evaluation. Only two top-level functions differ in their AST: builder construction and artifact publication. The builder's validation loop moves from initial-stack offsets 8/16/24 to 16/24/32. Three scalar loads also advance by eight bytes: ELF path, map path and input path. The loop expands to three loads, making six corrected argument-load sites in total.

This is the recorded CLI defect: the earlier layout starts from the program-name slot where the three input/output arguments should begin. R2 changes the selected slots. Source agreement with the intended argument positions is now directly checked. The claimed six changed native displacement bytes remain a binary-level prediction here because neither candidate ELF was acquired or diffed.

R2 also adds a write of its own source into the artifact directory. That publication statement is outside native builder construction. Removing it and applying only the specified offset corrections to the R1 AST makes all remaining AST structure equal, including packaging and the encoder class. The R1 snapshot's presence therefore does not imply that R1's own publication routine wrote it; its routine lacks the later snapshot-write line. Exact saved bytes and a capture mechanism's behavior are distinct evidence.

An initial comparison helper matched every loop with the same three literal offsets, accidentally including unrelated mandatory-label key padding. The equality assertion stopped. Restricting the transformation to the path-validation role produced the exact comparison above; no upstream file was changed. The retained correction illustrates why matching constants without their use context is insufficient.

## Both structural checks passed

The saved static-check records differ only in bootstrap and ELF digest fields, which bind their corresponding build-record declarations. The R1 source and held R2 source verify their bootstrap pins. Both records report 1,589 instructions, 479 internal patches, 13,740 ELF bytes and 155,648 owned writable bytes. Both report structural PASS despite the R1 argument defect.

All fifteen saved syscall-site addresses and their seven syscall numbers agree between revisions and with the earlier R2 observation record. Addresses lie inside the declared code interval. Eight buffer intervals are ordered, nonoverlapping and fit the declared writable segment; their names and endpoints also agree with the retained observation record. The source's import list matches the saved imports. These are fresh consistency checks of source and saved metadata, without executing the inspector, external tools or emitted code.

The concrete negative finding is narrower than a general rejection of static checking: instruction-boundary, layout and syscall-inventory agreement did not distinguish this CLI semantic defect. Exact source/control-flow review supplied the missing question. The records themselves explicitly disclaim behavior proof.

## Saved ELF structure is shared across revisions

The readelf text describes an ELF64 little-endian x86-64 executable with entry `0x401000`, three program headers and no section headers. Its RX load occupies 13,740 file/memory bytes at `0x400000`; its separate RW load has zero file bytes and 155,648 memory bytes at `0x420000`. The GNU stack entry is RW. The declared load intervals do not overlap, and the sizes reconcile with the build/static records.

The R1 and R2 readelf paths have the same pinned Git blob. This earns identical-content alias credit for the other path. It also demonstrates a limit: identical header/program-header text can accompany differing source and code identities. It is neither an independent second observation nor evidence that the correction left code unchanged. No actual ELF header, disassembly payload or executable mapping was inspected afresh in this unit.

The source's package builder and these saved fields agree on the declared layout. That remains distinct from running the packager or observing the runtime loader. Historical emitted-only/PASS status does not establish current worker state or rule out later recorded execution.

## Research return and next unit

Keep the correction's levels explicit: intended argument slots, source AST changes, predicted encoded-field changes, actual binary difference and observed invocation. The present return establishes the source comparison and consistency of saved structural metadata. It adds no native execution or compiler-trust result.

Coverage reaches **502 distinct blobs / 3,835,991 bytes**, plus **77 identical alias paths**. The remaining full-reading gap is **5,014 paths / 3,927 distinct blobs**. Global historical acquisition overlap remains unresolved.

Next: preparation README, preparation/provenance JSON, review request and control review, five texts / 20,587 bytes. Read the transition from the source-only checkpoint to a proposed concrete batch before interpreting later results. The already-read case matrix and envelope keep their existing coverage rather than receiving duplicate credit. Reconcile fresh main and worker ownership first; no recipient has accepted the next unit. Separate storage, dispatch-reconciliation and public checkpoint lanes retain their ownership.
