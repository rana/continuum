# Complete decoder-profile source and author review

This Research Delta fully reads `bootstrap.py`, `STATIC_REVIEW.md` and `AUTHOR_STATIC_CHECKS.json` under `research/owned-stack/2026-10-16/native-builder-decoder-output-profile/`. The three files total 32,987 bytes at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This chat owns the read-only contribution based on Continuum main `2506de176425baf21f7613049312909c7151f5ce`. The [ledger](base12-coverage-decoder-profile-source-static.json) pins all sources; the [validation record](../../research/runs/base12-decoder-profile-source-static/validation.json) retains actual checks and their limits.

## Acquired source closes the earlier reconstruction

The complete 24,745-byte bootstrap matches the identity previously derived from the retained diff. Applying that exact hunk to held R2 reproduces every acquired source byte. Recursive AST comparison finds precisely the same three Constant.value paths and before/after values recorded by the author. The complete author JSON also round-trips exactly.

The source preserves parser/grammar, argument handling, helper methods, errors, publication and its own packaging function. All 33 grammar forms agree with the author record. The consumer-header change remains the narrow source delta established in the [foundation review](base12-decoder-profile-foundation.md); no module or seed is imported here.

The full source shows a temporary Python/seed bootstrap whose main function would emit source, code, ELF, listing and layout metadata if invoked. Reading those statements is not invoking them. The source's package cap and emitted-file permissions remain part of its historical build-only design, not current activation or execution evidence.

## Fixed width supports a prediction

The held seed's immediate method defaults to the 64-bit path and selects its packing width from that width argument, not from the immediate magnitude. The unchanged header loop supplies no alternate width. All old and replacement values fit the admitted 64-bit range, so the three replacements retain the predicted instruction widths.

This was checked from the actual explicit width branch in the seed's syntax. A draft checker assumption about parameter spelling was corrected before the retained record; it is not an upstream source failure. No assembler method was called to obtain the result.

The author prediction matches the held R2 metadata: 1,589 instructions, 163 labels, 479 fixups, 9,644 code bytes and 13,740 ELF bytes. Source identity outside the three leaves and fixed-width immediates support that prediction. They do not produce a new native artifact hash, authenticate later output files or establish runtime correctness. The author record itself marks new bytes unobserved and new artifact hashes unknown.

## Builder state remains distinct from consumer memory

Literal source extraction reproduces all seven owned-buffer intervals and 33 scalar slots. Together they occupy 137,785 bytes within the unchanged 155,648-byte owned RW region, leaving 17,863 bytes of arithmetic layout slack. Every interval is ordered, nonoverlapping and in bounds. This is layout arithmetic rather than measured free memory.

The source retains its input, output, label, instruction, relocation and map limits, including the separate 1,152-row map bound. Its own package AST is identical to R2. Enlarging a generated consumer RW segment therefore does not enlarge builder storage or admit a larger symbolic decoder automatically.

The proposed consumer layout fields in the author record agree with the reviewed contract: fixed entry/RX mapping, page alignment, zero RW file size, three headers and a non-executable stack. Those remain contract/source checks rather than fresh ELF inspection.

## Citation and result boundaries

The static review cites a separate independent PASS report and a claim that 230 original R2 paths match their baseline blobs. It also preserves an inspection-reader correction concerning unified-diff context formatting and limits that review's acceptance scope. Those cited records require their own complete review; this unit does not substitute the author's citation for direct evidence.

One additional path in the pinned build-result tree is byte-identical to the acquired bootstrap. This establishes source-copy content identity, without newly acquiring that result path or accepting the surrounding build record. Later artifact/execution records remain separate from this source-unit review.

No upstream source or seed was executed, native artifact acquired/emitted/executed, model consulted, live process scanned, workstation activated or recipient acceptance obtained. The lesson is to promote a predicted property only as far as its mechanism supports: syntax can explain unchanged width and state layout while leaving emitted identity and observed behavior open.

Semantic reading reaches **617 distinct blobs / 5,360,750 bytes**, plus **115 identical alias paths**. **4,861 paths / 3,812 distinct blobs** retain full-reading gaps. Whole-repository reading and historical global acquisition overlap remain incomplete.

Next: complete six independent-review envelope files, totaling 17,687 bytes, preserving the original report, identities, checks, provenance, reader correction and checksum scope without executing the reader. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted the next unit.
