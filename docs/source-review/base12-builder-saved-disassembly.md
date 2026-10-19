# Complete saved builder disassembly

This Research Delta reads all 118,160 bytes of `research/owned-stack/2026-10-16/native-builder-slice/artifact-r2/builder.disassembly.txt` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `5c1828b8a7b243dd440e1c927de8492533468794`. The [ledger](base12-coverage-builder-saved-disassembly.json) binds the exact source; the [validation record](../../research/runs/base12-builder-saved-disassembly/validation.json) records original representation and identity checks.

## Full reading includes the input format

The complete seven-line header and all 1,589 address/byte/decoded-text rows were read, including 572 distinct annotations. A lossless projection preserves every virtual address and byte span alongside an annotation dictionary. Exact reconstruction includes the original tabs, spacing, blank lines and final newline, reproducing the entire source. Length, Git blob and SHA-256 checks bind those bytes to the pinned tree.

The header names a raw code-binary input and says its file format is `binary`. Its displayed `.data` section is therefore not evidence of an ELF section or segment permission. It does not contradict the separate saved readelf record's executable segment, and it cannot replace that record. The display address likewise needs its relation to the declared entry; a printed address alone is not a loader observation.

Every displayed address equals the listing's code offset plus the layout entry. All 1,589 byte spans and boundaries match exactly, covering the same continuous 9,644 bytes. Streaming those saved bytes agrees with the preceding listing's SHA-256 and the pinned `builder.code.bin` Git identity. Full ELF headers, padding and loader behavior remain outside this code-only comparison.

## Operand meaning survives the representation change

An original explicit conversion checks every decoded-text row against the listing's annotation. It handles source/destination order, decimal versus hexadecimal immediates, full-width negative values, register widths, memory displacement spelling, zero-extending byte loads and branch mnemonic aliases. Whitespace normalization is applied only after exact source-text reconstruction has already passed.

This matters beyond spelling. The single 32-bit load decodes to the 32-bit destination register; the single 32-bit store uses its 32-bit source. Flattening both to the surrounding 64-bit register names would lose width information. Similarly, a negative 64-bit immediate's full hexadecimal representation cannot be replaced by a shorter positive value. All these cases agree with the existing finite byte-field checks without rerunning an encoder or disassembler.

Six intentionally changed representations fail comparison: swapped operand order, load width, store width, branch kind, branch target and immediate sign extension. These checks establish that the comparison preserves those distinctions; they are not exhaustive malformed-text or instruction tests.

All 479 saved branch/call targets also agree with their signed byte displacements and layout destinations. This supplies a complete join between the listing's named targets and the external record's numeric targets. It remains a static correspondence between identified records, rather than an observed runtime control-flow trace.

## Syscall decoding loses authored number annotations

The listing has 578 distinct annotations; the saved disassembly has 572. The only many-to-one annotation family is syscall: seven different numbered listing annotations collapse to the same unnumbered decoded mnemonic. All fifteen syscall sites still match the static record and listing addresses.

The number is supplied by the preceding register-setting instruction, rather than an operand encoded in the syscall instruction itself. The prior listing review checked that local sequence. This record correctly preserves the opcode without inventing a number operand. A successor must retain the association between the two instructions if it needs a syscall-number claim; counting or hashing the opcode text alone cannot carry it.

## Evidence strength and remaining work

This is a retained external decoding record that agrees throughout with the listing and code identity. No external disassembler ran during this unit, and the text alone does not authenticate its historical tool invocation or establish behavioral independence. Agreement across two representations is useful for detecting mismatched boundaries, operands or targets while retaining their shared byte dependency.

No upstream source was imported, native artifact emitted or executed, model consulted, live process scanned, workstation worker activated or upstream result accepted. The full ELF and the historical assertion of exactly six R1-to-R2 changed bytes remain separate dependencies.

Semantic reading reaches **531 distinct blobs / 4,635,961 bytes**, plus **77 identical alias paths**. The remaining gap is **4,985 paths / 3,898 distinct blobs**. Historical global acquisition overlap remains unresolved; whole-repository reading remains incomplete.

Next: complete the 75,434-byte `artifact-r1/builder.instructions.txt` and compare both complete saved code representations to test the exclusive six-change claim. Reconcile fresh main and ownership first; no recipient has accepted the next unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
