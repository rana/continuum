# Builder contract witnesses: admission, custody and historical comparison

This Research Delta completes five source readings, totaling 31,764 bytes, at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The current Continuum chat owns this read-only contribution. The [additive ledger](base12-coverage-builder-contract-witnesses.json) records each source path, length, Git blob and SHA-256; the [validation record](../../research/runs/base12-builder-contract-witnesses/validation.json) separates original checks from retained expectations. The input Continuum main is `97804f36ca631e70fdfa466d8375c8c54a5b8a37`.

All selected files belong to `research/owned-stack/2026-10-16/native-builder-slice/witnesses/`: `contract-cases.json`, `historical-comparison.json`, `SHA256SUMS`, `exit17.b12asm` and `branch42.b12asm`. Their identities were checked against the complete pinned tree before full reading. No upstream source was imported or executed, no native output emitted, and no new model invocation made.

## Admission is narrower than execution safety

An original declarative checker of the retained small source examples agrees with all 63 saved contract verdicts: 23 accepted and 40 rejected, including their conditional success/source-error exit expectations. It checks byte admission before comment removal, token limits, instruction forms and operand bounds, label uniqueness and references, instruction counts, and the required first symbolic instruction at `_start`. It does not call the native parser or encode instructions.

The examples expose useful boundary distinctions. Invalid bytes remain invalid inside comments; adjacent comment markers split tokens. Numeric negative zero and shift-count minus spelling have different admission rules. Multiple labels can name one code offset, and a label at code end can resolve. An accepted source can contain just one instruction or a jump to code end. Admission therefore establishes neither a terminating program nor safe control flow. Agreement of this second contract representation with the finite examples is useful consistency evidence, not native parser correctness or exhaustive grammar coverage.

Nine larger recipes were checked only by count and length arithmetic, without constructing their expanded inputs. These cover the 65,536-byte input bound and one-byte overflow, 1,024/1,025 instructions, 128/129 labels, 256/257 relocations, and the maximum 1,152 map records occupying 36,896 bytes. These are recipe checks, not executed boundary tests.

## Source identity now reaches the tiny examples

Both tiny source hashes match the earlier program expectations. Their physical statement lines, label offsets and map kinds agree with the predicted maps: `exit17.b12asm` has 138 bytes and six physical lines; `branch42.b12asm` has 206 bytes and thirteen. Both pass the declarative admission check. Their predicted exits remain unobserved here. This closes a source-custody gap in the previous [encoding-witness review](base12-builder-encoding-witnesses.md); it does not turn predicted machine code into a fresh emitted artifact.

All ten entries in the witness checksum file bind held files. The witness directory now has complete reading coverage across all eleven files / 75,717 bytes, including the checksum file itself. This scoped closeout says nothing about unread files elsewhere in the builder lane.

## Saved comparisons retain their dependencies

The historical record contains 29 selected instruction pairs whose expected and observed hex strings agree. Their saved file/code offsets reconcile and fall within the declared 6,930-byte runner. Four selected manual relocations independently satisfy target-minus-next-instruction arithmetic and agree with the recorded signed displacement bytes, including forward and backward targets.

The broader all-109-patches claim is explicitly saved-layout consistency. The historical runner ELF, instruction listing and layout were not acquired for this unit. Matching fields in their comparison record cannot replace a fresh comparison with those payloads, independently recovered labels, or observed execution. Their declared identities remain source metadata.

Ten publication expectations were also read in full. They distinguish malformed source before output reservation, existing-path collisions, a second reservation failure leaving the first empty file, and write/sync/close failures leaving partial or full-looking outputs. Interrupted close is not retried. Successful fresh outputs depend on observed exit zero and the stated I/O assumptions; exclusive creation does not establish atomic pair publication or crash durability. No filesystem fault, interruption or output experiment ran here.

## Coverage and next return

Cumulative direct semantic coverage reaches **488 distinct blobs / 3,715,004 bytes**. The two tiny sources also identify 22 additional identical paths, bringing alias credit to **75 paths**. Those aliases are content equivalence, not 22 additional readings or observations. The ledger leaves **5,030 paths / 3,941 distinct blobs** without full semantic-reading claims. Historical acquisition overlap remains unresolved.

The next bounded return is six migration/control/proposal texts totaling 22,795 bytes: `migrate_runner.py`, `runner.b12s`, `CHECKPOINT.json`, `OWNER.json`, `OPEN.md` and `TEST_PROPOSAL.md`. Read their actual transformation and ownership boundaries without importing, emitting or executing, before taking on the larger migration table. Reconcile fresh main and other workers first. No recipient has accepted that next unit; separate storage, dispatch-reconciliation and public checkpoint work retain their ownership.
