# Disposable committed-boundary journal

This successor to the framing-only primitive implements `src/journal.rs`. Input source: framing/oracle commit `5890ea50c2b88ea71baadfe22cf512053861c442`, main `c474b0dc9e6f4732d22a1c3f2f4da20df415a2cd`, ADR 0002 and selected design in PR 112. Owner: this continuing Codex engineering session; no overlapping implementation owner observed during fresh reconciliation.

This is a bounded Unix/local-filesystem laboratory, not storage adopted for retained work. It persists opaque payload frames. No object type/closure checks, operation deduplication, acceptance transition, receipt, semantic replay, export/restore or migration is implemented yet. Those requirements remain in the [oracle](../oracle/README.md).

## Contract and boundary selection

A directory contains `lock`, `journal`, and `boundary`. Maximum journal image is 1,048,576 bytes; frame payload remains at most 65,536 bytes. Existing directories are never initialized again. Initialization uses exclusive creation, synchronizes the journal and initial boundary, then the directory and parent. Partial initialization is preserved, not automatically repaired. The caller owns a trusted local directory tree; malicious path replacement, symlinks, remote filesystems and uncooperative writers are outside this prototype's contract.

Boundary encoding is exactly 80 bytes: eight ASCII bytes `CTJBD001`, u64 little-endian journal length, 32-byte SHA-256 of the entire journal image, then SHA-256 of `continuum:boundary:v1` plus NUL plus the preceding 48 marker bytes. Missing boundary is an error even when the journal itself decodes. This checksum does not authenticate metadata or detect a coherently replaced older image.

Opening acquires a nonblocking exclusive OS file lock before recovery, held for the handle lifetime. Contention is an error. Readers currently use the same exclusive ownership: there is no concurrent committed-generation reader optimization. Lock release on process exit was exercised. Replacing the lock inode externally defeats cooperative ownership and is out of scope.

Recovery requires no pending boundary, exactly matching journal length and digest, valid boundary checksum, and valid complete chained framing. It exposes no prefix if any check fails. It never truncates, removes pending files, chooses a shorter boundary, rewrites damaged bytes or converts a reread into a durability acknowledgement. Availability is deliberately sacrificed on ambiguous tails: manual inspection and a later explicitly qualified repair protocol are still needed.

Append under that lock:

1. Validate the next bounded image without I/O. Mark the handle poisoned before starting mutation.
2. Append exactly the new frame suffix, then `sync_all` the journal.
3. Exclusively create `boundary.pending`, write the complete next marker, then `sync_all` it.
4. Rename the pending marker over `boundary`, then `sync_all` the repository directory.
5. Update the in-memory records and unpoison the handle; only then return success.

Any I/O error after mutation begins leaves the handle poisoned. Reads and further writes through it refuse. The path is preserved, and no automatic retry occurs. Dropping/reopening can recover a valid published image without knowing whether a reply was delivered; it does not prove an uncertain earlier sync actually succeeded. An interrupted pending publication or unexplained tail refuses even if an older valid prefix exists.

## Declared fault assumptions

The intended process-crash contract assumes cooperative locking, ordered program execution and the local filesystem's successful file/directory sync guarantees. Successful synchronization is assumed to preserve those bytes/namespace updates across the modeled crash. Atomic replacement is assumed to expose an old or new marker, not arbitrary mixed bytes. A failed sync is uncertain; it cannot justify success. Tests below do not emulate block-device persistence, reordering, storage lies or actual failed sync syscalls.

Corruption controls expect integrity refusal. Whole-file suffix loss with a newer boundary refuses, unlike framing alone. A valid older marker paired with newer journal bytes also refuses. Coherent rollback of BOTH journal and matching marker remains undetectable, explicitly demonstrated. Loss of acknowledged synchronized history or wholesale rollback is not solved by this design; an independent monotonic witness would be needed for that stronger fault model. Never silently relabel these assumptions as tested power-loss durability.

The in-process history oracle has no knowledge of these physical assumptions; agreement with it cannot authorize recovering a damaged image.

## Executed Research Delta — 2026-10-19

Linux, Rust 1.91.1, Python 3.14, filesystem reported `ext2/ext3`; no physical-device qualification. Build, formatting, strict Clippy and the existing three Rust framing tests passed. The separately implemented Python boundary reader shares only the published format and the earlier Python frame reader; it does not call the Rust decoder.

Actual subprocess checks in `check_journal.py`, output in [journal-validation.txt](journal-validation.txt):

- Exclusive initialization, six clean initial reopen cases and an independently held OS lock preventing a contender append without file changes.
- Four process exits with no reply: after data sync (74), after pending-marker sync (75), after marker rename before directory sync (77), and after directory sync before reply (76). First two preserve/refuse; latter two recover two exact frames under ordinary process exit on the still-running OS. Rename-before-sync recovery is **not evidence** of durable directory publication under power loss.
- Synthetic uncertain-sync return after append poisons the live handle: same-handle reads and further writes fail. Reopening refuses the unexplained tail. This is injected control flow, not an actual kernel sync failure.
- **265** copied-image missing-file, marker-byte flip, journal-cut and stale-marker controls refused by both readers, with reads and attempted writes leaving every copied byte unchanged. Healthy source directory stays unchanged.
- A coherent rollback control is accepted by both readers, exposing the documented limit rather than counting it as a safety pass.

Reproduce from repository root after building the separate crate:

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/framing/check_journal.py research/owned-authority/framing/target/debug/continuum-journal-framing
```

These tests establish specific process-exit/locking/integrity-refusal behavior in disposable directories. No actual power loss, broad filesystem coverage, hostile caller, comparative performance, provider invocation or recipient acceptance occurred.

Next: encode original v1 objects and complete acceptance outcomes in this journal, check them against the finite oracle and separate SQLite reference, and recover the original historical receipt after lost reply. Then no-overwrite export/restore and a real investigation continuation. Keep the conservative refusal policy until an independently checked repair/availability design changes it.
