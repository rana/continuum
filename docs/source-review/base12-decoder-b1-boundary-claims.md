# Decoder B1 boundary: one layout proposal leaves the full port open

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five design texts / 25,425 bytes were fully read: README, requirement matrix, layout sketch, next-source proposal and opening status. Exact identities are in the [ledger](base12-coverage-decoder-b1-boundary-claims.json); comparisons are in the [validation record](../../research/runs/base12-decoder-b1-boundary-claims/validation.json). No source variant, builder, decoder, generator or model was executed.

## Research Delta: direct transcription fails several independent bounds

The packet is explicitly design-only, based on a later historical main revision. Its decoder figures agree with held Gate-A metadata: **5,288 instructions**, **17,970 code bytes**, **22,066 ELF bytes**, **94 labels**, **198 patches** and **10,555,392 BSS bytes**. Against the builder limits stated in these documents, direct instructions/file bytes exceed the caps while current labels/patches fit. A lowered program can change every count; no complete symbolic decoder or future symbolic source size is supplied.

The matrix lists **53 width-aware consumed-form classifications** whose counts sum to all 5,288 instructions. It reports **4,178 SHA instructions**, leaving **1,110 non-SHA instructions**, already above 1,024. Held layout labels independently give the SHA byte interval **4,200 through 16,067 inclusive**, or **11,868 bytes**, agreeing with the document. The instruction partition remains an authored listing inspection; the full listing is unacquired. The arithmetic refutes only replacing SHA while leaving everything else unchanged, not a compact whole-program port.

The stated one-record-per-instruction/label map would need **5,382 records / 172,256 bytes**, compared with the stated maximum **1,152 / 36,896**. Those totals reconcile with a 32-byte header plus 32 bytes per record. They are design implications, not generated maps or newly verified builder behavior. Builder source, provenance and inspection records remain separate reading work.

## Research Delta: a fixed memory profile removes one structural obstruction

The proposed route preserves the decoder's current buffering and validation-before-publication order. Under that choice, a 4 KiB consumer RW mapping cannot host the held 10.6 MiB layout. Instruction compaction alone cannot fix that address-space mismatch. The packet does not claim that memory dominates total engineering cost or that streaming is impossible.

Its proposed additive profile changes only three serialized ELF fields: RW virtual/physical addresses at offsets **136/144** to **0x500000**, and RW memory size at **160** to **10,555,392**. Zero file size remains zero. Thus a larger zero-fill mapping need not add BSS file bytes; it does not itself consume that region inside the builder. The proposed RW end **0xF11000** and minimum gap **0xFC000** from the unchanged maximum RX extent reconcile arithmetically. The builder's own memory layout and the emitted consumer's layout remain separate.

The source-only proposal predicts unchanged instruction/count/code size because the three constants use fixed-width immediates. This unit has not read the builder source to verify that premise or built a variant. The old positive ELF hashes would change under the proposed profile, while code/map equivalence is an obligation for identical symbolic input. A different-size future decoder also changes the RX length fields; a three-field header comparison does not imply byte identity with the accepted decoder.

## Research Delta: value identities do not complete an instruction lowering

The requirement matrix distinguishes wire/SHA/publication semantics from current unrolling, buffer placement and encoding choices. It identifies missing forms and flags/clobber/access-width obligations rather than silently widening reads, replacing signed shifts with logical ones or treating 64-bit arithmetic as modulo-32 SHA.

An original check of the supplied rotate-right value identity passes **248 boundary-vector/count pairs**. That supports those values only: it does not verify flag behavior, scratch-register liveness, all uint32 inputs or a costed machine-code lowering. Similar cautions already appear in the matrix. Fixed-array storage can be changed only with a separate proof preserving integrity order, exact tail placement, history and publication behavior.

The packet also reconsiders competing work: it says existing semantic rules ignore one admitted input and therefore have a small effective domain; the interval [-36,36] indeed contains 73 integers. Rule semantics and generator benefit were not independently checked here. It correctly treats a native auditor as a dependency-boundary change rather than automatic independence. Neither statement establishes a performance result or selects a new implementation in Continuum.

## Research Delta: preserve proposal, selection and achieved maturity separately

The packet's only recommendation is a separately selected source-only fixed-profile variant. It expressly preserves the accepted builder lane, grammar and actual caps, distinguishes witness-only thresholds from those caps, and leaves parent selection/integration open. Acceptance of that source unit would establish a reviewed header-profile change; build bytes, runtime correctness, full decoder fit, native build-path completion and self-build would still need their own evidence. Existing consumed attempts do not transfer authority.

For Continuum, a bounded prerequisite can be useful without completing the larger milestone. Record exactly which obstruction it removes, what remains, and whether its fixed-cost prediction has been built or merely reasoned from source. A successful witness or native runtime should not silently stand in for rebuilding the intended application from editable source.

Cumulative semantic reading reaches **457 distinct blobs / 3,527,289 bytes**, plus **52 byte-identical alias paths**, covering 509 paths. **5,084 paths / 3,972 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No private raw source, operational identifiers, executable, signal, output or trace buffer is published. Hosted CI checks this public contribution, not an unbuilt decoder port.

Next bounded unit: B1 provenance, source-checks, checks, manifest and source-return records, **five texts / 35,527 bytes**. Bind inspection inputs and distinguish observed source facts from design predictions before following implementation work. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
