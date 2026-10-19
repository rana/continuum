# Complete saved builder instruction listing

This Research Delta reads all 75,436 bytes of `research/owned-stack/2026-10-16/native-builder-slice/artifact-r2/builder.instructions.txt` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution, based on Continuum main `005cfb654605cd2efa7ef1df50d8be751f499b0b`. The [ledger](base12-coverage-builder-instruction-listing.json) binds source identity; the [validation record](../../research/runs/base12-builder-instruction-listing/validation.json) records the original finite byte-field checks and their limits.

## Full reading and continuous byte coverage

All 1,589 rows were read, including offsets, hex bytes and all 578 distinct annotations. A lossless projection retains repeated annotations by dictionary index; reconstructing the original line format and final newline reproduces the exact complete text. Length, Git blob and SHA-256 checks bind it to the pinned tree.

The listing starts at code offset zero and has no gap or overlap: each row starts immediately after the preceding row's bytes. Every row is between one and fifteen bytes. The final row ends at 9,644 bytes, matching the layout's code span; the row count matches its declared instruction count. All 163 layout labels resolve to row starts, strengthening the previous address-range check into a saved-listing boundary check.

Streaming the listed byte fields through a Git-blob hash yields `1914a0c1346316de7439349d4d0b36b68c590b86`, exactly the pinned tree identity of `builder.code.bin`. The derived code SHA-256 is `f1ed3e878d6beaba79c9317147ecace63f8bb2e6e9c2ea811a27fd6be2f6dd96`. No binary file was acquired or emitted: these identities derive from the held textual byte fields. This ties the listing to the identified code artifact under the pinned hash, while leaving the complete ELF and its header/padding outside fresh byte verification.

## Instruction fields and every relocation agree

An original finite field reader checks the listing's declared instruction families against their byte fields: fixed instructions, immediate moves, register operands, memory width/base/displacement fields, register arithmetic, immediate groups, shifts, unary forms, direct calls and conditional/unconditional branches. It checks full field consumption and the memory forms' displacement/SIB structure. This is a bounded consistency checker for these saved families, not a general x86 decoder or an execution proof.

All 479 branch/call rows match the layout's complete relocation sequence. For each, the opcode agrees with the annotated branch kind, the four-byte field occurs at the declared file offset, its signed value equals the saved displacement, and its decoded destination equals the named label address. The earlier arithmetic-only dependency is therefore resolved for the bytes represented in this listing. It remains separate from fresh external disassembly or observing a processor execute those bytes.

Eight targeted changes are rejected: a displacement byte, branch opcode, target annotation, immediate value, memory displacement, operand width, register field and syscall opcode. These small negative checks exercise distinct conditions in the original checker; they do not establish exhaustive malformed-instruction coverage.

## Syscall sites and the argument correction are now byte-bound

All fifteen listed syscall instructions have the fixed syscall bytes and the immediately preceding full-width move of their annotated syscall number into RAX. Their addresses and numbers match the earlier static record. This verifies the saved local encoding relationship. It does not infer reachable runtime sequences, successful calls or particular kernel effects.

All six R2 argument-load rows also match the earlier correction witnesses' exact expected and observed hex fields. The listing therefore supplies current byte-field support for the corrected stack offsets. The historical assertion that these are the only R1-to-R2 binary changes still needs the historical byte comparison; agreement with six selected R2 rows alone cannot establish exclusivity of a cross-revision difference.

## Transferable result and remaining dependency

A successor can now reuse a complete layout-to-listing join, rather than only matching summary counts or address equations. The evidence strengthens in specific steps: complete text custody, continuous field coverage, named code-blob identity, finite operand checks, then relocation and site associations. Each step has a narrower conclusion than native behavior. Retaining those layers prevents a static byte-consistency result from becoming an execution or acceptance claim during continuation.

No upstream encoder was imported or called, native artifact emitted or executed, external disassembler invoked, model consulted, live process scanned, workstation worker activated or upstream result accepted. Historical reports keep their capture-time scope.

Semantic reading reaches **530 distinct blobs / 4,517,801 bytes**, plus **77 identical alias paths**. The remaining gap is **4,986 paths / 3,899 distinct blobs**. The code-blob hash check does not add a separate full semantic reading for its unacquired binary path. Historical global acquisition overlap remains unresolved, and whole-repository reading remains incomplete.

Next: read the complete 118,160-byte `artifact-r2/builder.disassembly.txt` and compare its saved external decoding with this listing without rerunning a tool. Reconcile fresh main and ownership first; no recipient has accepted the next unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
