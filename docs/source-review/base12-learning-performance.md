# Interpreting learned results before accelerating them

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. This unit fully reads the three documents / 20,038 bytes in `research/owned-stack/2026-10-15/learning-performance-followup/`. The [ledger](base12-coverage-learning-performance.json) records exact Git blob, raw SHA-256, length and line count. Private source and historical messages remain outside this public repository.

No upstream code, dataset, learner, decoder, CPU/GPU probe, benchmark or model consultation ran. The documents' reported runs, consultations and later integrations remain attributed historical evidence.

## Research Delta: a constrained improvement is not an unconstrained trial

The original README interprets a learned dictionary whose candidates include all baseline candidates. With equal block overhead and choice-independent exact history, choosing a minimum cannot worsen an individual block payload. The dictionary itself is charged globally. Consequently the reported improvements across eight records cannot be treated as eight unconstrained successes in a sign test. Their magnitude and the matched authored-dictionary control remain meaningful. The document also distinguishes development validation from the unopened test partition, and rejects both population-wide generalization and the claim that validation transfer is no evidence at all.

Continuum should similarly identify structural advantages before interpreting a continuation comparison. Giving an arm the baseline's choices plus additional evidence may constrain some outcomes; counting wins alone can obscure that design. Declare the candidate relationship, whole-task cost and relevant control. A selected-output histogram is also not automatically a causal explanation: ties, ordering and the magnitude of each contribution matter.

## Research Delta: preserve the denominator and the attribution

The source reports archive totals A=5,524,566, B=5,418,065, C=5,467,168 and D=5,416,191 bytes. This unit independently recomputed elementary arithmetic from those reported inputs: B saves 106,501 bytes against A and 49,103 against C, while D is 1,874 bytes smaller than B. The fraction `106501/108375` is approximately 98.27% of D's **net saving relative to A**; it is not a total-size ratio, speed measurement or causal efficiency estimate.

Conditional on the documented one-stream format and 31 extra dictionary bytes, D's payload saving against B is derived as 1,905 bytes. The reported `D-B=-1874` satisfies the earlier upper bound of 31. The [arithmetic record](../../research/runs/base12-learning-performance/reported-arithmetic.json) retains the exact inputs, numerator, denominator and derived quantities. Computing them neither authenticates the original execution nor establishes persistence of its raw files.

The original README retains an uncertain audit-file write and a later terminal completion report. The integration guide subsequently reports completion of the saved-evidence audit and links its result. Those linked raw receipts and recipient replies were not newly examined here. A guide can resolve historical navigation without becoming fresh execution evidence or permission to recreate an uncertain file or repeat a scored run.

## Research Delta: optimize the dependency structure, then measure the whole boundary

`PERFORMANCE.md` proposes profiling an unchanged operation before selecting bit parsing, coding-cost fusion, vectorization, threading or device work. Its exact-output contract includes invalid-input behavior and bounded resource use. Hardware capability probes are not complete codec measurements; a plausible bottleneck remains a hypothesis until profiled. Resident device work and complete host-to-result work answer different questions.

The document derives an associative chunk-state composition for a fixed second-order residual recurrence. It explicitly declines to transfer that linear rewrite to a rounded/clipped learned feedback rule. This is a useful distinction for Continuum: batching or parallelizing a computation requires proving which state is sufficient at each boundary, preserving ordering, validation and cost accounting. A proof for one recurrence is not permission to change another algorithm's semantics. No scan implementation, compiler instruction or device speedup was verified by this reading; linked external technical references were not independently reopened.

The later integration guide preserves the earlier proposals while distinguishing completed bounded native decoder checks from unimplemented performance ideas, controller and builder milestones. Those historical proposals are not this chat's current action list. The separate owned-storage model lane retains its ownership.

## Validation, coverage and next unit

All three acquired byte strings matched the pinned tree's Git blob and length; raw SHA-256 was recomputed and full UTF-8 text read. Two in-scope original-file preservation bindings in `INTEGRATION.md` match. The third binding is an external historical handoff outside this unit and was not retrieved or checked. The guide itself is pinned separately. The [validation record](../../research/runs/base12-learning-performance/validation.json) distinguishes these checks from execution and raw-run auditing.

Cumulative direct reading is **185 distinct blobs / 1,322,614 bytes**, plus **47 byte-identical alias paths**. This covers 232 paths by reading or byte equality; **5,361 paths / 4,244 distinct blobs** remain without a complete semantic-reading claim. Alias directory context is not separately reviewed. Whole-repository reading remains incomplete.

The historical acquisition aggregate remains 539 paths / 530 blobs / 4,536,603 path bytes. Its full overlap index was not recovered, so these fetches are not blindly added. Hosted CI checks the public contribution, not private-source reading or inaccessible historical execution.

Next bounded review: eleven distinct unread files / 45,984 bytes under the same pinned `research/owned-stack/2026-10-15/alignment-pilot/` group, after reconciling fresh main and ownership. Review source and saved results without importing or executing upstream code. No recipient has accepted that next unit and no historical dispatch is reauthorized.
