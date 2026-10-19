# First actual owned-store development continuation

One real supplied-context Claude successor completed a bounded test implementation using original source retained in the disposable owned store. The returned patch applied **unchanged** and passed; the coordinator separately added the positive control Claude recommended. This is a qualitative continuation, not a comparative model-benefit result or retained-data adoption.

Source: `02d491d5057095a92ba21d1d23a4fa7a27b28026`. Owner: this continuing Codex session; no independent implementation owner was observed after reconciling fresh main and open PRs. While preparing the trial, PR 110 merged at `f48f8ef5ea59d497f0a5c6e40c22e4ca7386db44` after both checks passed. PR 111 was retargeted to main, both checks passed and it merged at `91c98ce88eca66b807c11a265c1d8c70180eadce`. PR 113 was retargeted to main. Main was merged non-forcibly into this development branch, preserving those contributions.

## Exact offer, exposure and response

The owned store captured exact `check_archive.py`, an exact `Store::restore` excerpt and the task as Blob/Snapshot objects. Its source snapshot is `sha256:f8742d13ee664144ea5ef4f419e3cbd91b75b1a97e3edd5d8707e910d59b9ba3`. Operation `offer-source` accepted it at sequence 1/generation 1. The complete actual supplied request JSON was also retained as a Blob. [offer.json](offer.json) binds native identities and measured binary SHA-256. [offered.export](offered.export) is an original same-version source/evidence archive, not a machine-code executable or production database. Fresh restoration recovered the original receipt before dispatch.

[request.json](request.json), SHA-256 `16f8ee01a30d1752d7659f6158bdc611386bd34263836131f9727d247c12d1a0`, is 10,459 UTF-8 bytes in the retained caller serialization. Its context is 9,365 UTF-8 bytes. The connector received those parsed fields, not necessarily that JSON wire serialization. It supplied the exact archive-test source, exact restore excerpt, local acceptance receipt, relevant Snapshot codec facts, explicit limitations and one requested test improvement. The successor had no project access, tools, memory, Blob codec source, full event enum or full framing implementation. Native archives were retained locally; their binary contents were not independently read by Claude. URLs/native IDs alone did not deliver additional source.

[submitted.json](submitted.json) was written before invocation and remains a pre-call may-have-been-submitted marker. One actual new call completed, separately from earlier uncertain calls. Actual returned model **claude-opus-5-5**, configured Opus US profile, medium effort, adaptive thinking, text only, no server memory, end_turn, not truncated; **3,923 input / 4,601 output tokens**, zero reported cache tokens. [provider-result.json](provider-result.json) preserves the complete returned visible tool content/metadata; [response.json](response.json) parses its fenced JSON without changing the actual retained text. No hidden reasoning was requested or retained.

The response matched source commit, snapshot and acceptance sequence. It explicitly declined to claim hash verification or authenticated recipient acceptance. These are consistent model-authored references, not a full native handoff acknowledgement, identity proof or evidence of internal understanding.

## Observed consequence and correction

The task was chosen by the coordinator: add an archive with valid container/framing checksums but a Snapshot referencing a missing Blob; restore must fail before target creation. It was not a problem independently discovered by the successor.

[successor.patch](successor.patch) is the exact returned diff. It applied to the supplied source with `git apply`, without edits, and the archive check passed with **11** negative cases; [unchanged-patch-output.txt](unchanged-patch-output.txt) retains stdout. The successor accurately stated that it had not executed the patch.

Claude also identified an exposure gap: without the complete event representation and Blob/chaining codec, a negative case might pass for an encoding reason rather than missing closure. The coordinator checked the actual missing-object error and added an accepted positive archive using the same encoding with a preceding real Blob. [coordinator.patch](coordinator.patch) preserves this separate change; [final-check-output.txt](final-check-output.txt) confirms both rejection-reason and two-object positive controls. Do not attribute that extra implementation or execution to Claude.

The checked final source, actual response/metadata, both patches and observed outputs were captured in a new native snapshot with pass evidence and accepted by `accept-checked-successor` at sequence 2/generation 2. [result.json](result.json) records those identities, exact model metadata, final source/binary/archive digests and limits. [completed.export](completed.export) restores independently with both original and later receipts. Retrying the original offered request after movement still returns its original receipt. The exact tool-request Blob also reconstructs byte-for-byte. No SQLite store was used as authority for this trial.

## Research Delta and limits

Finding: the disposable owned path can carry a real development offer, a completed model contribution, independent caller execution and an accepted successor result while preserving exact historical references through export/restore. The useful delta is one added closure-negative test plus a discriminating positive control. Total model/context preparation and coordinator effort remain material and were not compared against a Git/Markdown handoff.

The task was explicit and the source exposure deliberately selected. This trial does not isolate effects of the native store, formatting, supplied implementation facts or coordinator guidance. No avoided-work, broad productivity, autonomous dispatch, authenticated execution, complete recipient acceptance, power-loss durability, second-host operation or production migration is established. Earlier unknown provider outcomes remain unknown and were not retried; this one successful new-purpose call does not retroactively resolve them or prove global route reliability.

Next priority from implementation inspection: recovered exact retries currently return stored receipts without a new startup durability barrier. Test the case of a prior uncertain marker/directory sync, then qualify/reject recovered acknowledgement explicitly; a successful reread alone is not a completed synchronization barrier. This is a source-identified obligation, not an executed power-loss counterexample. Continue that fault work before any retained-data qualification, then use the engine for a distinct small public investigation.

## Offline verification

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/runs/owned-successor-01/verify.py --binary research/owned-authority/framing/target/debug/owned-store
```

The verifier checks actual request/response/diff custody, restores both source/evidence archives in temporary directories, recovers both receipts and reproduces the exact patch chain against archived source. It never invokes a model, repeats inference, edits project source or infers that a current build digest must equal the historical one. The current archive check separately exercises the new positive/negative behavior.
