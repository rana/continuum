#![cfg(feature = "fault-injection")]

use continuum_core::{AcceptRequest, Object, Outcome, SnapshotEntry, Store};
use std::{fs, process::Command};
use tempfile::tempdir;

fn process_death_at(boundary: &str, should_be_committed: bool) {
    let dir = tempdir().unwrap();
    let database = dir.path().join("recovery.db");
    let request_path = dir.path().join("request.json");
    let request = {
        let mut store = Store::open(&database).unwrap();
        let a_blob = store
            .put(&Object::Blob {
                bytes: b"A".to_vec(),
            })
            .unwrap();
        let b_blob = store
            .put(&Object::Blob {
                bytes: b"B".to_vec(),
            })
            .unwrap();
        let a = store
            .put(&Object::Snapshot {
                entries: vec![SnapshotEntry {
                    path: "source".into(),
                    blob: a_blob,
                }],
            })
            .unwrap();
        let b = store
            .put(&Object::Snapshot {
                entries: vec![SnapshotEntry {
                    path: "source".into(),
                    blob: b_blob,
                }],
            })
            .unwrap();
        let initial = AcceptRequest {
            acceptor: "local".into(),
            target: "main".into(),
            operation_id: "initial".into(),
            expected: None,
            candidate: a,
        };
        let expected = store.accept(&initial).unwrap().receipt.resulting;
        AcceptRequest {
            operation_id: "interrupted".into(),
            candidate: b,
            expected,
            ..initial
        }
    };
    fs::write(&request_path, serde_json::to_vec(&request).unwrap()).unwrap();
    let output = Command::new(env!("CARGO_BIN_EXE_continuum"))
        .arg("accept")
        .arg(&database)
        .arg(&request_path)
        .env("CONTINUUM_FAILPOINT", boundary)
        .output()
        .unwrap();
    assert_eq!(
        output.status.code(),
        Some(86),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        output.stdout.is_empty(),
        "the caller must not receive a reply"
    );
    let mut recovered = Store::open(&database).unwrap();
    let original_receipt = recovered.receipt("local", "interrupted").unwrap();
    assert_eq!(original_receipt.is_some(), should_be_committed);
    if !should_be_committed {
        assert_eq!(recovered.head("local", "main").unwrap(), request.expected);
        assert_eq!(recovered.events("local", "main").unwrap().len(), 1);
    }
    let retry = recovered.accept(&request).unwrap();
    assert_eq!(retry.replayed, should_be_committed);
    assert_eq!(retry.receipt.outcome, Outcome::Accepted);
    if let Some(original_receipt) = original_receipt {
        assert_eq!(retry.receipt, original_receipt);
    }
    assert_eq!(
        recovered.head("local", "main").unwrap(),
        retry.receipt.resulting
    );
    assert_eq!(retry.receipt.resulting.unwrap().root, request.candidate);
    assert_eq!(recovered.events("local", "main").unwrap().len(), 2);
}

#[test]
fn process_death_before_commit_leaves_neither_transition_nor_receipt() {
    process_death_at("before_commit", false);
}

#[test]
fn process_death_after_commit_before_reply_reconciles_original_receipt() {
    process_death_at("after_commit", true);
}
