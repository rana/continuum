# Reference decoder: dimensions of independence

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Seven texts / 33,915 bytes were fully read: reference-decoder integration, preservation, README, result, manifest, decoder source and source review. The [ledger](base12-coverage-reference-decoder.json) records exact paths and identities. No decoder, launcher, encoder, native code, dataset acquisition or model was executed.

## Research Delta: implementation diversity has a specific scope

The earlier stage-A result checked decoding in a fresh process using the original implementation. This later packet describes one decode of the existing archive through a separately implemented reference. Source inspection confirms standard-library imports only; it imports neither the original codec nor its native wrapper. Its reconstruction uses accumulated finite differences, and its signed-byte repacking uses division/modulo. These differ from the original coefficient/native operations and bit-mask formulation.

The source and reports explicitly retain the same authorship and shared wire specification. A separate implementation can challenge implementation-specific errors while sharing a specification mistake or an author's assumptions. A fresh process can challenge inherited state while retaining the same algorithm. Neither property establishes independently authored validation or OS isolation. Continuum should describe which dependency was changed and which was shared when treating a result as corroboration; the word independent alone conceals too much.

The historical result reports exact original-file equality after one standalone invocation of the existing archive. This unit reads that report and the source review, but has not yet inspected its raw execution receipt, launcher, result review or evidence archive. It therefore adds source-derived assessment and attributed history, not a fresh decoding observation. It does not add a compression measurement, heldout result, learned predictor, radix advantage or throughput comparison.

## Research Delta: compare mechanisms through an explicit identity

For order p, the original fixed-predictor residual is the p-th backward difference. The reference initializes successive differences from the warmups. Its descending updates use the current higher difference to advance each lower one until the sample is recovered. This gives a different route through the same recurrence, with order zero using the residual directly.

Without importing either implementation, this unit recomputed the alternating binomial predictor coefficients for orders zero through four and compared them with the retained original coefficient literal. All five agree. Original arithmetic also checks all 4,096 signed-12 values: division/modulo yields the same low byte and high nibble as the bit-mask representation. These finite arithmetic checks support the stated correspondence; they are not execution of the reference functions, full wire-parser equivalence, or historical signal reconstruction.

The source bounds metadata and bit reads, validates reconstructed signed-12 values, rejects trailing bytes/padding, and checks the reconstructed original digest before creating outputs. It then creates a directory and writes header and data sequentially. A completed validation gate and exclusive file creation do not provide atomic publication of the pair. The historical review also keeps protected-path assumptions and external resource enforcement explicit. No interruption, malicious-input campaign or path-race experiment was performed here.

For Continuum, a useful cross-check names the transformation being compared and its domain. Agreement of two implementations under one invariant is stronger than their matching names, while still leaving shared assumptions, parser behavior and effect publication to separate checks.

## Evidence checked and remaining work

All seven acquired byte strings match pinned Git blob identity, length and raw SHA-256. Four Markdown documents and two JSON records were fully read; the Python source was fully read and parsed as syntax. Its source identity agrees with the preservation record. The [validation record](../../research/runs/base12-reference-decoder/validation.json) retains imports, arithmetic and partial manifest bindings.

For this separate reference packet, **5/17 evidence-manifest entries** and **6/19 preservation entries** match current bytes or a pinned identical-blob alias. Each includes one verified empty-stderr alias, admitted only as mechanical custody. Outstanding payloads remain explicit. This does not reopen the preceding original-run packet's completed 27/27 delivery and 49/49 preservation checks. The new reference archive itself is not acquired or inspected in this unit. No private payload or operational identifier is published.

Preparation-time held-publication labels remain unchanged in the preserved files; the later integration note describes subsequent approval. This review does not rewrite those labels or treat historical one-run authority as permission to repeat the run.

Cumulative full semantic reading reaches **258 distinct blobs / 1,724,340 bytes**, plus **49 byte-identical alias paths**: 307 covered paths. **5,286 paths / 4,171 distinct blobs** remain without complete semantic-reading claims. Empty-payload aliases are not semantic coverage. The historical acquisition aggregate remains unchanged because its complete overlap index is unavailable. Hosted CI checks this public contribution and existing repository behavior, not private reading or historical execution.

Next bounded unit: eight reference-decoder launcher/receipt documents / 23,272 bytes. Inspect the actual attempt, clearance, source/freeze, execution and postrun records alongside the launcher and launcher review; reconcile shared identities, effect ordering and timeout correction without replaying anything. Reconcile current main and ownership first. The owned-storage finite-model lane retains separate ownership, and no recipient has accepted this next unit.
