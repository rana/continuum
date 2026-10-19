# Bounded receipt-view continuation

## Research Delta

Question: can a fresh receiver use a bounded, explicitly partial view of the new execution receipt to decide what evidence is reusable and what a changed execution environment requires? Starting source: main `95cabd828d2e39ce4b5b680b0dd69a53224cbbd9`, with the [source-bound verification](../source-bound-verification/README.md) and its 5,420-byte native context pack. Owner: the active desktop Codex coordinator, resumed by the 2026-10-19 06:49:01.895 UTC heartbeat. No competing open PR was observed before selection or publication preparation. The older cloud scheduler's live execution status remains unavailable.

The pilot contributed a fixed field projection and two actual Claude receiver turns. The receiver requested the 7,136-byte view of the 77,194-byte receipt, reused the recorded Linux result within its stated scope, and declined to infer Windows/Python 3.11 support. It requested no omitted subtree for that narrow decision. This is a qualitative supplied-context continuation, with no comparison arm or causal saved-work claim. The environment-bound question intentionally has a relatively easy negative portability answer; success does not establish that this view suffices for deeper correctness review.

## Actual view and checks

[receipt_view.py](receipt_view.py) extracts exact JSON values at 20 fixed JSON Pointer paths. It retains source/request/operation identities, observation times, reported outcomes, both worker environments and module digests, commands and local scope. The [view](receipt-view.json) binds its original native Blob ID, raw SHA-256 and 77,194-byte length. These are distinct digest schemes: a native domain-separated Blob ID is not the plain SHA-256 of the raw JSON bytes.

Eight omitted subtree pointers cover the two stages' elapsed times, stdout, stderr and complete children arrays. Those arrays contain all per-child inputs/outputs; no individual assertion or child output was exposed. Every original JSON leaf belongs to exactly one selected or omitted subtree. The original remains losslessly retained in the earlier run, including all 37 child observations. The 16,384-byte view budget refuses overflow without truncation. Unknown fields become explicit omissions. This is a pilot-specific selector for this two-stage schema, not a core object type or general JSON retrieval API.

[verify_records.py](verify_records.py) checks exact regeneration, independent complete/nonoverlapping leaf coverage, original bytes against the earlier native `get` output, exact replay/exposure and actual completion metadata. It rejects changed selected counts, a missing omission entry, changed raw JSON bytes (even semantically insignificant trailing whitespace), and a substituted native reference. Four mutation checks passed. Native `get` is archived executed evidence; the verifier does not implement native hashing or authenticate the originating execution. The prior run's archival verifier also passed locally. No CSV tests or inference run during these archival checks.

Reproduce the view and verify retained data:

```sh
python3 research/runs/bounded-receipt-view/receipt_view.py
python3 research/runs/bounded-receipt-view/verify_records.py
```

The view is independently identifiable through the SHA-256/length in this run's artifact manifest. Its identity was not inserted retrospectively into the earlier WorkState or native handoff. That broader handoff still has no full native acknowledgement from this receiver.

## Exact receiver exposure and result

[Turn one request](turn-1-request.json) supplied only the exact native pack, a new maintainer scenario, retrieval limits and available representation sizes. The Windows/Python 3.11 shipping question is an experiment scenario authored by the coordinator, not an actual user deployment request. The real [response](turn-1-response.json) requested only the verification receipt's view. It explicitly left the historical model receipt uninspected. Its preliminary wish to compare raw digest and native ID was ill-posed; turn two explicitly requested that distinction be addressed, so the final correction is prompted, not independently discovered.

[Turn two request](turn-2-request.json) supplied the exact view, a coordinator sidecar about the archived native-get/raw-byte verification and exact replay of turn one's supplied user/assistant text. It did not supply the raw receipt, source files, request payload or hidden context. The actual [response](turn-2-response.json) correctly separated directly comparable strings from custody assertions that rely on the coordinator. It recorded Python 3.14.4 on Linux, UTF-8 environment variables and distro startup hooks; reused the observation within that scope; and requested new target-environment evidence before a Windows/3.11 support claim. It did not reopen the already recorded seven-added/eleven-total correction.

Both calls completed with returned `claude-opus-5-5`, medium effort, `end_turn`, no truncation; aggregate reported usage was 10,883 input and 4,777 output tokens. These are actual returned usage fields, not a price or comparative efficiency claim. Full tool results and requests are retained; turn two includes exact prior exposure rather than constituting an independent receiver.

The receiver explicitly accepted **only the narrower verification-receipt inspection**, not the broader offered inspection of both receipts. This is model-authored acceptance text; no native acknowledgement, authenticated identity, test execution or deployment is claimed. Its listed Windows concerns are hypotheses, not observed incompatibilities: it had no source bytes and did no target-environment testing. Its suggestion that another run needs separate authority is its own limited-context statement; the coordinator retains the user's existing engineering authorization. No new permission gate was created.

## What changed and next action

The concrete transport problem was avoided for this decision: a 7,136-byte identified view fits the new 16,384-byte budget and prior 65,536-byte cap while the full 77,194-byte receipt remains intact. The view enables environment-scope decisions without exposing individual outcomes. It does not prove that those outcomes are correct, that execution happened as claimed, that another environment works, or that this receipt format improves continuation performance. No general view API is justified yet.

Stop expanding this CSV evidence chain absent a new use requirement. Next useful unit: a bounded SQLite backup/restore experiment that preserves objects, accepted heads and historical exact-retry receipts while a WAL-backed source store is live. Inspect existing transaction/schema behavior and select a supported consistent snapshot mechanism before claiming persistent-store safety. Keep SQLite as baseline; no engine migration, installed worker or full backup/upgrade guarantee is selected. No recipient has accepted that next unit.
