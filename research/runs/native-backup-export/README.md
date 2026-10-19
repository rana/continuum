# Native same-schema backup export

## Research Delta

Question: turn the completed [SQLite backup experiment](../sqlite-online-backup/README.md) into a narrow native export with no destination overwrite and explicit interruption boundaries. Owner: the active desktop Codex coordinator, resumed by the 2026-10-19 07:04:31.912 UTC heartbeat. Input main: `65e6b368beef93e654fc327d56bee7a65206f09f`. The separately published owned-storage research lane remains unchanged; no replacement engine or migration is adopted.

Implemented `Store::backup_export` and `continuum backup DB NEW_FILE` in [the native module](../../../src/backup.rs). See [operation instructions](../../../docs/operations/backup.md) for usage, publication uncertainty and restore limits. A source read transaction pins the cut; SQLite's incremental Backup API copies to private staging. Cut counts, application/schema version, SQLite integrity and foreign keys are checked. The destination leaves WAL mode and closes as a standalone file, is synced and hashed, then hard-linked without replacement. The staging alias is unlinked and synced; the containing directory is synced before success.

The runtime enables rusqlite's backup feature and promotes the already-locked tempfile dependency from tests to production. Native object encodings, schema version and acceptance semantics are unchanged. Unix plus filesystem hard-link/directory-sync support is required. A trusted destination directory cannot be concurrently repurposed as a live database; the file link does not reserve all possible sidecar names against unrelated writers.

## Executed evidence

Formatting, strict all-target/all-feature Clippy and **25 scenarios** passed locally: nine context, nine invariants, two acceptance process-recovery and five new backup cases. The [backup tests](../../../tests/backup_export.rs) cover:

- Standalone copy, raw hash/length, mode 0600, exact Snapshot/Blob bytes, head/events and accepted/rejected historical retries; changed-request conflict still precedes candidate lookup.
- Existing file/source path, SQLite sidecar and dangling-symlink refusal without replacement.
- Two competing exports: one complete winner and one failure.
- Exits after a copy step, before link, after link and after directory sync. No reply is returned. Before publication the final name is absent; afterward it is complete and cannot be overwritten by retry. Tests use a source larger than one 64-page step, copy the published file before opening and retain exact receipt behavior.
- A scratch foreign-key inconsistency: validation fails, no destination appears and ordinary cleanup removes the private stage. The fixture initially attempted corruption while foreign-key enforcement was still enabled; explicitly disabling it on only that scratch connection made the intended failure test meaningful.

The [default-feature CLI smoke](smoke-result.json) separately built and executed the command, exported seven objects/three events at schema version 1 and native SQLite **3.53.2**, and restored the expected head and exact original acceptance receipt in a copied working store. A second export to the same name failed and left published bytes unchanged. Exact command stdout/stderr/exit codes are in [smoke-native-log.json](smoke-native-log.json); raw database files remain outside Git. [Validation](validation.json) identifies the checked source bytes and actual commands. Hosted CI runs the same Rust tests and existing end-to-end pilot checks.

This command's local tests exercise live open connections, publication competition and process exits. The earlier Python experiment separately retains a controlled accepted write between backup steps. No new native concurrent-acceptance interleaving or sustained-write benchmark is claimed here.

## Actual review and changes

[Claude's exact request](claude-request.json) contained the initial module and four passing backup tests plus explicit trusted-directory/platform scope. The [returned response](claude-response.json) reported `claude-opus-5-5`, medium effort, **`max_tokens`, truncated=true**. It is a partial review, not a completed exhaustive audit; the missing continuation was not invoked again. Returned usage was 7,097 input / 8,192 output tokens, not a cost estimate.

A useful returned finding was that an orphan staged file after `link` aliases the published inode. The final implementation unlinks it and syncs its directory before success. A new assertion observes identical inodes at the deliberate link-before-unlink exit and removes only the alias; published content remains intact. A crash in that gap can still leave the alias. Documentation now says never to open orphan stages: reconcile and delete them only. Ordinary temp cleanup is not a guarantee after process death.

The review also warned that opening the published file through `Store::open` changes journal/header state. Inspection instructions and uncertain-publication errors therefore require hashing the file or inspecting a separate copy. No new inspection API was added. The fixed 30-second copy limit remains an explicit initial small-store boundary, checked between steps; its error wording now says elapsed copy limit. It does not cover validation/hashing or promise backup of arbitrarily large stores. A configurable large-store policy is deferred until an actual use requires it. Collision errors remain ordinary errors rather than a new native idempotent operation protocol.

## Limits and next action

File and directory sync calls are implemented; process exits are executed. Neither establishes physical power-loss behavior across arbitrary OS/filesystem/device stacks. Restore is copy-to-fresh-directory inspection, with no live in-place restore, writer fencing, schema upgrade, retention daemon or installed service. The command checks SQLite structure/dependencies; it does not authenticate actors or prove receipt semantics. An old cut omits later acknowledged operations and requires caller reconciliation. A lost reply can mean the final file exists; inspect it without overwrite.

Next practical unit: use the new native export on the actual retained source-bound checkpoint store, restore a copy and compare native context/anchor and historical receipt behavior. This is a backup-use validation of existing evidence, not another CSV inference or implementation round. Reconcile remote ownership before selecting it. No recipient has accepted that next unit; the owned-storage finite model remains separate.
