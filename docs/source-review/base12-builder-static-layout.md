# Complete static builder layout

This Research Delta reads all 53,163 bytes of `research/owned-stack/2026-10-16/native-builder-slice/artifact-r2/builder.layout.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `a18549a95ec6f6a8632bff0581efb2be64596d87`. The [ledger](base12-coverage-builder-static-layout.json) retains exact source identity; the [validation record](../../research/runs/base12-builder-static-layout/validation.json) records original arithmetic and metadata comparisons.

## Every layout field is included

The complete reading covers eleven top-level fields, 163 named labels, 479 relocation entries, 33 globals and seven buffers. A lossless projection preserves every name, address, file offset, target and displacement. Reconstructing the original JSON formatting and final newline reproduces the exact source bytes; length, Git blob and SHA-256 checks bind them to the pinned tree.

The layout declares 9,644 code bytes, a 13,740-byte ELF and 1,589 emitted instructions. The ELF length is exactly the fixed 4,096-byte prefix plus code. Entry, writable base and owned writable length agree with the held source constants. The build and static records agree with the ELF digest, length, memory size and instruction/patch counts. The later saved review also names the same candidate digest. These are consistent declarations; the candidate binary remains unacquired, and this unit does not independently count decoded instructions.

## Relocations have a complete arithmetic check

For every patch, the declared displacement equals target virtual address minus the virtual address immediately after its four-byte field. File offsets convert through the declared executable base. Every target exists, every target lies within the declared code span, every field lies within the file's code span, all fields are distinct and nonoverlapping, and every displacement fits signed 32 bits.

There are 375 positive, 102 negative and two zero displacements, ranging from −7,250 to 7,601. The entries reference 162 distinct labels. All 163 label addresses are distinct, ordered and within the declared code region; the entry label equals the entry address. Zero displacement is a valid relation when a target starts immediately after the field. These counts describe saved static relationships rather than executed branch outcomes.

The important remaining dependency is instruction context. A correct four-byte displacement formula does not establish that the field follows the right opcode, occupies an instruction boundary, or actually contains the declared bytes. The saved instruction listing is the next bounded source for those checks. This unit neither imports the encoder nor emits a replacement binary to manufacture agreement.

## Source declarations and writable intervals agree

An original restricted AST reader extracts only literal constants, integer addition/multiplication, tuple declarations and the literal global-name string from the already read bootstrap. It does not evaluate upstream functions. The resulting constants and eight-byte global offsets match the layout: 33 globals occupy 264 bytes. All seven buffer start/length pairs also match the source declarations and the earlier static interval record.

The eight combined intervals are ordered, disjoint and contained within the declared 155,648-byte writable region. They account for 137,785 bytes, leaving 17,863 bytes between intervals or after the last one. This is layout slack, not measured free memory or a whole-process resource bound. It excludes separate stack/kernel/loader effects and proves no runtime occupancy claim.

The capacities retain their concrete purposes: four 32-byte token cells, the input limit plus one probe byte, a fixed output buffer, a map header plus up to 1,152 rows, 128 label records and 256 relocation records. The map row capacity combines the instruction and label bounds. The builder's own writable base and size remain separate from the smaller writable segment it constructs for consumer outputs.

## Transfer and remaining scope

A handoff can carry a complete, internally consistent address map while still lacking evidence that the named artifact contains those bytes. Keeping a metadata-relation verdict separate from byte custody lets a successor reuse the arithmetic work without inheriting an unsupported binary-verification claim. Memory slack likewise needs its stated scope before it becomes a resource claim.

No upstream source was imported, builder called, native artifact emitted or executed, model consulted, live process scanned, workstation worker activated or upstream result accepted. The historical build-only and later execution reports retain their respective capture-time meanings.

Semantic reading now reaches **529 distinct blobs / 4,442,365 bytes**, plus **77 identical alias paths**. The remaining gap is **4,987 paths / 3,900 distinct blobs**. Historical global acquisition overlap remains unresolved, and whole-repository reading remains incomplete.

Next: complete the 75,436-byte `artifact-r2/builder.instructions.txt` and join instruction boundaries and saved bytes to this layout without execution. Reconcile fresh main and ownership first; no recipient has accepted the next unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
