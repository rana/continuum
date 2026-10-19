# Gate-A artifact records: reconcile declarations without claiming executable custody

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Five dependency/build/layout/readelf/static-check texts were fully read: 25,544 bytes, including all 54 globals, 94 labels and 198 patch records. Exact identities are in the [ledger](base12-coverage-gate-a-artifact-records.json); original checks are in the [validation record](../../research/runs/base12-gate-a-artifact-records/validation.json). No upstream program, inspection utility or executable ran here.

## Research Delta: source pins close a dependency set, not its entire provenance

All six dependency entries match exact held payloads: emitter, ISA seed, wire document, codec source, native signal source and reference decoder. The build record's seed path/digest and emitter digest agree with those entries; the static report binds the same emitter digest. These are actual payload comparisons rather than merely matching digest strings between documents.

The dependency record separately declares an earlier source baseline and inspected owner-document revision. Those authored commit references were not freshly resolved against their commit trees. Likewise, the recorded CPython version is historical build metadata, not a newly observed interpreter. Dependency custody, revision-history attribution and current environment remain separate facts.

The dependency/build/static records say zero native executions, NOT EXECUTED or NONE at their pre-execution stage. Later correctness receipts describe a later stage. Keeping both is necessary: the older fields neither negate the later run nor authorize a new one. There is no reason to rewrite a historical build record into a current execution status.

## Research Delta: all declared allocation and branch arithmetic reconciles

The retained layout has **17,970 code bytes**, **22,066 ELF bytes**, entry **0x401000**, and writable base **0x500000**. Code plus the 4,096-byte header region equals the declared ELF length. All **54 global offsets** match the previous return's independently calculated allocation, and both layout and static report agree with its **10,555,392-byte BSS** result. The declared RX file extent ends **1,026,510 bytes** before the writable base. This is address/length arithmetic, not an observed process memory footprint or a loader experiment.

Every one of the **198** relative-displacement records fits signed 32 bits and resolves, from its declared file position plus four bytes, to its named declared label. All patch fields are distinct, ordered, nonoverlapping and within the declared code-bearing file span. All **94** label addresses are unique and within the declared code interval; the entry matches `_start`. These checks do not establish that bytes at those positions encode the claimed instructions, or that target addresses are actual instruction starts. That requires additional byte/listing custody and inspection.

The static report declares **5,288 instructions** and repeats the layout's ELF digest and byte/BSS totals. Its instruction count remains a saved inspector result, not a count regenerated from a listing here. The executable digest also agrees with the freeze declaration, but the executable is unacquired. Repeated consistent declarations do not replace hashing the artifact payload.

## Research Delta: external inspection output supplies scoped historical evidence

The retained readelf text records an ELF64 little-endian x86-64 executable with entry 0x401000, program headers at offset 64, three 56-byte program headers, no section table and no dynamic section. Its RX load length is 0x5632, matching 22,066 bytes; its zero-fill RW extent is 0xa11000, matching 10,555,392 bytes. The two load mappings and non-executable RW stack agree with the already read emitter's structure and the static report.

This fills in historical header observations that the inspector source did not separately assert in full. It does not strengthen that inspector into a general malformed-ELF validator. The text has no self-contained byte-to-command attestation, and no current readelf/objdump invocation or ELF-byte comparison occurred. Source construction, retained external output, copied metadata and native execution retain distinct evidence paths.

For Continuum, an artifact view should expose which fields are payload-bound, which are arithmetic recomputations, and which remain declarations from an earlier stage. Agreement improves recoverability while preserving the work needed for stronger verification.

Cumulative semantic reading reaches **436 distinct blobs / 3,358,805 bytes**, plus **52 byte-identical alias paths**, covering 488 paths. **5,105 paths / 3,993 distinct blobs** remain without full semantic-reading claims. Historical acquisition totals remain unchanged. No private raw source, operational identifiers, executable, signal, instruction listing, disassembly, decoded output or trace buffer is published; no new inference occurred. Hosted CI validates this public contribution, not the historical native artifact.

Next bounded unit: reviewer instructions/request and retained parent decoder review/static-verification records, **four texts / 29,617 bytes**. Recover actual reviewer exposure, conclusions and qualifications before promoting approval claims. Reconcile main and lane ownership first; no recipient has accepted this next unit. Owned-storage, dispatch-reconciliation and public self-use checkpoint lanes remain separately owned.
