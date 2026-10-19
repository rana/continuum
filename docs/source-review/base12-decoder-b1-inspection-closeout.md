# Decoder B1 inspection closeout: complete packet custody, scoped derivation

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Nine inspection/ownership/review/reader/checksum texts total 32,863 bytes and were fully read. Both reader sources passed AST-only syntax parsing; neither was imported or executed. Exact identities are in the [ledger](base12-coverage-decoder-b1-inspection-closeout.json); comparisons are in the [validation record](../../research/runs/base12-decoder-b1-inspection-closeout/validation.json).

## Research Delta: preserve the stopped inspection and its actual correction

The retained r1 reader attempts literal evaluation of the builder's entire header-field list. The r2 reader instead filters to offsets 136/144/152/160/168 before evaluating their values. It also removes the repeated builder instruction-listing walk and count assertion. All four helper-function ASTs remain identical between versions: digesting, contiguous listing parsing, fixed ELF-header inspection and instruction classification. The two exact reader hashes agree with the correction/provenance/source-check records.

The reported exit-one literal-parser failure is therefore consistent with a narrowly corrected inspection reader. This return did not execute either version or reproduce the old exception. The corrected invocation's recorded success remains historical; no failed native gate or candidate correction is inferred. The reader writes its derived summary with exclusive file creation, but reads multiple source paths separately; the pinned baseline and stable input files remain provenance assumptions, not an atomic multi-file snapshot implemented by that reader.

The source distinguishes what it derives. It obtains the 33 dispatch names and five needed header values through AST inspection, counts existing decoder listing rows, checks contiguous listing bytes against the saved ELF, and partitions SHA by declared labels. Several capacity fields are different: **eight numeric limits are literal values written into the output summary**, not extracted enforcement predicates. Their agreement with design documents does not independently verify the builder enforces them. The actual builder source is the next useful reading.

The classifier is specialized to the accepted listing: annotations identify forms, with the first encoding byte distinguishing certain operand widths. It is not a general independent instruction decoder or a full flags/liveness proof. The focused reviewer reports separate byte/header/listing checks, without claiming new disassembly or runtime correctness. Those historical observations do not acquire the missing binaries/listings in this session.

## Research Delta: a focused review supports only its stated decision

All twelve focused identity rows agree with the packet's provenance declarations. The review supports a separately identified fixed decoder-output profile for the concrete buffered decoder. It explicitly distinguishes three profile constants from variable RX-length fields, the builder's own memory from consumer memory, and missing direct forms from proofs that each form must be added.

It does not accept every final packet paragraph, rank the proposal as cheapest, establish a compact symbolic decoder, or grant implementation/execution authority. It preserves different publication contracts for builder outputs and decoder outputs rather than treating them as one mechanism. Source recommendations, parent selection and achieved native-build/self-build maturity remain separate.

Ownership records describe supported task/worktree/ref/open-PR checks at that historical time. They explicitly disclaim full-host process absence and record no retry of previously denied process metadata. A returned task inventory is scoped evidence, not current exclusive ownership or proof that all other workers stopped. Private task identities, workstation paths and tool-result identifiers remain unpublished.

## Complete packet reading and custody

All **17 manifest payloads** match exact held lengths and SHA-256. All **18 top-level checksum entries**, both focused-review checksum entries and all three provenance review copies bind. The top-level checksum includes the manifest and excludes itself. All **19 packet paths / 93,815 bytes** now have full semantic readings, with no remaining packet path uncredited. This scoped closeout does not close its 36 historical input pins, outside-packet source/artifact gaps, parent decision or full repository reading.

For Continuum, an inspection summary should preserve which values were computed from bytes, extracted from source, copied as constants or reported by another reviewer. Complete packet custody makes that distinction recoverable; it does not erase it.

Cumulative semantic reading reaches **471 distinct blobs / 3,595,679 bytes**, plus **52 byte-identical alias paths**, covering 523 paths. **5,070 paths / 3,958 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals stay unchanged. No upstream reader, builder, native artifact or model ran; no private raw source, operational identifier, executable, signal, output or trace bytes are published. Hosted CI checks this public contribution, not the historical inspection or an unbuilt port.

Next bounded unit: native builder bootstrap, dependencies and README, **three unread texts / 30,664 bytes**, with its already credited contract recovered as context. Inspect actual parser/encoder/output-bound enforcement without importing or executing it. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separate.
