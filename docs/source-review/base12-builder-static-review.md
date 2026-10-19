# Builder static review: structural agreement did not catch argv semantics

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five inspector/design/correction/witness-review texts total 27,309 bytes and were fully read. Exact identities are in the [ledger](base12-coverage-builder-static-review.json); comparisons are in the [validation record](../../research/runs/base12-builder-static-review/validation.json). The inspector passed AST-only parsing; no inspector, bootstrap, seed, native artifact or model ran here.

## Research Delta: keep the concrete defect beside the successful structural checks

The correction history and independent source review record a real R1 command-line blocker: argc was checked correctly, but argv0 was treated as input, outputs were shifted and the final map argument was ignored. Structural ELF/listing/patch inspection had passed. The reviewer reports that R2 changed exactly six load-displacement bytes to use user arguments at initial stack offsets 16/24/32, while retaining the argc load at zero. Current bootstrap source agrees with those intended accesses and preserves initial RSP across helper calls.

This is historical source/byte-review evidence, not a freshly reproduced R1 failure or six-byte binary diff. Neither revision ran in that source unit. R1 remains an immutable rejected revision rather than a candidate for another gate. The useful lesson is concrete: correct instruction boundaries, headers and relocation targets do not establish that a program reads the right arguments.

## Research Delta: recover the static inspector's actual predicates

The inspector hashes the artifact's saved bootstrap source against its build record, hashes the seed, and checks the saved source import set. It compares ELF/code bytes, complete fixed headers, zero padding, contiguous listing bytes and recorded relocation values/targets. It invokes external objdump/readelf for inspection and compares disassembled boundaries/bytes with the listing, rejecting undecodable instructions. It checks that each observed syscall has an immediately preceding literal-number load and the expected syscall set, plus bounded nonoverlapping buffer metadata.

These are complementary structural checks. The inspector explicitly retains full source/control-flow review as necessary; a syscall inventory is not a behavioral proof. Its source-snapshot binding preserves the artifact's own historical source rather than silently attaching later mutable source. Reread paths and external tools still depend on a stable inspection context. The inspector writes derived inspection files and a final report exclusively; running it would have effects, so it was only read and AST-parsed here.

The reviews declare **13,740 ELF bytes / 9,644 code bytes / 1,589 instructions / 479 internal patches** for R2. The ELF/code subtraction reconciles, but these remain retained artifact observations without new binary custody. The 479 bootstrap patches, 256-relocation input guard and 109 historical consumer fixups describe different objects and are not inconsistent counts.

## Research Delta: some guards are deliberately redundant

The author review derives a tighter valid-input bound: at most ten bytes per supported instruction and 1,024 instructions yield at most **14,336 ELF bytes**, below the independent **16,384-byte guard**. Likewise 1,024 instructions plus 128 labels produce at most 1,152 map records, or **36,896 bytes** with the header. These arithmetic relationships reconcile. They do not require inventing a valid program that independently reaches every guard, and are not new executable boundary tests.

The source review also covers sign/magnitude-based numeric checks, short-I/O cursor preservation, bounded symbol/patch tables, acyclic helper calls, exclusive reservations and non-retried close. It already qualifies stable private paths, initial-stack assumptions, repeated interruption, partial outputs and missing runtime tests. Those limits are original review findings, not new source defects alleged here.

## Research Delta: finite witnesses have more than one independence boundary

The witness overview distinguishes 73 manually specified non-relocating instruction vectors; branch/call and abstract displacement cases; grammar recipes; I/O expectations; two tiny program predictions; and selected historical byte comparisons. Expected bytes were hand-derived from encoding references rather than obtained by calling the pinned encoder. Historical whole-consumer agreement remains another evidence path, not independent proof of the encoder. The additional all-109-patch comparison is expressly internal saved-layout consistency.

The two proposed programs have predicted exits 17/42, code sizes 24/58 and map counts 5/12. These are authored derivations, not observed program outcomes. Accepted grammar snippets may be unsafe or nonterminating if executed; acceptance means source admission only. No witness supplies execution clearance, exhaustive proof or a performance result. The overview records an older official opcode-manual edition used when a newer volume did not load; this return did not newly fetch or verify those external references.

For Continuum, preserve why an independent source review changed a candidate despite a static PASS, and distinguish manual expectations, internal consistency and observed execution. Later evidence should extend that record rather than overwrite its earlier limitations.

Cumulative semantic reading reaches **479 distinct blobs / 3,653,652 bytes**, plus **53 byte-identical alias paths**, covering 532 paths. **5,061 paths / 3,950 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No private raw source, identifiers, executable, signal, output or trace bytes are published. Hosted CI checks this public contribution, not historical native correctness.

Next bounded unit: encoding vectors, relocation vectors, program expectations and R2 static observations, **four records / 29,588 bytes**. Inspect every witness field and recompute bounded byte/offset/map arithmetic without emitting or running programs. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
