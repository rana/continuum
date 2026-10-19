#![cfg(unix)]

use continuum_core::{AcceptRequest, Object, Outcome, Receipt, SnapshotEntry, Store};
use sha2::{Digest, Sha256};
#[cfg(feature = "fault-injection")]
use std::process::Command;
use std::{
    fs,
    os::unix::fs::{MetadataExt, PermissionsExt, symlink},
};
use tempfile::tempdir;

fn fixture(path: &std::path::Path) -> (Store, AcceptRequest, Receipt) {
    let mut store = Store::open(path).unwrap();
    // More than one 64-page backup step, including in interruption tests.
    let blob = store
        .put(&Object::Blob {
            bytes: vec![42; 1024 * 1024],
        })
        .unwrap();
    let root = store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "a".into(),
                blob,
            }],
        })
        .unwrap();
    let second = store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "b".into(),
                blob,
            }],
        })
        .unwrap();
    let initial = AcceptRequest {
        acceptor: "local".into(),
        target: "main".into(),
        operation_id: "initial".into(),
        expected: None,
        candidate: root,
    };
    let receipt = store.accept(&initial).unwrap().receipt;
    store
        .accept(&AcceptRequest {
            operation_id: "advance".into(),
            expected: receipt.resulting,
            candidate: second,
            ..initial.clone()
        })
        .unwrap();
    let stale = store
        .accept(&AcceptRequest {
            operation_id: "stale".into(),
            ..initial.clone()
        })
        .unwrap();
    assert_eq!(stale.receipt.outcome, Outcome::PreconditionFailed);
    (store, initial, receipt)
}

fn check_copy(
    source: &Store,
    published: &std::path::Path,
    restored: &std::path::Path,
    initial: &AcceptRequest,
    receipt: &Receipt,
) {
    fs::copy(published, restored).unwrap();
    let mut copy = Store::open(restored).unwrap();
    assert_eq!(
        copy.head("local", "main").unwrap(),
        source.head("local", "main").unwrap()
    );
    assert_eq!(
        copy.events("local", "main").unwrap(),
        source.events("local", "main").unwrap()
    );
    let retry = copy.accept(initial).unwrap();
    assert!(retry.replayed);
    assert_eq!(&retry.receipt, receipt);
    let stale = copy.receipt("local", "stale").unwrap().unwrap();
    assert_eq!(copy.accept(&stale.request).unwrap().receipt, stale);
    let root = copy.head("local", "main").unwrap().unwrap().root;
    assert_eq!(copy.get(root).unwrap(), source.get(root).unwrap());
    assert_eq!(
        copy.get(initial.candidate).unwrap(),
        source.get(initial.candidate).unwrap()
    );
    if let Object::Snapshot { entries } = copy.get(root).unwrap() {
        for entry in entries {
            assert_eq!(
                copy.get(entry.blob).unwrap(),
                source.get(entry.blob).unwrap()
            );
        }
    } else {
        panic!("head must retain its snapshot type");
    }
    let changed = AcceptRequest {
        candidate: root,
        ..initial.clone()
    };
    assert!(matches!(
        copy.accept(&changed),
        Err(continuum_core::Error::OperationConflict)
    ));
}

#[test]
fn exports_standalone_snapshot_with_historical_retry_and_raw_digest() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("live.db");
    let (mut source, initial, receipt) = fixture(&db);
    let target = dir.path().join("backup.db");
    let report = source.backup_export(&target).unwrap();
    assert_eq!(
        (report.objects, report.events, report.last_sequence),
        (3, 3, 3)
    );
    assert_eq!(report.database_version, 1);
    assert!(!report.sqlite_version.is_empty());
    let bytes = fs::read(&target).unwrap();
    assert_eq!(report.file_sha256, format!("{:x}", Sha256::digest(&bytes)));
    assert_eq!(report.file_bytes, bytes.len() as u64);
    assert_eq!(
        fs::metadata(&target).unwrap().permissions().mode() & 0o777,
        0o600
    );
    assert!(!dir.path().join("backup.db-wal").exists());
    check_copy(
        &source,
        &target,
        &dir.path().join("restored.db"),
        &initial,
        &receipt,
    );
    assert!(source.backup_export(&target).is_err());
    assert_eq!(fs::read(&target).unwrap(), bytes);
    assert!(source.backup_export(&db).is_err());
}

#[test]
fn rejects_existing_names_sidecars_and_dangling_symlinks_without_overwrite() {
    let dir = tempdir().unwrap();
    let (mut source, _, _) = fixture(&dir.path().join("live.db"));
    for suffix in ["", "-wal", "-shm", "-journal"] {
        let target = dir.path().join(format!("target{}", suffix.len()));
        let collision = dir.path().join(format!("target{}{suffix}", suffix.len()));
        fs::write(&collision, b"must survive").unwrap();
        assert!(source.backup_export(&target).is_err());
        assert_eq!(fs::read(&collision).unwrap(), b"must survive");
        fs::remove_file(collision).unwrap();
    }
    let target = dir.path().join("dangling");
    symlink(dir.path().join("absent"), &target).unwrap();
    assert!(source.backup_export(&target).is_err());
    assert!(
        fs::symlink_metadata(target)
            .unwrap()
            .file_type()
            .is_symlink()
    );
}

#[test]
fn competing_exports_publish_one_complete_file() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("live.db");
    let (source, initial, receipt) = fixture(&db);
    let target = dir.path().join("backup.db");
    let barrier = std::sync::Arc::new(std::sync::Barrier::new(2));
    let handles: Vec<_> = (0..2)
        .map(|_| {
            let db = db.clone();
            let target = target.clone();
            let barrier = barrier.clone();
            std::thread::spawn(move || {
                let mut store = Store::open(db).unwrap();
                barrier.wait();
                store.backup_export(target)
            })
        })
        .collect();
    let results: Vec<_> = handles.into_iter().map(|h| h.join().unwrap()).collect();
    assert_eq!(results.iter().filter(|r| r.is_ok()).count(), 1);
    check_copy(
        &source,
        &target,
        &dir.path().join("restored.db"),
        &initial,
        &receipt,
    );
}

#[cfg(feature = "fault-injection")]
#[test]
fn process_exit_never_exposes_partial_file_and_lost_reply_does_not_allow_overwrite() {
    for boundary in [
        "backup_after_copy_step",
        "backup_before_publish",
        "backup_after_link",
        "backup_after_publish",
    ] {
        let dir = tempdir().unwrap();
        let db = dir.path().join("live.db");
        let (mut source, initial, receipt) = fixture(&db);
        let target = dir.path().join("backup.db");
        let output = Command::new(env!("CARGO_BIN_EXE_continuum"))
            .arg("backup")
            .arg(&db)
            .arg(&target)
            .env("CONTINUUM_FAILPOINT", boundary)
            .output()
            .unwrap();
        assert_eq!(output.status.code(), Some(86), "{boundary}: {:?}", output);
        assert!(output.stdout.is_empty());
        let published = matches!(boundary, "backup_after_link" | "backup_after_publish");
        assert_eq!(target.exists(), published);
        // A killed process can leave a private stage. No stage is a published backup.
        assert!(fs::read_dir(dir.path()).unwrap().any(|entry| {
            entry
                .unwrap()
                .file_name()
                .to_string_lossy()
                .starts_with(".continuum-backup-")
        }));
        if boundary == "backup_after_link" {
            let alias = fs::read_dir(dir.path())
                .unwrap()
                .map(|e| e.unwrap().path())
                .find(|p| {
                    p.file_name()
                        .unwrap()
                        .to_string_lossy()
                        .starts_with(".continuum-backup-")
                })
                .unwrap()
                .join("snapshot.db");
            assert_eq!(
                fs::metadata(&alias).unwrap().ino(),
                fs::metadata(&target).unwrap().ino()
            );
            // Deleting the alias preserves the published file; never open it.
            fs::remove_file(alias).unwrap();
        }
        if published {
            let before = fs::read(&target).unwrap();
            assert!(source.backup_export(&target).is_err());
            assert_eq!(fs::read(&target).unwrap(), before);
        } else {
            source.backup_export(&target).unwrap();
        }
        check_copy(
            &source,
            &target,
            &dir.path().join("restored.db"),
            &initial,
            &receipt,
        );
        assert_eq!(source.events("local", "main").unwrap().len(), 3);
    }
}

#[test]
fn ordinary_validation_failure_publishes_nothing_and_cleans_private_stage() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("live.db");
    let (mut source, _, _) = fixture(&db);
    let connection = rusqlite::Connection::open(&db).unwrap();
    connection
        .pragma_update(None, "foreign_keys", "OFF")
        .unwrap();
    connection
        .execute(
            "UPDATE heads SET root=?1",
            [format!("sha256:{}", "0".repeat(64))],
        )
        .unwrap();
    let target = dir.path().join("backup.db");
    assert!(
        source
            .backup_export(&target)
            .unwrap_err()
            .to_string()
            .contains("SQLite integrity")
    );
    assert!(!target.exists());
    assert!(!fs::read_dir(dir.path()).unwrap().any(|e| {
        e.unwrap()
            .file_name()
            .to_string_lossy()
            .starts_with(".continuum-backup-")
    }));
}
