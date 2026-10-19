# Native backup export

On Unix, with a trusted local source and destination directory:

```sh
continuum backup work.db /absolute/path/to/new-backup.db
```

The source must already be a supported Continuum database. The destination parent must exist. The destination file and its `-wal`, `-shm` and `-journal` names must be unused; existing files, directories and dangling symlinks are refused. Keep the destination directory under one owner's control and do not concurrently open or repurpose that destination as a live database. A filesystem supporting hard links and directory synchronization is required. Other platforms are currently refused.

A successful JSON reply reports database schema version, actual native SQLite runtime version, raw file SHA-256, file length, object count, event count and last acceptance sequence at the pinned cut. The raw digest is not a domain-separated native object ID. This command does not authenticate evidence or check the semantic truth of receipts.

## Snapshot and publication

The command pins a source read transaction, incrementally copies through SQLite's Online Backup API into a private sibling staging directory, checks the cut counts, database identity, SQLite integrity and foreign keys, and converts the destination to a closed standalone database in DELETE journal mode. It syncs and hashes that file before publishing it through an atomic hard link that cannot replace an existing destination. The staging alias is unlinked and its directory synced, then the containing directory is synced before success is returned. Published files have mode `0600`.

A 30-second elapsed budget is checked between 64-page copy steps, with short pauses on busy/locked outcomes. It is not a timeout for validation, hashing, filesystem operations or the whole command. A pinned reader may retain WAL history while writers continue, so source disk headroom still matters. No sustained-load or WAL-growth guarantee is established.

A process exit before the link leaves no published destination; it may leave an orphan `.continuum-backup-*` private staging directory. Never open an orphan staging database: after a link-before-unlink exit it can share the published inode, so opening it could modify the backup. Orphans may only be deleted after reconciling the invocation; they are never automatically reused. A process exit or error after linking may leave a complete destination even without a successful reply. In particular, directory-sync failure reports that publication may have occurred. Hash the destination or inspect a separate copy before deciding the next action. Do not remove it merely to retry or introduce an overwrite option as recovery.

Ordinary validation failures remove the private stage without publishing. A competing export can win the destination name; the loser leaves the winner intact. Trusted-directory ownership is required because a single file link cannot atomically reserve all possible SQLite sidecar names against unrelated processes.

## Restore boundary

There is no in-place restore command. Preserve the exported file. For inspection or recovery work, copy the complete exported file into a fresh empty directory before opening that copy with the native CLI. Opening it as a working store can create WAL/SHM files and modify SQLite header state. Compare the file digest before opening, then check the relevant object, head, event and receipt identities against the intended recovery cut.

A backup preserves the cut it observed, not subsequent acknowledged operations. A later caller may hold a receipt or candidate missing from that cut. Reconcile that history before continuing writes; exact retry applies only to operations retained in the restored history. No schema migration, automatic worker activation, fencing against a still-running source writer, retention schedule or installed backup service is supplied.

The process-interruption tests establish local process-exit behavior. File and directory sync requests remain subject to OS/filesystem/device behavior; they are not empirical physical power-loss validation. The [native export run record](../../research/runs/native-backup-export/README.md) retains the executed checks and review; the earlier [online-backup experiment](../../research/runs/sqlite-online-backup/README.md) establishes the pinned-cut interleaving and main-file-only negative control.
