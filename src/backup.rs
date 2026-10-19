//! Same-schema local snapshot export. No in-place restore or migration.
use crate::{Error, Result, Store};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct BackupExport {
    pub database_version: i64,
    pub sqlite_version: String,
    /// Raw file SHA-256, not a native domain-separated object ID.
    pub file_sha256: String,
    pub file_bytes: u64,
    pub objects: u64,
    pub events: u64,
    pub last_sequence: u64,
}

impl Store {
    /// Publishes one consistent SQLite snapshot at a new file name. The trusted
    /// destination directory must not be concurrently repurposed as a live DB.
    /// An error or lost reply after linking may leave a complete published file;
    /// inspect it rather than retrying with overwrite. Unix only for now.
    pub fn backup_export(&mut self, path: impl AsRef<std::path::Path>) -> Result<BackupExport> {
        #[cfg(unix)]
        {
            export(self, path.as_ref())
        }
        #[cfg(not(unix))]
        {
            let _ = path;
            Err(Error::Invalid(
                "backup export currently requires Unix".into(),
            ))
        }
    }
}

#[cfg(unix)]
fn export(store: &mut Store, path: &std::path::Path) -> Result<BackupExport> {
    use crate::store::{APPLICATION_ID, DATABASE_VERSION, failpoint};
    use rusqlite::{
        Connection, TransactionBehavior,
        backup::{Backup, StepResult},
    };
    use sha2::{Digest, Sha256};
    use std::{
        fs::{self, File, OpenOptions},
        io::Read,
        os::unix::fs::OpenOptionsExt,
        thread,
        time::{Duration, Instant},
    };

    let name = path
        .file_name()
        .ok_or_else(|| Error::Invalid("backup needs a new file name".into()))?;
    let parent = path
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(std::path::Path::new("."));
    let parent = parent.canonicalize()?;
    let target = parent.join(name);
    for suffix in ["", "-wal", "-shm", "-journal"] {
        let mut candidate = target.as_os_str().to_os_string();
        candidate.push(suffix);
        match fs::symlink_metadata(candidate) {
            Ok(_) => {
                return Err(Error::Invalid(
                    "backup destination or SQLite sidecar already exists".into(),
                ));
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            Err(e) => return Err(e.into()),
        }
    }
    // Preflight directory sync support before publication; final sync can still fail.
    let directory = File::open(&parent)?;
    directory.sync_all()?;
    let stage = tempfile::Builder::new()
        .prefix(".continuum-backup-")
        .tempdir_in(&parent)?;
    let staged_file = stage.path().join("snapshot.db");
    let file = OpenOptions::new()
        .read(true)
        .write(true)
        .create_new(true)
        .mode(0o600)
        .open(&staged_file)?;
    drop(file);
    let mut destination = Connection::open(&staged_file)?;
    destination.pragma_update(None, "synchronous", "FULL")?;
    let transaction = store
        .connection
        .transaction_with_behavior(TransactionBehavior::Deferred)?;
    // The first read fixes this WAL snapshot before any incremental copy steps.
    let cut = counts(&transaction)?;
    let start = Instant::now();
    {
        let backup = Backup::new(&transaction, &mut destination)?;
        loop {
            if start.elapsed() > Duration::from_secs(30) {
                return Err(Error::Invalid(
                    "backup copy exceeded 30-second elapsed limit (checked between steps)".into(),
                ));
            }
            let result = backup.step(64)?;
            failpoint("backup_after_copy_step");
            match result {
                StepResult::Done => break,
                StepResult::Busy | StepResult::Locked => thread::sleep(Duration::from_millis(10)),
                StepResult::More => {}
                _ => return Err(Error::Invalid("unsupported backup step result".into())),
            }
        }
    }
    transaction.rollback()?;
    if counts(&destination)? != cut {
        return Err(Error::Invalid(
            "backup cut counts do not match destination".into(),
        ));
    }
    let application: i64 = destination.pragma_query_value(None, "application_id", |r| r.get(0))?;
    let version: i64 = destination.pragma_query_value(None, "user_version", |r| r.get(0))?;
    if application != APPLICATION_ID || version != DATABASE_VERSION {
        return Err(Error::UnsupportedDatabase(
            "backup database identity mismatch".into(),
        ));
    }
    let integrity: String = destination.query_row("PRAGMA integrity_check", [], |r| r.get(0))?;
    if integrity != "ok"
        || destination
            .prepare("PRAGMA foreign_key_check")?
            .exists([])?
    {
        return Err(Error::Invalid(
            "backup failed SQLite integrity checks".into(),
        ));
    }
    // The published artifact must be a standalone file, with no WAL dependency.
    let mode: String = destination.query_row("PRAGMA journal_mode=DELETE", [], |r| r.get(0))?;
    if mode != "delete" {
        return Err(Error::Invalid("backup could not leave WAL mode".into()));
    }
    destination.close().map_err(|(_, error)| error)?;
    let mut file = File::open(&staged_file)?;
    file.sync_all()?;
    let mut digest = Sha256::new();
    let mut buffer = [0u8; 65536];
    loop {
        let count = file.read(&mut buffer)?;
        if count == 0 {
            break;
        }
        digest.update(&buffer[..count]);
    }
    let report = BackupExport {
        database_version: DATABASE_VERSION,
        sqlite_version: rusqlite::version().to_owned(),
        file_sha256: format!("{:x}", digest.finalize()),
        file_bytes: file.metadata()?.len(),
        objects: cut.0,
        events: cut.1,
        last_sequence: cut.2,
    };
    failpoint("backup_before_publish");
    // Atomic no-replace publication on a filesystem supporting hard links.
    // Unlike rename(), this cannot replace an existing file or dangling symlink.
    fs::hard_link(&staged_file, &target)?;
    failpoint("backup_after_link");
    // Remove the second name before success: opening an orphan alias read-write
    // would otherwise mutate the published inode. A crash in the link/unlink gap
    // can still leave that alias; orphan stages must only be deleted, never opened.
    fs::remove_file(&staged_file).and_then(|()| File::open(stage.path())?.sync_all())
        .map_err(|e| Error::Invalid(format!(
            "backup may be published at {}; staging unlink/sync failed: {e}; hash it or inspect a separate copy", target.display()
        )))?;
    directory.sync_all().map_err(|e| {
        Error::Invalid(format!(
            "backup may be published at {}; directory sync failed: {e}; hash it or inspect a separate copy",
            target.display()
        ))
    })?;
    failpoint("backup_after_publish");
    // TempDir removes only this invocation's private staging path. A process
    // exit may leave an orphan stage; it must never be treated as published.
    drop(stage);
    Ok(report)
}

#[cfg(unix)]
fn counts(connection: &rusqlite::Connection) -> Result<(u64, u64, u64)> {
    let counts: (i64, i64, i64) = connection.query_row(
        "SELECT (SELECT count(*) FROM objects), count(*), coalesce(max(sequence),0) FROM events",
        [],
        |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)),
    )?;
    let convert = |value: i64| {
        u64::try_from(value).map_err(|_| Error::Invalid("negative backup count or sequence".into()))
    };
    Ok((convert(counts.0)?, convert(counts.1)?, convert(counts.2)?))
}
