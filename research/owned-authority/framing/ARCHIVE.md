# Exact-image export and fresh restore

The disposable owned store now exports a complete locked journal image and restores it only into a new directory. Sources: semantic store `817214566a211ab6d0c9ad4e8c8208faf9dd411d`, boundary/oracle contracts, ADR 0002 and selected design in PR 112. Owner: continuing Codex engineering session; main/instructions/open PRs reconciled before this disjoint unit. No retained store was modified.

## Export contract

`owned-store export DIRECTORY DESTINATION [FAULT]` opens and semantically validates the source under its existing exclusive process lock. It encodes that exact committed image while retaining ownership; a subsequent source writer cannot alter the cut. The archive is version-specific: eight ASCII bytes `CTJEX001`, u64 little-endian journal length, exact journal bytes, then SHA-256 of `continuum:export:v1` plus NUL plus all preceding archive bytes. Journal maximum is 1 MiB. There is no index, source path, filesystem identity, credential or external process state in the archive.

Publication creates a unique `0600` staging file in the destination parent with exclusive create, writes/synchronizes it, then hard-links to the requested destination. Hard-link creation is atomic and fails if that name already exists; neither file nor directory destinations are replaced. Remove the staging name and synchronize the parent directory before returning success. Same-parent staging avoids cross-device publication. A bounded process-local sequence handles known staging-name collisions; no retry occurs after an uncertain write/link/sync result.

Any failure after staging creation leaves evidence for inspection. In particular, exit/error after linking but before unlinking staging can leave **two names for the same inode**. This is not a completed publication. The valid archive may be restorable while its alias must still be inspected; same-user mutation through that alias is not prevented. Completed publication has no staging alias. No automatic cleanup, replacement, stale-stage scavenging or inference of remote success is performed. Repeated failed exports can leave disk growth; this is an explicit operability cost.

## Restore contract

`owned-store restore NEW_DIRECTORY ARCHIVE [FAULT]` first bounds/validates the archive, framing, all object closure and every complete acceptance outcome. Only then does it exclusively create the destination directory. An existing destination is never overwritten or repaired, even if empty or left by a previous failed restore.

Initialization/restore holds a new cooperative lock and creates a `RESTORING` guard before populating files. It writes/synchronizes the exact journal and computed boundary, synchronizes the directory, removes the guard, synchronizes the directory and its parent, then returns. All ordinary journal openings refuse a present guard. A partial install therefore cannot be mistaken for an intentionally shorter store. Failure preserves the directory and guard/artifacts for inspection; no automatic repair/retry follows.

A ready restored directory is an independent authority with the original objects, head and historical accepted/stale receipts. Its subsequent writes do not update the source or archive. Restore is same-version exact-image reproduction, not merge, newest-history recovery, schema upgrade or migration. The CLI's boolean reply is local completion acknowledgement, not authentication or a portable signed export receipt.

## Executed Research Delta — 2026-10-19

Linux/Rust 1.91.1/Python 3.14. Build, formatting, strict all-target Clippy, three framing tests and the previous semantic/journal checks passed after the installation guard was added. [Archive check output](archive-validation.txt) and binary identity are retained.

Observed in temporary directories:

- Two exact objects and three historical outcomes exported unchanged. Source advances to a fourth outcome after the cut; published bytes stay fixed. Fresh restore has the identical original journal, original source Blob, and independently checked objects/history. All three original requests, including stale rejection, return their exact old receipts without byte changes.
- Export and restore against existing destinations fail without changing them. Two independently started exporters yield exactly one successful destination; source ownership itself may reject a competitor before link publication, so this is not proof that every race reached `link` simultaneously.
- Three export exits: before linking (83, no destination), after linking before staging removal (84, valid archive with link count two), and after unlink/parent sync before reply (85, valid single-link archive). Both published images restore exactly. Complete ordinary export also has link count one.
- Two restore exits: before guard removal (81, opening refuses) and after directory/parent sync before reply (82, opening recovers). Neither can be overwritten by repeating restore; artifacts remain unchanged.
- Ten malformed archives, including a physically valid/checksummed archive containing an invalid semantic event, refuse **before target creation**. Source archive bytes remain unchanged.

These are actual local process exits and checks of namespace/content behavior on a running OS. They are not physical power-loss, cross-filesystem/platform, malicious same-user, second-host or device-persistence validation. The [boundary journal's coherent rollback limitation](JOURNAL.md) remains: an older matching journal/boundary/archive is internally valid without a separate monotonic witness. Hashes are integrity checks, not authority or freshness evidence.

Reproduce from repository root:

```sh
cargo build --manifest-path research/owned-authority/framing/Cargo.toml --locked
python3 research/owned-authority/framing/check_archive.py research/owned-authority/framing/target/debug/owned-store
```

Next: use this disposable path for one actual continuation of its development, retaining exact source, exposure, recipient response and observed consequence. A qualitative continuation will not establish comparative model benefit or qualify retained-data adoption. Continue contract/fault review, including real I/O errors and availability costs, independently of that use.
