# Recovered acknowledgement requires fresh barriers

The owned journal now performs fresh startup synchronization before exposing recovered records, including an exact historical retry. Reading valid bytes after a prior uncertain sync does not itself establish a completed durability barrier.

Sources: owned journal/successor `a739c4c345d3c0a4f1e4a1f070c4d6b5a7048a36`, canonical object source at main `91c98ce88eca66b807c11a265c1d8c70180eadce`, ADR 0002 and the selected successor design in PR 112. Owner: this continuing Codex engineering session. Fresh main, instructions and open PRs were reconciled; no overlapping implementation owner was observed. No retained store was modified and no provider call was made.

## Actual gap and correction

Before this change, opening acquired ownership and checked the boundary/framing, but did not synchronize recovered state. An exact retry returned its stored receipt without a new append. If an earlier operation had installed its marker but received an uncertain directory-sync error, the new process could acknowledge that result after merely rereading it.

Opening now holds the existing exclusive lock, validates the physical image, and completes these barriers before returning any Journal handle: journal file, boundary file, repository directory, and repository parent directory. The parent covers a previously uncertain initialization/restore namespace publication. Any error returns before the Store or cached records are exposed. The normal semantic replay then still verifies all objects and receipts. No format, operation identity, global sequence or historical receipt changes.

This adds four synchronization calls to each open, including reads. That startup cost and availability tradeoff are explicit; concurrent read-only optimization remains unimplemented. Fresh barriers do not repair corrupt/missing/pending images or detect coherent rollback, and assume the filesystem honors successful synchronization. Old valid archives remain readable without migration.

## Discriminating experiment

`fail_sync.c` is an original, temporary-built, single-threaded Linux libc interposer. It counts/logs `fsync` calls by actual descriptor path. At one selected call it returns `-1`/EIO without invoking underlying fsync; other calls reach the real function. It is loaded **only into our own disposable CLI subprocesses**, not upstream/native artifacts. Raw temporary paths stay local; retained JSON records resource roles. This is synthetic failure at the real API boundary, not an actual kernel/device EIO, persistence simulator or physical power-loss experiment.

A fixture creates two original v1 objects and evaluates a new request. The journal append and marker-file sync succeed, but the post-rename directory sync is injected to fail. The caller receives an error without a reply. Recovered bytes contain the complete original outcome.

[Actual before/after result](result.json):

- The **before** binary has the same SHA-256 as the measured binary in the earlier [actual successor record](../../runs/owned-successor-01/result.json). Its failing commit has three fsync calls, ending with directory EIO. Exact retry, even with failure requested at the first possible fsync, returns sequence-1 historical receipt successfully with **zero fsync calls** and no byte changes. This demonstrates the missing barrier, not observed data loss.
- The **after** binary first makes four successful startup barriers, then its uncertain commit fails at fsync 7, the directory after journal and pending marker. All four injected startup failure positions separately return error and no acknowledgement, preserving bytes. The trace confirms which actual resource failed.
- With no startup injection, the retry completes exactly four successful barriers in journal/boundary/directory/parent order, returns the original receipt with `replayed:true` and appends no bytes. No acceptance event is repeated.

Local formatting, strict all-target Clippy, three framing tests, journal process/corruption controls, semantic/closure checks, eleven archive-negative plus positive controls and offline reconstruction of both real successor archives pass with the new code. Historical validation files retain their original build hashes and observations.

## Reproduce

From repository root on Linux with a C compiler and dynamically linked native binary:

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/recovery-sync/check.py --binary research/owned-authority/framing/target/debug/owned-store
```

The script builds its interposer in a disposable temporary directory and deletes it afterward. Optional `--before PATH` runs the distinguishing historical control against a separately built `a739c4c` binary; no historical executable is committed. Hosted CI checks the updated failure/refusal/retry behavior, not a fresh historical build. The retained before result is a local observation, not a CI result.

## Research Delta and next work

Finding: valid recovered bytes and stable historical identity were insufficient to justify a new durable acknowledgement after an uncertain prior barrier. The actual boundary-call trace distinguishes the old and corrected behavior without pretending a process restart emulates storage loss. The correction deliberately pays startup synchronization cost rather than inferring stability from a reread.

Scope remains a disposable one-writer Unix laboratory with bounded images, trusted paths, same-version restore and cooperative ownership. This does not qualify physical power loss, filesystem/device lies, coherent rollback, kernel failure handling, multi-host operation, authentication or retained-data adoption. Broader durability claims still need an explicit fault model and independent qualification.

Next: review the complete owned-store contract and operating costs, including these startup barriers and fail-closed availability, before expanding the authority surface. Keep the actual successor evidence intact; a distinct small public investigation and independent fault/recovery review remain useful qualification steps.

The subsequent [focused review](../../runs/owned-journal-review-01/README.md) qualifies this result further: fresh successful calls do not establish recovery after real kernel writeback failure. Primary-source evidence supports that failure class. Persistent pre-write error fencing remains the selected next unit; the synthetic before/after observations above remain valid within their declared model.
