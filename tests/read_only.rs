use continuum_core::{AcceptRequest, Error, Object, SnapshotEntry, Store, context};
use rusqlite::Connection;
use serde_json::{Value, json};
use std::{
    fs,
    path::Path,
    process::{Command, Output},
};
use tempfile::tempdir;

fn invoke(db: &Path, command: &str, args: &[String]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_continuum"))
        .arg(command)
        .arg(db)
        .args(args)
        .output()
        .unwrap()
}

fn fixture(path: &Path) -> (Store, AcceptRequest, continuum_core::ObjectId) {
    let mut store = Store::open(path).unwrap();
    let blob = store
        .put(&Object::Blob {
            bytes: b"read-only fixture\n".to_vec(),
        })
        .unwrap();
    let root = store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "source.txt".into(),
                blob,
            }],
        })
        .unwrap();
    let request = AcceptRequest {
        acceptor: "local".into(),
        target: "main".into(),
        operation_id: "initial".into(),
        expected: None,
        candidate: root,
    };
    store.accept(&request).unwrap();
    (store, request, blob)
}

#[test]
fn all_eight_cli_reads_work_while_writer_reservation_remains_held() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("work.db");
    let (mut store, request, blob) = fixture(&db);
    let state = json!({"schema":context::WORK_STATE_SCHEMA,"id":"work:one","source_snapshot":request.candidate,
        "objective":{"id":"objective:one","statement":"Read consistently.","done_when":"Reads complete.","constraints":[]},
        "attempts":[],"decisions":[],"uncertainties":[],
        "handoff":{"id":"handoff:one","from_worker":"sender","to_worker":"receiver","scope":"Inspect.","required_decision_ids":[]}});
    let state = store
        .put(&Object::Blob {
            bytes: serde_json::to_vec(&state).unwrap(),
        })
        .unwrap();
    let state_root = store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "state.json".into(),
                blob: state,
            }],
        })
        .unwrap();
    let accepted = store
        .accept(&AcceptRequest {
            expected: store.head("local", "main").unwrap(),
            candidate: state_root,
            operation_id: "state".into(),
            ..request.clone()
        })
        .unwrap();
    let pack = context::prepare_context(
        &mut store,
        &context::PrepareContextRequest {
            schema: context::PREPARE_CONTEXT_SCHEMA.into(),
            work_state: state,
            max_bytes: 16000,
            anchor: Some(context::AcceptanceAnchor {
                acceptor: "local".into(),
                target: "main".into(),
                expected: accepted.receipt.resulting.unwrap(),
                work_state_path: "state.json".into(),
            }),
        },
    )
    .unwrap();
    let ack = json!({"schema":context::CONTEXT_ACKNOWLEDGEMENT_SCHEMA,"id":"ack:one","context_pack":pack.context_pack,
        "handoff_id":"handoff:one","recipient_worker":"receiver",
        "included_ids":pack.manifest.included.iter().map(|r|r.id.clone()).collect::<Vec<_>>(),
        "omitted_ids":pack.manifest.omitted.iter().map(|r|r.id.clone()).collect::<Vec<_>>(),"note":"Reference check only."});
    let ack = context::acknowledge_handoff(&mut store, &serde_json::to_vec(&ack).unwrap())
        .unwrap()
        .acknowledgement;
    let commands = [
        ("get", vec![blob.to_string()]),
        ("head", vec!["local".into(), "main".into()]),
        ("receipt", vec!["local".into(), "initial".into()]),
        ("events", vec!["local".into(), "main".into()]),
        ("inspect-context", vec![pack.context_pack.to_string()]),
        ("verify-context", vec![pack.context_pack.to_string()]),
        (
            "verify-current-context",
            vec![pack.context_pack.to_string()],
        ),
        ("verify-handoff", vec![ack.to_string()]),
    ];
    let before: Vec<_> = commands
        .iter()
        .map(|(name, args)| invoke(&db, name, args))
        .collect();
    let writer = Connection::open(&db).unwrap();
    writer.execute_batch("BEGIN IMMEDIATE").unwrap();
    for ((name, args), baseline) in commands.iter().zip(before) {
        assert!(baseline.status.success(), "{name}: {:?}", baseline);
        let held = invoke(&db, name, args);
        assert!(held.status.success(), "{name}: {:?}", held);
        assert_eq!(held.stdout, baseline.stdout);
        assert!(!writer.is_autocommit()); // Completion occurs before release; no speed threshold.
    }
    writer.execute_batch("ROLLBACK").unwrap();
}

#[test]
fn pinned_snapshot_stays_consistent_and_reopen_observes_later_commit() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("work.db");
    let (mut writer, initial, _) = fixture(&db);
    let first = writer.head("local", "main").unwrap();
    let mut reader = Store::open_existing_read_only(&db).unwrap();
    let advance = AcceptRequest {
        expected: first,
        operation_id: "later".into(),
        ..initial
    };
    let later = writer.accept(&advance).unwrap().receipt;
    assert_eq!(reader.head("local", "main").unwrap(), first);
    assert!(reader.receipt("local", "later").unwrap().is_none());
    assert_eq!(reader.events("local", "main").unwrap().len(), 1);
    assert!(
        reader
            .put(&Object::Blob {
                bytes: b"must not write".to_vec()
            })
            .is_err()
    );
    assert_eq!(reader.head("local", "main").unwrap(), first);
    drop(reader);
    let reopened = Store::open_existing_read_only(&db).unwrap();
    assert_eq!(reopened.head("local", "main").unwrap(), later.resulting);
    assert_eq!(reopened.receipt("local", "later").unwrap(), Some(later));
}

#[test]
fn rejects_missing_empty_unrelated_future_and_corrupt_objects_without_initializing() {
    let dir = tempdir().unwrap();
    let missing = dir.path().join("missing.db");
    assert!(Store::open_existing_read_only(&missing).is_err());
    assert!(!missing.exists());
    let empty = dir.path().join("empty.db");
    fs::write(&empty, []).unwrap();
    assert!(matches!(
        Store::open_existing_read_only(&empty),
        Err(Error::UnsupportedDatabase(_))
    ));
    assert!(fs::read(&empty).unwrap().is_empty());
    let db = dir.path().join("work.db");
    let (store, _, blob) = fixture(&db);
    drop(store);
    let before = fs::read(&db).unwrap();
    for (pragma, value) in [("application_id", 7), ("user_version", 99)] {
        let bad = dir.path().join(format!("{pragma}.db"));
        fs::write(&bad, &before).unwrap();
        let connection = Connection::open(&bad).unwrap();
        connection.pragma_update(None, pragma, value).unwrap();
        drop(connection);
        let bytes = fs::read(&bad).unwrap();
        assert!(matches!(
            Store::open_existing_read_only(&bad),
            Err(Error::UnsupportedDatabase(_))
        ));
        assert_eq!(fs::read(&bad).unwrap(), bytes);
    }
    let connection = Connection::open(&db).unwrap();
    connection
        .execute_batch("DROP TRIGGER objects_no_update")
        .unwrap();
    connection
        .execute(
            "UPDATE objects SET canonical=x'00' WHERE id=?1",
            [blob.to_string()],
        )
        .unwrap();
    drop(connection);
    let reader = Store::open_existing_read_only(&db).unwrap();
    assert!(matches!(reader.get(blob), Err(Error::Integrity(_))));
    let output = invoke(&db, "get", &[blob.to_string()]);
    assert!(!output.status.success());
    let error: Value = serde_json::from_slice(&output.stderr).unwrap();
    assert!(error["error"].as_str().unwrap().contains("integrity"));
}

#[test]
fn reads_standalone_delete_journal_backup_without_modifying_main_file() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("work.db");
    let (store, _, _) = fixture(&db);
    drop(store);
    let connection = Connection::open(&db).unwrap();
    let mode: String = connection
        .query_row("PRAGMA journal_mode=DELETE", [], |r| r.get(0))
        .unwrap();
    assert_eq!(mode, "delete");
    drop(connection);
    let before = fs::read(&db).unwrap();
    let mtime = fs::metadata(&db).unwrap().modified().unwrap();
    let output = invoke(&db, "head", &["local".into(), "main".into()]);
    assert!(output.status.success());
    assert_eq!(fs::read(&db).unwrap(), before);
    assert_eq!(fs::metadata(&db).unwrap().modified().unwrap(), mtime);
    assert!(!dir.path().join("work.db-wal").exists());
    assert!(!dir.path().join("work.db-shm").exists());
}

#[cfg(all(unix, feature = "fault-injection"))]
#[test]
fn wal_recovery_permissions_fail_without_writable_fallback() {
    use std::os::unix::fs::PermissionsExt;
    let dir = tempdir().unwrap();
    let db = dir.path().join("source.db");
    let (store, mut request, _) = fixture(&db);
    request.expected = store.head("local", "main").unwrap();
    request.operation_id = "interrupted".into();
    drop(store);
    let request_path = dir.path().join("request.json");
    fs::write(&request_path, serde_json::to_vec(&request).unwrap()).unwrap();
    let killed = Command::new(env!("CARGO_BIN_EXE_continuum"))
        .arg("accept")
        .arg(&db)
        .arg(&request_path)
        .env("CONTINUUM_FAILPOINT", "after_commit")
        .output()
        .unwrap();
    assert_eq!(killed.status.code(), Some(86));
    let wal = dir.path().join("source.db-wal");
    assert!(wal.is_file());
    for writable in [false, true] {
        let copied_dir = dir
            .path()
            .join(if writable { "writable" } else { "restricted" });
        fs::create_dir(&copied_dir).unwrap();
        let copy = copied_dir.join("copy.db");
        fs::copy(&db, &copy).unwrap();
        let copied_wal = copied_dir.join("copy.db-wal");
        fs::copy(&wal, &copied_wal).unwrap();
        let before = fs::read(&copy).unwrap();
        fs::set_permissions(&copy, fs::Permissions::from_mode(0o444)).unwrap();
        fs::set_permissions(&copied_wal, fs::Permissions::from_mode(0o444)).unwrap();
        if !writable {
            fs::set_permissions(&copied_dir, fs::Permissions::from_mode(0o555)).unwrap();
            let permissions_enforced =
                fs::write(copied_dir.join("permission-probe"), b"x").is_err();
            let reader = Store::open_existing_read_only(&copy);
            let shm_exists = copied_dir.join("copy.db-shm").exists();
            let output = invoke(&copy, "head", &["local".into(), "main".into()]);
            fs::set_permissions(&copied_dir, fs::Permissions::from_mode(0o755)).unwrap();
            if permissions_enforced {
                assert!(
                    reader.is_err(),
                    "WAL without shared memory needs recovery access"
                );
                assert!(!shm_exists);
                assert!(!output.status.success());
            } else {
                eprintln!("permission-denial assertion unavailable for privileged test process");
            }
        } else {
            let reader = Store::open_existing_read_only(&copy).unwrap();
            assert_eq!(reader.head("local", "main").unwrap().unwrap().generation, 2);
            assert!(copied_dir.join("copy.db-shm").exists());
        }
        assert_eq!(fs::read(&copy).unwrap(), before);
    }
}
