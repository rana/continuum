# Fresh receiver inspection of a recorded attempt

## Research Delta

Question: after exact attempt objects can move into a fresh store, does a genuinely fresh receiver use them to select a useful next action, and where does retrieval still fail? Starting main was `7c35f9a0de7d17bec539ae1508aef72cffb16240`, with no open PR at recovery. The active Codex coordinator owns this bounded experiment and integration. It was started by the local `continue-continuum` heartbeat at 2026-10-19 06:18:01.679 UTC (2026-10-18 23:18 Pacific).

[run-spec.json](run-spec.json) was written before the first model call. It bounded retrieval to three rounds, six native IDs and 65,536 supplied UTF-8 bytes per round. It explicitly rejected a causal claim that stored history prevented repetition: the existing offered handoff already said not to reissue the model call, and there is no comparison arm. This is one arranged continuation, not a model benchmark or a general adoption result.

## Actual exposure and response

The initial input was only the exact [existing rendered pack](../checkpoint-object-import/first/context.jsonl) plus a coordinator retrieval interface. The receiver had no other project conversation, repository tools, shell, or prior model-side memory. Subsequent turns replayed exact visible prior exposure explicitly. This manual relay is an experiment facility, not a shipped native model runner.

| Stage | Actual input beyond prior exposure | Observed result |
|---|---|---|
| First turn | Exact pack and retrieval bounds | Requested request/receipt, WorkState and historical Snapshot plus actual test/oracle/sample-check sidecars. Selected inspecting the existing receipt, without reimplementation. |
| Retrieval 1 / second turn | Four native objects and three requested sidecars; 54,259 bytes | Distinguished returned code from execution evidence. Found the receipt's six-versus-seven test-count error. Requested current Snapshot, sample and oracle source/input. |
| Retrieval 2 / corrected third turn | Two native objects, retained oracle script and clearly labeled reconstructed fixture; 5,077 bytes | Read sample/oracle behavior as consistent, and requested the three applied-source Blobs for comparison. |
| Retrieval 3 / final turn | Three exact native source Blobs; 9,773 bytes | Completed source/record inspection, proposed a new source-bound verification record, and explicitly claimed no fresh test execution. |

The exact requests and visible responses are retained as `turn-*-request.json.gz` and `turn-*-response.json.gz`. Decompression recovers the original UTF-8 JSON bytes; no summaries replace them. All four successful turns reported actual `claude-opus-5-5`, medium effort, adaptive thinking, `end_turn`, no truncation. [Latency and usage](latencies-and-usage.json) retain each call's metadata: reported aggregate input 137,152 tokens and output 6,180. These are supplied-context/replayed-history totals, not financial cost, total upkeep, or an efficiency comparison. The coordinator did not infer billing from tokens.

A first attempt at turn 3 was rejected by the connector because one `prior_exchange[].text` exceeded 32,000 characters. Its exact failed request/error are retained separately. It was a reported parameter-schema failure with no returned model reply/usage metadata. Corrected attempt **3b** moved the exact replayed history into the supported context field, without summarizing it; it was not a blind replay of an uncertain inference outcome. This host-specific limit was absent from the original experiment's 64 KiB per-retrieval bound. Each retrieval fit that bound, but that alone did not guarantee a compatible multi-turn request shape. No connector source or schema was modified.

## What the evidence supports

The receiver did not suggest repeating the original implementation call or reimplement the completed feature. It requested the exact historical record and distinguished authored summaries, model-returned code, retained execution logs, source comparison and fresh execution. The [coordinator evaluation](coordinator-evaluation.json) verifies all returned retrieval text against retained native `get` bytes and sidecar files, the byte limits, and exact equality of all three current-source files to the original receipt's files. It also checks the sample Blob identity is unchanged across historical/current roots. The receiver itself compared text by reading and did not compute hashes; coordinator executable checks provide the stronger byte-equality observation.

The original oracle's temporary input file was not retained with its historical digest. The exact oracle script and a newly derived CSV fixture were supplied with explicit provenance. The reconstruction is not reclassified as an original retained file. The receiver's phrase “unrecoverable” is stronger than established: historical equality is not independently demonstrated by an original retained input/hash; deterministic reconstruction is available. Similarly, its broad “Nobody executed anything” means no new **CSV verification** occurred: the coordinator did execute native retrieval, fixture reconstruction and evidence validation.

The next action it selected is concrete: materialize current source, run checks under identified interpreters, and retain a source-linked execution record. The receiver's concern about an authenticated runner does not make authentication a prerequisite for this trusted local pilot. A clearly scoped local observation with exact source, fixtures, commands and outputs is useful while remaining distinct from authenticated multi-user execution.

## Negative findings and decisions

**Some repeated investigation remained.** The receiver rediscovered the six-versus-seven test-count discrepancy and initially proposed amending that note. The [original pilot record](../independent-csv-pilot/README.md) already corrects it while retaining the raw reply unchanged. That correction was outside this pack/exposure. It is not a new defect, and the historical reply must not be rewritten. The final instruction explicitly required appended corrections. A future authored context should preserve the existing correction or its reference rather than invite another investigation. No new native record type is needed for that.

**A model receipt does not cover subsequent execution.** The imported attempt's request/response describe the model turn. Actual test/oracle outputs live in sidecars not linked by that attempt's native references. The receiver could request them only by description; the coordinator selected the corresponding files. Native object custody worked, but did not make execution evidence discoverable or prove that the later tested tree was the same tree. This supports representing a separate verification attempt using existing source/request/receipt fields, rather than overloading the model receipt or declaring a semantic truth guarantee.

**Exact provider projections are bulky model context.** The retained response contains the same visible payload in both `content` and `structuredContent`, plus nested JSON source files. Replaying the full object preserved custody, but consumed much input and triggered a host message-field constraint. No advantage is demonstrated for showing all wrapper metadata to the receiver; it reported usage/model metadata and anchor/budget fields unused for its code inspection. Their retention/integrity functions remain valid. A future measured view could expose a clearly identified selected JSON field while preserving the original object; this unit does not implement that speculative interface.

**Source comparison is not a historical execution binding.** The exact source equality check is now executable and passes, but the earlier test logs still do not record all interpreter/fixture/source identities in one request/receipt. The receiver proposed a fresh verification record. That is a new experiment justified by a specific missing binding, not a reason to keep rerunning an unchanged suite during this inspection.

## Validation and replay

Run from the repository:

```sh
python3 research/runs/recorded-attempt-receiver/verify_records.py
```

It checks exact supplied exposure, native/sidecar bytes and lengths, retrieval bounds, unchanged sample identity and three source-to-receipt matches. [verification-result.json](verification-result.json) is the observed output. It performs no inference and does not execute the CSV sample. Source/native code was not modified in this unit, and unchanged Rust/CSV suites were not rerun locally. Hosted CI runs its existing checks and this record verifier separately.

`retrieval-N.json` contains the actual model-visible projection; `retrieval-N-native-log.json.gz` preserves native stdout/stderr; custody files retain IDs, lengths and digests. Raw original request/response artifacts remain in their earlier authoritative run. No runtime binaries, databases, credentials or private upstream sources are committed. The capture uses the existing disposable reconstructed store and identified retained native binary; it is not evidence of a persistent installed worker, backup/upgrade path or exclusive scheduling ownership.

Next useful unit: capture **one new source-bound local CSV verification attempt** with interpreter identity and actual retained fixture bytes, then checkpoint it alongside the existing model attempt using existing native object import. Preserve the earlier missing evidence and correction as historical limits. The current heartbeat owns the next active step subject to fresh repository/ownership reconciliation; no other recipient has accepted that follow-up.
