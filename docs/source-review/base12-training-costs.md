# Saved training costs: complete input and separate greedy replay

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The 205,827-byte training-cost JSON was acquired with length, Git blob framing and SHA-256 verification. All 256 rows were inspected through a complete field-preserving view in four contiguous 64-row chunks: exposure identity, five fixed costs, thirty-five coefficient costs and the common raw cost of 6,147 bytes. Rebuilding the original JSON from that view reproduces its exact bytes, including layout. Raw JSON layout was not read verbatim. The [ledger](base12-coverage-training-costs.json) records the source identity and method.

## Research Delta: close the missing input before promoting replay

The acquired table's SHA-256 matches both model freeze and the saved learning-audit input identity. All seven inputs of the [previously inspected audit](base12-learning-audit.md) now bind to acquired payloads. This closes the previously explicit missing-input condition; it does not rerun that audit or establish its excluded external-wrapper and full-container properties.

Each row has exactly the expected fields and integer types. The exposure sequence matches thirty-two training records, two channels and four blocks per channel from the acquired corpus constants. All 10,240 predictive costs satisfy the previously derived full-block bounds of 531–6,675 bytes; their actual extrema are 1,799 and 6,670. These are candidate costs, distinct from selected output after raw fallback. The saved call count is 256 × 40 = 10,240 and its sample-evaluation arithmetic is 10,240 × 4,096 = 41,943,040; distinct training sample positions total 1,048,576. These checks do not observe native calls or read waveform payloads.

For Continuum, promote a claim only when the specific missing evidence has arrived. Closing an input set is a useful state transition, but preserves the audit's original acceptance boundary.

## Research Delta: reproduce the decision from saved values

A separately written set-objective calculation evaluates every candidate dictionary afresh against the entire saved matrix. Its objective sums each row's cheapest raw, fixed or selected coefficient alternative, then adds one serialized byte per dictionary entry. At each slot it minimizes that total and uses ascending coefficient order for equal minima. No upstream learner or audit function is imported or executed.

| Slot | Coefficient | Net bytes saved at this step | Equal best coefficients |
| --- | --- | --- | --- |
| 1 | 10 | 8,980 | 10 |
| 2 | 5 | 1,781 | 5 |
| 3 | 8 | 518 | 8 |
| 4 | 7 | 70 | 7 |

Every event matches the recorded learner and saved audit. Baseline block cost is 554,263 bytes; selected block cost is 542,910, plus four dictionary bytes gives 542,914 and net savings of 11,349. All four minima are unique; the tie rule was applied but this table does not exercise a tied winner. Selection ends at the four-entry budget; no fifth-slot stopping result or global optimum is claimed. The [validation record](../../research/runs/base12-training-costs/validation.json) preserves every candidate total at each of the four slots, along with actual input checks.

A distinct calculation reduces dependence on the original implementation's control flow. Its agreement remains conditional on the same saved cost matrix and objective. It neither validates waveform-derived costs nor supplies independent experimental provenance. No native program, signal decoder, upstream audit, new inference or experiment ran. For Continuum, retain the replay input identity, objective, budget and events so a successor can distinguish decision reproducibility from measurement reproducibility.

Cumulative semantic reading reaches **302 distinct blobs / 2,171,222 bytes**, plus **51 byte-identical alias paths**: 353 covered paths. **5,240 paths / 4,127 distinct blobs** remain without full semantic-reading claims. The historical global acquisition aggregate remains unchanged because its full overlap index is unavailable. No private source rows, raw receipts, operational identifiers or signal payloads are published. Hosted CI checks public repository behavior; it cannot verify private reading or historical execution.

Next bounded unit: the saved full-accounting audit source/result and two external-envelope records, four files / 46,234 bytes. Inspect the actual acceptance predicate, resource boundary and recorded accounting inputs before extending the learning-audit claim. Reconcile main and ownership first. No recipient has accepted this next unit; the separate owned-storage lane retains its ownership.
