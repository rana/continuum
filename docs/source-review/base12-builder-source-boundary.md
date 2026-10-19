# Native builder source: enforce capacities before publishing a pair

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Bootstrap, dependencies and README were fully read: three new texts / 30,664 bytes. The already credited 6,957-byte contract was recovered from its pinned blob and reread as context, without another semantic credit. Exact identities and repeat custody are in the [ledger](base12-coverage-builder-source-boundary.json); source checks are in the [validation record](../../research/runs/base12-builder-source-boundary/validation.json). Bootstrap syntax was AST-parsed only; no upstream import, emission or execution occurred.

## Research Delta: the summary limits have actual source-level enforcement

The bootstrap verifies the ISA seed before importing it. The held identical seed payload and bootstrap digest match dependency declarations. Python constructs a native parser/encoder; the builder runtime does not import a consumer, copy its old ELF or execute the generated output. Its 33 dispatch names and five fixed consumer-profile fields agree with the B1 inspection record.

The source now supplies the derivation missing from a literal-only summary. Input admits at most **65,536 bytes**, checking reported regular-file size and also reading through EOF with a **65,537-byte** overflow probe. Count checks precede adding an instruction, label, relocation or map entry: **1,024 / 128 / 256 / 1,152** respectively. Every emitted byte checks the **16,384-byte ELF cap**. With code starting at 4,096, the derived code maximum is **12,288**; a 32-byte map header and 1,152 32-byte records derive **36,896 map bytes**. Declared buffers do not overlap and fit **155,648 owned RW bytes**.

These are source-inspected guards and arithmetic, not freshly exercised boundary tests or a guarantee that generated machine instructions implement the source correctly. The builder's own packaging bounds are separate from the consumer's tighter output bounds. Enlarging a consumer zero-fill mapping would not allocate it inside builder-owned memory, but remains a distinct output-profile change.

## Research Delta: symbolic encoding is bounded without proving program behavior

The lexer checks four tokens per statement and 31 bytes per token, rejects control/non-ASCII bytes even in comments, and accepts a final line without LF. Numeric parsing bounds unsigned decimal accumulation before multiply/add, then separately handles negative magnitude and signed operand ranges. The decimal threshold and final digit match the uint64 endpoint arithmetically. Register/name spelling is checked rather than truncated.

Encoding chooses fixed immediate/register forms and bounded displacement layouts, including no-index SIB for rsp/r12 and explicit displacement zero for rbp/r13. Label resolution requires `_start` at the first code byte, rejects missing/duplicate labels and checks each patch span and signed displacement. Parsing, encoding and resolution finish before output reservation. Source maps preserve instruction/label source order and same-offset labels; a code-end label is allowed because the builder does not prove control-flow semantics.

The source contains exactly the declared seven builder syscall literals: read, write, open, close, fstat, exit and fsync. That concerns the builder runtime. Its language can encode consumer syscall instructions; bounded compilation is not verification of arbitrary consumer behavior or execution safety. The builder never runs those outputs. Native runtime, native construction, native self-build and general compiler trust remain different milestones.

## Research Delta: a complete-looking pair is not an atomic success receipt

The builder reserves ELF first, then map, with exclusive creation and no-follow flags. It never truncates an existing entry. If the second reservation fails, the first empty file remains; write/sync/close failures can leave partial or full-looking files. Cleanup closes owned descriptors without unlinking evidence. Positive short I/O advances actual counts, EINTR retries preserve arguments, and close is not retried. These are source observations, not new fault tests.

Both files are written, individually synced and closed before exit zero. There is no pair rename, directory sync or crash-durability claim. The contract explicitly requires observed success rather than inferring it from file presence. This differs from the decoder's private-directory staging/rename contract and should not be compressed into a single generic publication guarantee. The R2 initial-stack pointer is preserved for argument access while helper calls change RSP; the earlier correction history is selected next.

The README/dependency status is a dated source/build checkpoint saying no native execution in that unit. Later accepted builder evidence remains a separate stage, as already stated by the B1 design records. This reading neither erases that later history nor treats it as fresh execution. Python/seed bootstrap and external inspection-tool declarations retain their separate dependency roles; tool binaries were not acquired.

For Continuum, publish completion should have a precise receipt condition and failure model. Preserving a reservation after partial failure can be deliberate evidence retention; its presence must not be mistaken for a committed multi-artifact result.

Cumulative semantic reading reaches **474 distinct blobs / 3,626,343 bytes**, plus **53 byte-identical alias paths**, covering 527 paths. **5,066 paths / 3,955 distinct blobs** remain without full semantic-reading claims. The additional alias is identical-content coverage, not an independent observation. Historical acquisition totals stay unchanged. No private raw source, identifiers, executable, signal, output or trace bytes are published. Hosted CI checks this public contribution, not historical builder correctness.

Next bounded unit: static inspector, design review, correction history and witness overview/source review, **five texts / 27,309 bytes**. Recover actual independent encoding review, R1/R2 correction and inspector predicates without execution. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
