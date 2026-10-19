# Exposure isolation and bounded retrieval release

Research Delta from main `416e41f8f9a009f02fb20152d67f0c74bbef606a`, owned by this continuing chat. Fresh main, repository instructions and open PRs were reconciled before selecting the unit. The [original packet and rubric](README.md) remain unchanged. This unit prepares isolated request bytes, implements a source-only retrieval bridge and freezes a scoring procedure. **No trial receiver or scorer has run.**

## Exposure audit and repairs

The original menu pointed at the ten-entry source-pin inventory, which exposed metadata for both historical revisions even in the before case. That includes the later read-only result path and could reveal the existence of the fix. C's initial native rendering also carried six policy limits and basis-validity markers absent from A/B's initial representations. Those differences could influence decisions without any benefit from representation.

The [release](release/manifest.json) now maps neutral `current/` aliases to only the selected case's five current source/evidence files. Its pin projection contains only those five files. Original exact bytes and explicitly identified path-redacted historical result projections retain their original identity bindings; neutral aliases do not rewrite source text. The sender-side release manifest and case mappings are **not receiver inputs**. A receiver gets only its exact request, alias menu and that cell's bridge responses. It cannot retrieve the rubric, other cases, root source inventory or methodology reviews.

Every arm now receives identical shared facts, limits, metadata and menu. A is a readable rendering of the actual WorkState, B its ordinary JSON, C its native context rendering. All can retrieve the full local verification record; C is given no exclusive verdict proposition. This narrows the study to **same-information formatting/provenance usability calibration**. It does not isolate native execution benefit, independent authoring quality, backend speed or total product usefulness. A is not relabeled the best possible independently authored note. Author hindsight remains explicit.

The author audit binds these proposition groups to exact request contents; its assertions and common-input checks are in `test_bridge.py`:

| Proposition group | A | B | C |
| --- | --- | --- | --- |
| Objective, completion criterion and frozen-task constraint | readable handoff | WorkState | authored context records |
| Actual recorded probe and proposed route/writer boundary | readable decision | decision | authored decision |
| Decision status, no attempt basis and reopening condition | readable decision | decision | authored decision + shared markers |
| Uncertainty and why it matters | readable uncertainty | uncertainty | authored uncertainty |
| Offered handoff roles/scope/required decision | readable handoff + shared scope | handoff + shared scope | authored handoff + shared scope |
| No supplied attempt records, without claiming none occurred | shared facts + handoff | shared facts + empty attempts | shared facts |
| Work/source identities, original anchor, selector/budget/coverage | shared facts | shared facts | shared facts + rendered metadata |
| Actual local verification/current case revision and six native limits | shared facts | shared facts | shared facts + rendered limits |
| Current source, accepted state, case-only pins and full proof access | identical alias menu | identical alias menu | identical alias menu |

This is an author audit, not an accepted independent review. The [Claude Collaborator exposure-review attempt](exposure-review-attempt.json) returned `invalid_response`, HTTP 200 and `inference_outcome: unknown`; no model answer was accepted and actual model/usage were not supplied. The exact input and returned error are preserved. No automatic retry was made. The earlier completed methodology review retains its separate scope and does not become a successful audit of these new inputs.

## Bridge contract

`bridge.py` performs no provider calls, shell execution or filesystem writes. A caller must supply the precommitted release-manifest SHA-256; every retrieved file is rechecked against that manifest before delivery. This is custody relative to a trusted pin, not authentication of its author or a sandbox for a caller that already has host access. No path supplied by a model is opened directly. Only exact menu aliases select files, and mappings are restricted to the cell's evidence directory. Case/source directory or file symlink replacements and changed manifests/payloads fail.

The model protocol accepts only one strict JSON object with either `paths` or `answer`. Duplicate keys, nonfinite numbers, mixed/extra keys, invalid lists and oversized UTF-8 model responses fail. At most eight distinct aliases per request, two retrieval rounds and 65,536 **retrieved source bytes** are admitted. Denials consume a round; unknown aliases disclose no file content. An over-budget request returns no partial files. Final answers remain available after retrieval is exhausted and close the bridge cell.

Source-byte limits do not hide envelope overhead: future execution must retain/count the complete UTF-8 request and response serializations, hashes, tool/model metadata and provider usage. Denied-request text and repeated conversation input still cost bytes/tokens. No billing estimate is inferred. A malformed/truncated/unknown provider result ends that cell for inspection; the bridge does not repair or resend inference. The two-round ceiling permits up to 27 provider invocations for nine final observations, with incomplete cells retained explicitly. A caller must persist each returned provider outcome before the next invocation; this library is not a durable dispatch or retry engine.

The nine exact initial requests specify the same `opus` alias and medium effort. Actual returned model/configuration must still be recorded and matched. They exclude grading and sibling-case inputs; only differing handoff representations and lengths vary initially. Preserve those length differences as observations rather than padding or giving C free input. No API request is made by generating or loading these files.

## Frozen scoring procedure

Use the six R1–R6 conditions already fixed in README. Do not score until a receiver's final answer or incomplete outcome has been retained. For each completed cell, create two fresh supplied-context rater requests containing: the same common task, only that case's current source/pin/accepted-state/verification evidence, the receiver's exact answer, and the six conditions. Do not include arm name, other responses, earlier rater judgments or methodology exchanges. Role-separated calls do not establish blinded evaluation: response format may reveal the arm. Two calls to the same model have correlated biases even with no conversation memory.

Each rater returns a row per condition with `pass`, `fail`, `disputed` or `unavailable`, quoted response spans, source aliases and a concise explanation. Allow a source-supported unexpected defect/next action; do not demand one exact phrase. Absence of evidence is not automatically a pass. R6 also receives the actual complete cost/exposure record; if those observations are missing it is `unavailable`, never zero. Any disagreements remain disputed in the final table; an author note may explain but cannot manufacture independent agreement. Rater use/time is recorded separately from receiver cost and common preparation.

Report raw case/arm vectors, unsupported inferences, missed corrections, unnecessary holds/repeats, retrieval sequences and measured/unknown cost components. R3/R4/R5 failure stops trial expansion for analysis, per the prior rubric. No single-draw directional performance or adoption conclusion is allowed. The initial case labels come from source/history, not the native status. Historical references remain distinguishable from current supplied evidence and real live project state.

## Executed validation and next action

Ten bridge test methods passed, including exact ordered bytes, cross-case/grading/path denial, malformed JSON, UTF-8 bounds, denial rounds/final state, aggregate budgets, changed artifacts/manifests/symlinks, case-01 pin isolation and common request/menu/model parity. The existing original-packet checker also passed. A prior unpublished release generation is retained separately; the old published packet was not overwritten.

The [release validation](release-validation.json) pins the generated manifest and code, records exposure assertions and observed command outcomes. The PR's hosted CI now runs these bridge tests without inference. It does not rerun historical source commits or invoke Claude.

The owner selects this release for **one read-only protocol-calibration cell**, using the author audit with its explicit lack of independent confirmation. Its purpose is to test the request/retrieval/accounting flow, not establish native advantage. Next useful unit: run case-01/A with complete visible exposure and cost recording after fresh remote reconciliation. The bridge itself has no provider invocation implementation; the release manifest does not install or automatically dispatch a worker. The unknown exposure-review call is not retried. Separate receiver/scorer calls have distinct purposes and exact retained inputs; no general adoption claim follows. No receiver/rater has accepted or executed a handoff, and no default-workflow adoption is justified by this release.
