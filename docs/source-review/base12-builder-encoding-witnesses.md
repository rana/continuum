# Builder encoding witnesses: check finite expectations without running programs

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Four complete witness/static-observation JSON records total 29,588 bytes. Exact identities are in the [ledger](base12-coverage-builder-encoding-witnesses.json); original comparisons are in the [validation record](../../research/runs/base12-builder-encoding-witnesses/validation.json). No source was submitted to the builder, assembled as an ELF or executed.

## Research Delta: all finite encoding fields reconcile with the retained contract

All **73 unique encoding vectors** have matching byte lengths and cover the **23 non-relocating forms**. An original bounded decoder of their literal byte fields checks opcode families, REX width/register roles, ModRM direction, required no-index SIB, displacement widths and values, group extensions and immediate bytes against their statements and the held contract. It confirms the finite edge cases, including omitted bare REX for low 32-bit memory forms, forced zero displacement for rbp/r13, full-width immediates, signed displacement boundaries and IMUL's different operand direction.

This is a check of authored expectations against a restricted contract interpretation, not a new native candidate encoder, exhaustive x86 decoder or independent verification of external manuals. It produces no builder output and establishes no runtime semantics such as upper-half clearing, flags or memory safety. Negative-zero and leading-zero spellings can intentionally share byte expectations; vector count is not a count of independent semantic observations.

## Research Delta: concrete relocations and abstract endpoints answer different questions

All **14 concrete relocation vectors** agree on instruction length, patch position, next-instruction offset, signed displacement and final four bytes. They include ten branch/call forms plus backward, self and zero cases. All **four abstract signed-range cases** also reconcile, including rejection immediately outside the signed32 interval.

The abstract offsets cannot occur in an admitted tiny output file. They test arithmetic/narrowing expectations rather than supply executable source reaching those limits. Likewise a syntactically legal code-end or self target supplies no termination or safety guarantee. Keeping these categories explicit prevents endpoint arithmetic from being reported as an observed native boundary test.

## Research Delta: predicted code/map identity is reconstructible before execution

For both programs, the saved literal code length/digest, ELF-length implication, map header, every ordered map record, instruction count and relocation bytes reconcile. Reconstructing only the declared map serialization gives:

| Prediction | Code | Map records | Map bytes | Predicted exit |
|---|---:|---:|---:|---:|
| First program | 24 bytes | 5 | 192 | 17 |
| Branch program | 58 bytes | 12 | 416 | 42 |

Both map digests match. Instruction records form contiguous code coverage; zero-length label records preserve source order at the expected offsets. The branch program's saved displacements are −9 and +10. These buffers are reconstructed from already authored literal expectations to check identities; no ELF or native-builder output was generated. Program source hashes remain declarations until the two tiny source texts are read next. Exit values are predictions, not observed process results.

## Research Delta: saved correction bytes remain historical observations

The static-observation record's bootstrap/contract pins match held bytes. Its six argv-correction instruction rows have identical expected/observed hex, and each recorded changed file offset equals code offset plus 4,096 plus the instruction's final-byte position. Each old-to-new displacement increases by eight. This recovers the exact metadata behind the prior six-byte correction without claiming a fresh R1/R2 binary diff.

All fifteen saved syscall-site records use the same seven-number set found in source. Recorded buffer intervals are nonoverlapping and fit owned RW, while ELF/code dimensions and instruction/patch counts agree with the earlier review. The saved disassembler command/output digest and structural booleans remain that review's observations: binaries, disassembly and actual syscall execution were not acquired or repeated here.

For Continuum, expectations can have exact, reusable identities before execution. Preserve their derivation and labels so a later actual result can be compared with them without retroactively calling a prediction an observation or treating internal consistency as an independent trial.

Cumulative semantic reading reaches **483 distinct blobs / 3,683,240 bytes**, plus **53 byte-identical alias paths**, covering 536 paths. **5,057 paths / 3,946 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No private raw source, identifiers, executable, signal, output or trace bytes are published; no new model call occurred. Hosted CI checks this public contribution, not native encoding or program execution.

Next bounded unit: contract cases, historical comparisons, witness checksums and both tiny symbolic sources, **five texts / 31,764 bytes**. Bind the program sources, inspect grammar/I/O recipes and distinguish independent selected-byte comparisons from saved-layout consistency. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
