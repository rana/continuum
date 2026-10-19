# Exact builder numeric-endpoint inputs

This Research Delta reads all sixteen inputs33–48 under `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/inputs/` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The files total 530 bytes. This chat owns the read-only contribution, based on Continuum main `4c21bd5a5e1b2634a4500bc1968e8a2f1f5ead70`. The [ledger](base12-coverage-builder-numeric-inputs.json) binds every exact source; the [validation record](../../research/runs/base12-builder-numeric-inputs/validation.json) records original finite checks and metadata joins.

## Complete source custody and endpoint relations

Every byte of all sixteen sources was read. Each is exactly the entry-label line plus its materializer endpoint statement and final LF. Length, Git blob, SHA-256, fixture-list identity and both physical/LF line counts agree with the frozen case manifest. All authored counts are one label, one instruction and zero relocations; their acceptance-dependent map-row fields also agree.

The endpoint dictionary is read through `ast.literal_eval`, without importing or running the materializer. An original finite numeric comparison checks the source tokens against their declared operand grammar and ranges. Its seven accepted and nine rejected verdicts agree with all sixteen frozen expectations and the corresponding derived saved case records. Output-state, length, mode and digest declarations likewise reconcile as metadata; no private result payload was acquired.

The cases cover the unsigned 64-bit maximum and one above it, the negative signed 64-bit minimum and one below it, both signed 32-bit displacement endpoints and their adjacent failures, signed eight-bit immediate endpoints and adjacent failures, and the shift upper boundary. Their literal values are checked with integer arithmetic rather than truncated to the target field before admission.

## Numeric value alone loses two grammar distinctions

Two cases are rejected for their spelling even though value normalization makes them look admissible. The plus-prefixed immediate token normalizes to positive one, but the frozen grammar rejects its leading plus. The negative-zero shift token normalizes to zero, but the shift rule rejects a negative sign even when its magnitude is zero.

A deliberately value-only comparison accepts both of these cases; the finite grammar-aware comparison rejects them as specified. This is a concrete counterexample to discarding token spelling before validation. It is not a newly observed native parser failure or an exhaustive numeric-parser test.

The distinction also prevents a misleading description of the immediate range: positive values may reach the unsigned 64-bit maximum, while negative magnitudes have their separate signed bound. A single signed-64 value check would not express this fixture contract.

## Accepted byte fields and repeated map identities

All seven accepted literal encoding snippets match their declared fields. Checks cover register/opcode prefixes, full 64-bit immediate bit patterns, signed 32-bit displacement fields, signed eight-bit immediates and the shift count. The corresponding declared ELF lengths equal the fixed prefix plus the snippet lengths. No candidate encoder or full ELF construction ran.

Reconstructing each accepted case's two literal map records and header produces 96 bytes and matches its expected map digest. Seven cases form three repeated-map groups of sizes two, two and three. Those maps describe identical source-line/span structure for instruction lengths ten, seven and four bytes, respectively. They do not identify the distinct instruction contents. A map-content hash therefore needs a separate code/source association when used in a handoff.

These expected-map checks preserve their expectation layer. They neither acquire actual native outputs nor turn agreement with the saved derived review into a fresh execution observation.

## Transfer and next unit

For Continuum, preserving exact source tokens alongside parsed values is consequential when lexical distinctions affect validity. Code identity and structural map identity also remain different associations. A continuing worker can reuse these finite source/metadata checks while keeping native behavior, raw payload custody and acceptance explicit.

No upstream module was imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation worker activated or upstream result accepted.

Semantic reading reaches **567 distinct blobs / 4,883,647 bytes**, plus **79 identical alias paths**. The remaining gap is **4,947 paths / 3,862 distinct blobs**. Historical global acquisition overlap remains unresolved; whole-repository reading remains incomplete.

Next: complete capacity-boundary fixture inputs05–14, ten paths / 152,328 bytes. Read their exact bounded/repeated source structure and join byte/token/instruction/label/relocation/map limits to the frozen expectations without executing source. Reconcile fresh main and ownership first; no recipient has accepted that unit. Separate storage, dispatch and public checkpoint lanes retain ownership.
