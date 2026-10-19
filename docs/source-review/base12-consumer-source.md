# Consumer source: freeze order, costs and partial completion

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Six consumer sources / 38,089 bytes were fully read and parsed as syntax: checker, codec, corpus, learner, native predictor and runner. All six match the frozen check-summary hashes. The [ledger](base12-coverage-consumer-source.json) records exact paths and identities. No source was imported, compiled as a callable, executed or disassembled; no dataset or model was invoked.

## Research Delta: bind the freeze to its actual sequence

The runner writes pre-run metadata, verifies intake, fits on training records, saves training costs/learned choices and then writes the model-freeze record. Only afterward does it run the train/validation overlap scan and load validation records for numerical encoding. Source locations are retained in the [validation record](../../research/runs/base12-consumer-source/validation.json): fit at line 26, freeze at 30, overlap at 36 and validation loading at 37.

Intake verification reads all selected file bytes and structural headers before fitting. The learner's fitting loop uses the training partition only; validation numerical encoding follows the freeze. This supports the protocol's qualified exposure order, not a claim that validation bytes were unseen by all code. The freeze consists of ordinary file writes and hashes; source ordering alone does not establish crash-durable publication, protection from hostile path mutation or historical compliance by itself.

The greedy selector charges one byte for each added coefficient and stops without a strict positive net saving. It uses ascending coefficient order to break equal-gain ties. The encoder evaluates the union of candidates once per channel block and shares results across arms; therefore its joint time cannot become a per-arm throughput measurement. Each arm's decoder creates a fresh kernel cache in the same process, rather than a separately authored decoder or a fresh OS process.

## Research Delta: budget the serialized unit

The codec's partition cost includes its parameter byte and padded bit length, and the serializer checks that estimate against produced bytes. Predictive choices and raw fallback use the same block framing; raw wins equal payload-cost ties. A full 4,096-sample raw channel block has 6,144 payload bytes and three selector/length bytes. The common archive prefix is eleven bytes, with the coefficient dictionary charged once: 11/15/15/46 bytes for the reported four arms when learned selects four.

The native predictor clips predictions to signed-12 range. Under validated history/sample bounds, the largest scaled sample difference is at most 98,280; its rounded division by twelve is at most 8,190 before adding history and clipping. Residuals then lie in [-4,095,4,095], with folded maximum 8,190. The decoder checks reconstructed sample range before storing subsequent history. These are original integer bounds and source inspection under the caller contract, not a native machine-code proof or dynamic execution result.

The corpus scanner compares full paired bytes after its short-hash filter. Training anchors are 4,096 frames apart and validation candidates advance by one frame, matching the stated minimum guaranteed span of 8,191 frames. Candidate/match caps fail rather than return a clean overlap result. This source trace still does not reproduce the historical overlap outcome. Source/data paths and resource supervision retain their trusted-local assumptions; the scripts do not establish general adversarial isolation.

## Research Delta: final-result absence leaves an effect question

Each native arm's stream is written and decoded before the external Zstandard version query and gate at lines 57/59. The final `RESULTS.json` is written at line 80, only after successful external compression and framing verification. A late missing/mismatched reference or external failure could therefore leave fitted models and native arm outputs without a final result file.

That is a source-derived possibility, not an observed historical failure. It explains why a continuation must inspect intermediate evidence and attempt state before deciding to repeat work. A successful earlier stage, a failed later prerequisite and an absent final acknowledgement are separate facts. Continuum's retained worker-failure evidence is useful precisely because it need not depend on a worker producing its final result; this return adds no new runner behavior or recovery claim.

All **40/40 lineage destination payloads** now match declared size, Git blob and raw SHA-256 through 38 acquired paths plus two pinned vendor aliases. The native vendor pins match those already acquired blobs. This closes current custody for that declared file map, not independent verification of original PR completeness, missing attachments or full historical run outputs. The original archive and full synthetic report identified earlier remain unrecovered.

Cumulative full semantic reading reaches **292 distinct blobs / 1,902,232 bytes**, plus **49 byte-identical alias paths**: 341 covered paths. **5,252 paths / 4,137 distinct blobs** remain without complete semantic-reading claims. The historical acquisition aggregate remains unchanged because its overlap index is unavailable. Raw private sources and operational identifiers remain outside this public report. Hosted CI validates the public contribution and existing repository behavior, not private reading or historical execution.

Next bounded unit: six saved run JSON records / 33,264 bytes covering result, learned choices, model freeze, pre-run metadata, overlap and intake. Reconcile recorded identities, arm accounting and exposure claims against this source without rerunning acquisition, fitting, encoding or decoding. Reconcile main and ownership first. No recipient has accepted this next unit; the separate owned-storage lane retains its ownership.
