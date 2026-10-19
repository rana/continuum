# Source-bound local CSV verification

## Research Delta

Question: can a new local verification attempt retain the exact tested source, chosen interpreter, actual input bytes and raw outputs, then travel with the earlier model attempt using the existing checkpoint format? The [fresh receiver inspection](../recorded-attempt-receiver/README.md) identified those missing links; this is a new observation, not a retroactive claim about its historical logs. Starting main: `22dbf5eb46e5a09af2e520eb182bd0fdc6e2e6e7`. Implementation/data checkpoint: `effec4a`. The active Codex coordinator owns this unit, started by the local heartbeat at 2026-10-19 06:32:01.746 UTC (2026-10-18 23:32 Pacific).

## Actual mechanism and scope

[capture.py](capture.py) is a pilot-specific driver for exactly the existing CSV suite and oracle. It does not admit arbitrary commands, add a model runner, change native Rust types, or modify the source under test. The subject is the earlier four-file CSV Snapshot `sha256:5a6627294ea680ff162ce01723f88d8e7cb7b8c4c6fbb54e76e202ea7726b209`. Native Blobs and Snapshot are recreated from exact retained bytes before tests and checked against that known root. Subject file digests are checked again afterward.

Before dispatch, the driver retains its request as a native Blob: source root/file identities, exact fixed worker argv, interpreter identity, full capture-driver and oracle source, explicit environment overlay and instrumentation limits. The request/receipt JSON schema tags are **pilot payloads inside opaque Blobs**, not new core object types or a native claim that the program verifies their meaning.

Each worker loads the unchanged test/oracle module. Its `TemporaryDirectory` hook retains inputs; its narrow subprocess hook copies each actual input **before** executing the CSV child and observes it again afterward. This preserves the valid oracle fixture even though the oracle later overwrites the same file with a ragged record. Every child's exact input, raw stdout and stderr are retained inline as base64 plus length/SHA-256, alongside requested/executed argv, exit code and observed elapsed time. These are 37 input observations, not 37 distinct test cases. Invalid UTF-8, empty files, quoted CRLF/multiline values and significant whitespace survive without text normalization.

The hook deliberately resolves `python3` to the worker's identified absolute `sys.executable` and records both forms. That is an explicit chosen execution profile, not a claim that the earlier historical command resolved identically. Raw byte capture is decoded to UTF-8 only for the original checks' expected `CompletedProcess` interface. Source test/oracle files remain unchanged. The worker records the chosen executable's resolved path/digest/version and observed non-stdlib module origins after checks. Actual observation included distro startup modules (`_distutils_hack`, `apport_python_hook`, `sitecustomize`) as well as the capture/check modules. These dependencies were recorded, not silently treated as snapshot code or removed. Child startup imports were not exhaustively traced; the executable digest is not a complete OS/stdlib/environment image.

This is trusted local observation under these hooks. It is not authentication, a sandbox, proof against hostile concurrent filesystem mutation, or physical power-loss durability. File hashes are before/after observations. No CPU/RAM reservation, process timeout or performance threshold was configured; the workload was bounded to these fixed small checks and inputs. Timings include capture overhead and establish no comparative performance result.

## Executed results

The [final result](result.json) records:

- **11 unittest tests** passed, invoking 28 CSV subprocesses.
- **Nine oracle cases** passed, invoking nine CSV subprocesses.
- All **37 actual child inputs and raw outputs** were retained in the [receipt](verification-receipt.json.gz).
- The source remained unchanged, and both stage workers identified the same selected interpreter executable digest as the request.
- A checkpoint now carries **two distinct attempts**: the earlier model turn against the historical source, and this new local verification against the completed source.
- Restoring the exact request/receipt/WorkState into a second fresh store reproduced the same context-pack identity. This [restoration](restoration.json) did not rerun tests or inference.

The pack is 5,420 bytes; its verification receipt is 77,194 bytes. The latter exceeds the previous receiver experiment's 65,536-byte retrieval cap, although the native store/import bounds admit it. That is a concrete reason for a later *identified projection* of selected receipt fields, not for discarding full evidence or claiming the pack itself contains all of it.

A `known-count-correction` decision now makes the already-established seven-added/eleven-total correction explicit in context and requires it for handoff. The erroneous historical model reply remains byte-for-byte intact. The new verification receipt is separate from that model response, and neither is promoted into an authenticated actor or semantic truth guarantee.

## Review, failure and rejected approaches

The actual [Claude request](claude-request.json) supplied the initial driver and observed successful result. The [visible response/metadata](claude-response.json) reported `claude-opus-5-5`, medium effort, adaptive thinking, completed `end_turn`, no truncation. It identified a material failure path: a worker exception before writing structured results made the parent discard its raw output while trying to open missing files. The driver now writes raw stage outcomes first and treats absent worker records as absent. A failed receipt is stored before the driver stops; no successful checkpoint is created.

[check_failure_capture.py](check_failure_capture.py) exercises that path end to end. It copies the driver and retained subject into a scratch layout and substitutes **only a scratch oracle** that requests an off-fixture path. The hook raises before that CSV child runs; worker result/children files are absent. The parent preserves raw traceback, a failed receipt and its native Blob identity. Native `get` restored that receipt byte-for-byte, and no success checkpoint existed. The original oracle digest was identical before/after. [Fault results](fault-check/result.json), exact failed request/receipt and raw outcome are retained. This is an intentional test failure, not a failed real CSV requirement or a repeated unknown external action.

The review also raised in-process import origins. The revised driver records actual non-stdlib module paths/digests, confirming the test/oracle modules and revealing distro startup hooks. It does not claim a full imported-code closure or silently bind those modules to the subject Snapshot. The raw original successful request/receipt remain in [initial-pass/](initial-pass/); the revised run has a new operation ID and new evidence. Additional checks were justified by this changed failure/provenance concern, not by treating repeated passes as new independent evidence.

Rejected scopes: rewriting historical results, requiring a multi-user authenticated runner before useful local use, inventing a new native execution record type, or converting this two-stage example into a general scheduler/platform. Native imports/custody remain independent of caller-authored semantics, and slow testing occurs outside native acceptance transactions.

## Evidence and replay

Lossless gzip retains exact request, receipt, import bundle and native CLI outputs. The receipt includes every child input/output inline, so a future recipient does not need the deleted or overwritten temporary paths. Request and receipt files were fetched through native `get` and checked byte-for-byte. Checkpoint and restored-checkpoint directories retain manifests, context, coverage and native verification; duplicate runtime/database/source/put-input files are omitted from this public projection. Earlier public source and the independent Git bundle remain authoritative. Exact driver/oracle text is inside the request, with its digest, including capture-time source before this publication.

Validate the retained bytes without execution:

```sh
python3 research/runs/source-bound-verification/verify_records.py
```

[verification-result.json](verification-result.json) records that check: input/output digests, request linkage, native get equality, source/attempt references, case counts, oracle observations, failure evidence and equal restored packs. It performs no new CSV checks or inference.

For a **new** local observation, provide identified native bytes and matching explicit provenance:

```sh
python3 research/runs/source-bound-verification/capture.py \
  --binary /absolute/path/to/continuum \
  --build-provenance /absolute/path/to/build-provenance.json \
  --output /absolute/path/to/new-run
```

Run `check_failure_capture.py` with the same argument names and another fresh output to check the injected-failure behavior. The examples refuse existing output directories and use only retained public source/local Git bundles; they perform no inference or network request. A new execution gets a new operation ID, timestamps and timings, so its receipt/pack IDs may differ. Only restoring the same exact recorded artifacts is expected to reproduce the same pack.

Native build provenance in this actual run identifies the reused measured CSV-pilot binary; no rebuild or installed worker is claimed. Host/interpreter observations are in the request/receipt; no unchanged Rust gates were rerun locally for this Python-only unit. Hosted CI runs the existing gates, a fresh instrumented capture, the deliberate failure check and the archival verifier with its own build provenance.

Next useful action: let a fresh receiver request a small, explicitly identified view of this receipt while retaining its original Blob ID/digest and omitted-field coverage. Test whether the verification evidence and known correction can be used within the observed host message/retrieval limits. No receiver has accepted the new offer; no general JSON-view API is implemented by this unit. Persistent stores, backup/upgrade and comparative continuation benefit remain open.
