# Stage-A records: frozen identity and retained correction history

Reviewed 2026-10-19 UTC at private Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. Nine files / 28,461 bytes were fully read: the stage-A integration note, source/preservation manifests and all six direct children of `records/`. The [ledger](base12-coverage-stage-a-records.json) records exact identities. No upstream code, test, acquisition, codec, model or benchmark ran. Private source, Library identifiers and operational payloads are not published.

## Research Delta: a freeze binds content, not an independently verified clock

The source/design freeze records bind reviewed source hashes and disclose their preparation-time acquisition state. Four acquired numerical/test source files match the source freeze; two acquired protocol/wire documents match the design freeze. Each freeze also names two vendor files not rebound in this unit. The runner's literal expected source hashes match the published-pins record.

These are content-consistency checks. They do not independently authenticate the declared timestamps, prove that no earlier exposure occurred, or establish execution of those bytes. A reproducible source identity, a claimed pre-exposure freeze, an execution receipt and recipient acceptance need their corresponding evidence. Continuum should retain those links without treating one as proof of another.

The integration note reports a completed one-record run and distinguishes it from unchanged preparation-time README and UNSENT labels. This resolves how the preserved documents should be read; it is not fresh reproduction here. Its detailed execution and intake receipts are selected next. No historical acquisition or one-run clearance was repeated.

## Research Delta: corrections need to identify what changed

`development-corrections.json` preserves a failed expected packing vector and a later discovery that the fresh-process fixture initially retained RAW rather than owned encoded bytes. These correct different things: an oracle value and the artifact exercised by a test. The saved source freeze further says a later intake tightening left the tested codec/kernel source unchanged.

The recorded failed-source digest is a reference; its original source bytes and complete failed output were not acquired here. Nor does the concise correction ledger recover a complete development chronology. The passing record remains useful within that limit, rather than rewriting the earlier failure as an uninterrupted success.

The saved checks sum to 7,352 assertions. Ten native-code size entries sum to 1,238 bytes, matching the freeze's generated-byte total; eighteen archive fixture entries are retained. We checked that arithmetic and read every counter, identity and fixture entry. We did not regenerate machine code, inspect the referenced fixture archive bytes or rerun a test. The synthetic external-wrapper record is distinct from the later reported real-record result: tool availability and timings from one environment do not establish them in another.

For Continuum, a corrected check should identify whether the implementation, oracle, exercised artifact, environment or intake changed. A successor can then decide which earlier evidence still applies without either discarding everything or inheriting an unsupported pass.

## Research Delta: semantic coverage is not current byte availability

The source manifest contains eighteen entries. Thirteen match acquired payloads from this and the preceding source unit; five remain unchecked here. The larger preservation manifest declares forty-nine files; its membership count reconciles, and fourteen acquired payloads match. Thirty-five entries remain outside the checked payload scope. Those counts are separate bindings across overlapping manifests, not distinct experiments.

Our initial local checker assumed every older semantic-coverage path had a retained byte copy. It stopped at a missing vendor runtime path. The corrected checker requires an existing local payload before hashing and explicitly lists unchecked entries. No missing source was invented and no wider manifest validation was claimed. The [validation record](../../research/runs/base12-stage-a-records/validation.json) preserves that local check correction and each actual binding.

This is a practical continuity lesson: a reading ledger can establish an earlier inspection without establishing present recoverability at a named path. Keep semantic coverage, artifact custody, present retrieval and fresh validation distinct. Unavailable bytes need their actual retrieval route or a declared gap.

## Coverage and next unit

All nine newly acquired byte strings match the pinned tree's Git blob and length; raw SHA-256 was recomputed. One Markdown integration note and eight JSON documents were fully read and the JSON parsed as data. The full real-run evidence archives, raw source payloads and provider logs were not newly audited. Reported resource limits also remain attributed: per-process CPU/address-space limits do not establish aggregate process-tree quotas.

Cumulative direct reading reaches **224 distinct blobs / 1,508,013 bytes**, plus **48 byte-identical alias paths**. This covers 272 paths by reading or byte equality; **5,321 paths / 4,205 distinct blobs** remain without complete semantic-reading claims. Alias directory context is not separately reviewed. The earlier acquisition aggregate remains historical at 539 paths / 530 blobs / 4,536,603 path bytes because its full overlap index was not recovered; new fetches are not blindly added. Hosted CI checks the public contribution, not private reading or historical execution.

Next bounded unit: six unread JSON records / 22,004 bytes under `ecg-codec-stage-a/aum-run-2026-10-16/evidence/`: delivery manifest, intake acquisition receipt, run execution receipt, run input/code record, postrun verification and attempt record. Reconcile fresh main and ownership; read without executing acquisition or replaying the historical run. No recipient has accepted the unit. The separate owned-storage model lane retains its ownership.
