# Owned journal persistence review and remaining error boundary

One focused Claude source review examined the actual journal, archive and semantic-store modules at `ce2e024a6b2f9cd00d3791c39757b14257eca53b`. It established **no concrete source-level flaw within the declared idealized assumptions**. That is neither independent empirical verification nor a readiness certificate. The useful outcomes are an explicit framing invariant and a sharper unresolved writeback-error boundary.

Owner: continuing Codex engineering session. Fresh main, unchanged instructions, open PRs and the design-owner chat were reconciled before this unit. The separately owned design still has no external worker assignment; no message or new scheduler was created. Implementation remains disposable and SQLite remains the retained operational reference.

## Exact consultation

[request.json](request.json) retains the actual caller fields: 24,786 UTF-8 bytes in caller serialization, 23,236 context bytes; SHA-256 `2f7651cf0aba19dd36c8ddc88dfe3e7c121d61d0d216b45f46873f994614d80a`. The parsed fields were submitted once. [source-pins.json](source-pins.json) binds exact three-module bytes. The frame/object codecs, CLI, hosted CI and full test implementations were not supplied. Prior known limitations and the four startup-barrier observations were explicitly supplied, so this was not a blind review.

[submitted.json](submitted.json) remains the pre-call may-have-been-submitted marker. [provider-result.json](provider-result.json) preserves actual visible text and metadata: Claude Opus 5.5, configured US Opus profile, medium effort, adaptive thinking, text only, no server memory, end_turn, no truncation; **10,173 input / 5,982 output tokens**, zero cache tokens. [result.json](result.json) records observed facts and decisions. No hidden reasoning, fabricated execution or automatic retry was retained.

## Codec finding, correction and executed evidence

Claude identified an unexamined dependency: append offsets and the next boundary are computed from re-encoded prior records, so recovery/install must preserve `encode(decode(image)) == image`. It correctly labeled its proposed alternate-encoding trace conditional because it had not seen the frame codec.

The coordinator inspected the actual codec: fixed-width fields, exact magic/ordinal/chain/digest checks, bounded payload and no trailing-data tolerance. No current alternate-encoding counterexample was established. Nevertheless, `decode_canonical` now explicitly verifies exact re-encoding before recovery or installation exposes/uses an image. This enforces the persistence dependency if a future decoder becomes permissive; it does not repair or normalize bytes.

[codec-validation.txt](codec-validation.txt) retains actual local checks: **2,380 finite payload sequences** (0–3 frames; all payloads of length 0–2 over bytes 0/1/255), three prefix cuts per sequence, and a deliberate decoder mutant that strips padding. Every accepted tested prefix re-encodes exactly; the mutant's padded image fails the separate guard. The production decoder already rejects that padding. This is bounded enumeration plus a synthetic mutant, not unbounded fuzz coverage or discovery of a current codec defect.

Formatting, strict all-target Clippy, five Rust tests, process/corruption checks, selected oracle/SQLite semantic traces, archive negative/positive controls, both actual-successor archive reconstructions and current startup-sync interposition checks pass locally with the guard. Hosted CI remains a separate observation.

## Qualified review claims and a consequential remaining gap

One statement in the reply needs precision: installation synchronizes the directory before removing RESTORING, then synchronizes directory **and parent after** removal. It does not synchronize the parent before removing the guard as its prose might suggest. The exact supplied code and actual prior tests remain authoritative.

The reply also warned that a later successful fsync on a fresh descriptor may not repair a previous kernel writeback failure. This was checked against primary sources rather than accepted as model authority. Current Linux errseq documentation says previously seen errors need not be reported to new subscribers. That supports the error-observation limitation, not a guarantee about this host's filesystem. [Linux errseq documentation](https://cdn.kernel.org/doc/html/latest/core-api/errseq.html).

PostgreSQL's 2018 commit explains that some systems can drop dirty data after writeback failure, allowing a later fsync to appear successful without restoring it; its response was to stop further checkpointing. This is historical primary evidence for the failure class, not a reproduction on our current kernel/device. [PostgreSQL commit rationale](https://www.postgresql.org/message-id/E1gObRa-00028l-KU@gemulon.postgresql.org).

Consequently, the previous startup-barrier experiment establishes actual call/refusal ordering under synthetic libc errors. It **does not establish recovery after real kernel writeback errors**. The current implementation has no persistent pre-write error fence; dropping/reopening a poisoned handle can still rely on the stated stronger-than-qualified sync premise. This remains a consequential qualification gap. A successful model review within that premise cannot close it.

Next bounded unit: design and implement a durable pre-write intent/quarantine protocol so uncertain operations cannot be re-acknowledged merely after reopening and resynchronizing. Preserve lost-reply recovery only at an explicitly completed safe boundary, account for fail-closed availability and version compatibility, and exercise the fence with independent failure traces. Actual block-device/kernel fault testing remains separate; no shared-workstation mounts or device manipulation occurred. Retained-data adoption remains excluded.

## Offline custody check

`verify.py` checks request digest, exact supplied source slices and actual complete response/metadata; it never calls a model or edits project files. Rust tests and existing integration scripts exercise the code separately. Earlier uncertain collaborator outcomes remain unknown and were not repeated by this new review.
