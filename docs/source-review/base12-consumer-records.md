# Consumer saved records: accounting and selector scope

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Six JSON texts / 33,264 bytes were fully read and parsed, including all eighty intake rows, eight per-record result rows, four arms' file hashes and forty native identities. The [ledger](base12-coverage-consumer-records.json) records exact source identities. No acquisition, fit, encode, decode, native instruction or inference was executed.

## Research Delta: a local selector requires its dictionary

The result stores selector counters as numeric strings. The source resolves them through fixed predictors followed by each arm's serialized coefficient dictionary. Equal ordinal values need not identify equal models across arms; equal models can have different ordinals.

| Arm | Stored selector | Resolved coefficient | Saved count |
| --- | ---: | ---: | ---: |
| Learned | 6 | 5 | 293 |
| Authored four | 6 | 6 | 1,181 |
| Learned | 5 | 10 | 1,403 |
| Full family | 26 | 10 | 1,288 |

All saved selectors resolve legally in their respective dictionaries, and every arm totals 2,544 channel-block selections. Those totals agree with eight records, two channels and 159 blocks per channel, including the short final block. The [validation record](../../research/runs/base12-consumer-records/validation.json) retains every resolved counter.

Continuum should preserve the defining dictionary and parent artifact when projecting a local ordinal or tag. A shorter view that retains only the number can make two different choices appear identical, or obscure that two different numbers name the same operation. This return changes no native identifier format or receipt-view API.

## Saved accounting reconciles at each boundary

Per-record bytes sum to each complete arm after adding its 11/15/15/46-byte common-header/dictionary charge. Each arm's sixteen output hashes match the same validation intake entries, and all eight per-record source-byte totals match intake. The inventory has exactly the source-defined 32 training and eight validation pairs, totaling 78,009,188 bytes; validation totals 15,602,045. No test entry appears. This checks the saved inventory and scoped tool claim, not global absence of other accesses.

Literal framing is 15,602,639 bytes, matching its ten-byte prefix plus each record's source bytes and 73 framing bytes. The external reference records that exact input length and successful framing verification. Learned choices and training time agree between separate records and the final result. The learned payload's raw hash matches model freeze; all six source hashes and protocol hash match acquired source bytes. The training-cost hash remains a declaration here because that payload has not been acquired or read.

Saved net training gains sum to 11,349 bytes, agreeing with before/after-plus-dictionary totals. Original counter arithmetic also agrees: 256 contexts times forty candidates gives 10,240 training calls and 41,943,040 sample evaluations; 2,544 validation blocks times forty gives 101,760 calls and 416,000,000 sample evaluations. These are candidate evaluations rather than distinct source samples, additional trials or per-arm work totals. Greedy choices have not yet been independently replayed from the missing cost rows in this review sequence.

## Recorded scope is narrower than fresh reproduction

The overlap record's 5,167,240 candidate starts agree with eight full validation files and every possible 4,096-frame start. Its zero hash candidates means no full-byte candidate confirmations were needed under that filter. It is a saved, scoped scan result; this unit does not rerun it or extend coverage to shorter spans, channel swaps or the test partition.

The native identity map contains forty encoder entries totaling 7,472 code bytes and exactly the expected fixed/nonduplicate-coefficient set. Fresh decoder-cache identities are absent, as the earlier source review and summaries already disclose. This unit neither regenerates instructions nor compares encoder identities with the separate synthetic run's identities; those receipts are selected next.

The final saved result records pass for the arms and external reference, so the preceding source-derived late-failure possibility is not an observed outcome in this record. Source order and cross-record agreement support a coherent retained account; they do not authenticate execution, rehash excluded signal/encoded payloads, reproduce waveform-derived costs or create an independent decode. Single shared encoding time and same-process decode timings remain outside matched throughput claims.

All six acquired files match pinned Git blobs, lengths and SHA-256. Two additional pinned paths are byte-identical aliases: the result's stdout representation and a second intake receipt. They add no independent observation or direct semantic reading. Cumulative full semantic reading reaches **298 distinct blobs / 1,935,496 bytes**, plus **51 byte-identical alias paths**: 349 covered paths. **5,244 paths / 4,131 distinct blobs** remain without complete semantic-reading claims. The historical acquisition aggregate remains unchanged because its full overlap index is unavailable. Raw private records and operational identifiers are not published; hosted CI checks the public contribution, not private reading or historical execution.

Next bounded unit: three learning-audit/synthetic-receipt texts / 29,899 bytes: the saved-learning audit source, its returned record and the full synthetic check receipt. Inspect the audit's actual method and compare the saved encoder identity set against the synthetic set without executing the audit or native code. Reconcile main and ownership first. No recipient has accepted this next unit; the separate owned-storage lane retains its ownership.
