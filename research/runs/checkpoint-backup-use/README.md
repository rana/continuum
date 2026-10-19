# Native backup of the retained checkpoint

## Research Delta

Question: does the native backup export preserve the actual source-bound CSV checkpoint's context, anchor and historical receipt behavior? Owner: the active desktop Codex coordinator, resumed by the 2026-10-19 07:14:01.967 UTC heartbeat. Input main: `6365c7bdb74cbc5501692dd34821ba9d3b509636`. No open competing PR was observed at selection or publication preparation. The separate owned-storage finite-model lane is unchanged.

[run.py](run.py) executed against the retained `source-bound-verification-2/checkpoint/work.db`, using the default-feature binary already checked in the [native export unit](../native-backup-export/README.md). It did not reconstruct a new model response, rerun CSV tests, invoke inference or advance the original checkpoint. It exported a closed 204,800-byte standalone backup and opened only a copied working database in a fresh directory.

## Actual results

The [observed result](observed/result.json) and [full native outcomes](observed/native-log.jsonl.gz) retain:

- All **17 objects**, including both historical/current source roots, both attempts' exact request/receipt Blobs, the WorkState, context/coverage and accepted-state Snapshot. Native `get` validated IDs and returned identical envelopes from source and restored stores for every object.
- Exact **5,420-byte rendered context**, native pack `sha256:4cf78c9e2ee123e7ab1ed1b971491054179e3e0478f99aa7b2be7b64ae6df688`. Its source is the existing CSV Snapshot `sha256:5a6627294ea680ff162ce01723f88d8e7cb7b8c4c6fbb54e76e202ea7726b209`.
- Initial restored anchor **generation 1**, root `sha256:6c120b37853a19551ea255572126268c364cc8a3bce0eeed40edc35b6549e373`; exact current-context verification equaled the source's result.
- The exact original `initial-checkpoint` acceptance receipt, replayed unchanged before and after a controlled head change in the restored copy.
- A deliberately unrelated marker Snapshot accepted at **generation 2 in only the disposable working copy**. Historical pack verification remained exact and reported `stale_at_observation`; current-anchor verification rejected it. Context bytes remained unchanged. This marker is a freshness probe, not new source work or a recipient effect.
- Original source logical inventory and generation-1 head unchanged; published export bytes unchanged throughout restore inspection and probes.

The native export reported SQLite **3.53.2**, one event at acceptance sequence 1, and raw file SHA-256 `2bb952c29c604283a81e902b7797ace593bec791fee01675f99665e69858065c`. This file digest differs from the native domain-separated pack/object IDs. The actual binary digest matches the preceding unit's smoke result; [execution.json](execution.json) identifies the code baseline, command and script bytes. Raw database files, staging and working copies remain outside Git.

## Failure, validation and scope

The first harness assumed that the current-context error string contained the word `stale`. Native rejection actually said `context has no matching current anchor at observation; historical verification remains available`, while historical verification correctly reported `stale_at_observation`. That was a harness wording mismatch, not a native backup or freshness defect. [Initial script, raw completed outcomes and failure description](initial-harness-failure/) remain intact. The corrected attempt used a new output directory and the exact actual expected error; no unknown invocation was repeated. The original store was not advanced by either attempt.

The [archival verifier](verify_records.py) passed: exact source/pack/rendered references, 17 object-envelope pairs, both historical attempt closures, original receipt replays and the restored-copy freshness transition. It executes no native commands, inference or CSV tests. Hosted CI separately runs the new use check on the checkpoint produced earlier in its workflow, with its own runtime, operation IDs and pack identities. Local unchanged Rust tests were not repeated for this Python/data-only unit.

To use an existing single-acceptance checkpoint in a new disposable output directory:

```sh
python3 research/runs/checkpoint-backup-use/run.py \
  --binary /absolute/path/to/continuum \
  --checkpoint /absolute/path/to/checkpoint-directory \
  --output /absolute/path/to/new-run
```

The native backup command must be present in that binary. The input directory must retain `checkpoint.json`, `prepare.json`, `context.jsonl` and `work.db`. The script checks raw identity at start/end; it does not establish reproducible build truth. To verify only the published observation, run `python3 research/runs/checkpoint-backup-use/verify_records.py`.

This is application-level backup-use validation, not a new recipient handoff, authenticated execution or evidence truth guarantee. The source-bound model/test payloads retain their original claims and limits. There is no migration, installed worker, scheduled backup, in-place restore, source-writer fencing or physical power-loss validation. A stale but intact pack cannot authorize current actions; a historical acceptance receipt remains historical even when its exact retry succeeds.

Next practical unit: measure the existing CLI's read behavior while a separate connection holds a writer reservation. ADR 0002 already identifies the open-time writer reservation as an investigation, not a diagnosed bottleneck or approved fix. Use a controlled transaction and read-only SQLite control, retain outcomes, and choose an implementation only if the observation warrants it. Reconcile newer ownership first; do not overlap the independent finite recovery model. No recipient has accepted that next unit.
