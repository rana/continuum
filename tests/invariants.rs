use continuum_core::{
    AcceptRequest, Error, EvidenceOutcome, Head, Object, ObjectId, Outcome, SnapshotEntry, Store,
};
use std::sync::{Arc, Barrier};
use tempfile::tempdir;

fn snapshot(store: &mut Store, bytes: &[u8]) -> ObjectId {
    let blob = store
        .put(&Object::Blob {
            bytes: bytes.to_vec(),
        })
        .unwrap();
    store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "src/main.rs".into(),
                blob,
            }],
        })
        .unwrap()
}

fn request(operation: &str, expected: Option<Head>, candidate: ObjectId) -> AcceptRequest {
    AcceptRequest {
        acceptor: "local".into(),
        target: "main".into(),
        operation_id: operation.into(),
        expected,
        candidate,
    }
}

#[test]
fn exact_binary_source_and_canonical_snapshot_survive_reopen() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("objects.db");
    let source = Object::Blob {
        bytes: vec![0, 255, 128, 10, 13],
    };
    let (source_id, snapshot_id) = {
        let mut store = Store::open(&path).unwrap();
        let source_id = store.put(&source).unwrap();
        let entries = vec![
            SnapshotEntry {
                path: "z.bin".into(),
                blob: source_id,
            },
            SnapshotEntry {
                path: "a.bin".into(),
                blob: source_id,
            },
        ];
        let first = Object::Snapshot {
            entries: entries.clone(),
        };
        let reversed = Object::Snapshot {
            entries: entries.into_iter().rev().collect(),
        };
        assert_eq!(first.id().unwrap(), reversed.id().unwrap());
        (source_id, store.put(&first).unwrap())
    };
    let store = Store::open(&path).unwrap();
    assert_eq!(store.get(source_id).unwrap(), source);
    let Object::Snapshot { entries } = store.get(snapshot_id).unwrap() else {
        panic!("snapshot expected")
    };
    assert_eq!(
        entries.iter().map(|e| e.path.as_str()).collect::<Vec<_>>(),
        ["a.bin", "z.bin"]
    );
}

#[test]
fn canonical_format_rejects_ambiguous_and_unknown_encodings() {
    let object = Object::Blob {
        bytes: b"hello\n".to_vec(),
    };
    let bytes = object.canonical_bytes().unwrap();
    assert_eq!(bytes, b"continuum.object\0\0\x01\x01\0\0\0\x06hello\n");
    // Independently computed with Python hashlib from the literal envelope.
    assert_eq!(
        object.id().unwrap().to_string(),
        "sha256:7f20ef2d93ca7c8efeccaea5ff2e66aad6bf88d8355e390d3a543e011c7e9838"
    );
    assert_eq!(Object::from_canonical(&bytes).unwrap(), object);
    let mut trailing = bytes.clone();
    trailing.push(0);
    assert!(Object::from_canonical(&trailing).is_err());
    assert!(Object::from_canonical(&bytes[..bytes.len() - 1]).is_err());
    let mut future_version = bytes;
    future_version[18] = 2;
    assert!(Object::from_canonical(&future_version).is_err());
    assert!(
        serde_json::from_str::<Object>(r#"{"type":"blob","bytes":[],"unexpected":true}"#).is_err()
    );
}

#[test]
fn retries_return_original_receipt_after_later_head_changes() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("retry.db");
    let (initial_request, original, later) = {
        let mut store = Store::open(&path).unwrap();
        let a = snapshot(&mut store, b"A");
        let b = snapshot(&mut store, b"B");
        let req = request("first", None, a);
        let original = store.accept(&req).unwrap();
        let later = store
            .accept(&request("second", original.receipt.resulting, b))
            .unwrap();
        (req, original, later)
    };
    let mut store = Store::open(&path).unwrap();
    let replay = store.accept(&initial_request).unwrap();
    assert!(replay.replayed);
    assert_eq!(replay.receipt, original.receipt);
    assert_eq!(
        store.head("local", "main").unwrap(),
        later.receipt.resulting
    );
    assert_eq!(store.events("local", "main").unwrap().len(), 2);
}

#[test]
fn operation_id_binds_full_request_within_acceptor_namespace() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("identity.db")).unwrap();
    let root = snapshot(&mut store, b"A");
    let original = request("shared-id", None, root);
    store.accept(&original).unwrap();
    let changed_target = AcceptRequest {
        target: "other".into(),
        ..original.clone()
    };
    assert!(matches!(
        store.accept(&changed_target),
        Err(Error::OperationConflict)
    ));
    assert_eq!(store.head("local", "other").unwrap(), None);
    let separate_acceptor = AcceptRequest {
        acceptor: "another".into(),
        ..original
    };
    assert_eq!(
        store.accept(&separate_acceptor).unwrap().receipt.outcome,
        Outcome::Accepted
    );
    assert_eq!(store.events("local", "main").unwrap().len(), 1);
}

#[test]
fn generation_rejects_aba_even_when_root_bytes_return_to_the_same_value() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("aba.db")).unwrap();
    let a = snapshot(&mut store, b"A");
    let b = snapshot(&mut store, b"B");
    let c = snapshot(&mut store, b"C");
    let first = store.accept(&request("a1", None, a)).unwrap();
    let second = store
        .accept(&request("b2", first.receipt.resulting, b))
        .unwrap();
    let third = store
        .accept(&request("a3", second.receipt.resulting, a))
        .unwrap();
    let stale = store
        .accept(&request("stale-c", first.receipt.resulting, c))
        .unwrap();
    assert_eq!(stale.receipt.outcome, Outcome::PreconditionFailed);
    assert_eq!(stale.receipt.observed, third.receipt.resulting);
    assert_eq!(
        store.head("local", "main").unwrap().unwrap(),
        Head {
            root: a,
            generation: 3
        }
    );
    let retried = store
        .accept(&request("stale-c", first.receipt.resulting, c))
        .unwrap();
    assert!(retried.replayed);
    assert_eq!(retried.receipt, stale.receipt);
}

#[test]
fn competing_connections_have_one_winner_without_lost_updates() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("race.db");
    let (expected, candidates) = {
        let mut store = Store::open(&path).unwrap();
        let a = snapshot(&mut store, b"A");
        let b = snapshot(&mut store, b"B");
        let c = snapshot(&mut store, b"C");
        (
            store
                .accept(&request("base", None, a))
                .unwrap()
                .receipt
                .resulting,
            [b, c],
        )
    };
    let barrier = Arc::new(Barrier::new(2));
    let workers: Vec<_> = candidates
        .into_iter()
        .enumerate()
        .map(|(i, root)| {
            let path = path.clone();
            let barrier = barrier.clone();
            std::thread::spawn(move || {
                let mut store = Store::open(path).unwrap();
                barrier.wait();
                store
                    .accept(&request(&format!("worker-{i}"), expected, root))
                    .unwrap()
            })
        })
        .collect();
    let results: Vec<_> = workers.into_iter().map(|w| w.join().unwrap()).collect();
    assert_eq!(
        results
            .iter()
            .filter(|r| r.receipt.outcome == Outcome::Accepted)
            .count(),
        1
    );
    let winner = results
        .iter()
        .find(|r| r.receipt.outcome == Outcome::Accepted)
        .unwrap();
    let loser = results
        .iter()
        .find(|r| r.receipt.outcome == Outcome::PreconditionFailed)
        .unwrap();
    assert_eq!(loser.receipt.observed, winner.receipt.resulting);
    let store = Store::open(path).unwrap();
    assert_eq!(
        store.head("local", "main").unwrap(),
        winner.receipt.resulting
    );
    assert_eq!(store.events("local", "main").unwrap().len(), 3);
}

#[test]
fn invalid_paths_references_and_candidate_types_cannot_enter_state() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("references.db")).unwrap();
    let blob = store.put(&Object::Blob { bytes: vec![1] }).unwrap();
    for path in ["../escape", "/absolute", "a//b", "a/./b", "a\\b", ""] {
        assert!(
            store
                .put(&Object::Snapshot {
                    entries: vec![SnapshotEntry {
                        path: path.into(),
                        blob
                    }]
                })
                .is_err()
        );
    }
    for paths in [["a", "a"], ["a", "a/b"]] {
        let entries = paths
            .into_iter()
            .map(|path| SnapshotEntry {
                path: path.into(),
                blob,
            })
            .collect();
        assert!(store.put(&Object::Snapshot { entries }).is_err());
    }
    let absent: ObjectId = format!("sha256:{}", "0".repeat(64)).parse().unwrap();
    assert!(matches!(
        store.put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "missing".into(),
                blob: absent
            }]
        }),
        Err(Error::NotFound(_))
    ));
    assert!(matches!(
        store.accept(&request("wrong-kind", None, blob)),
        Err(Error::WrongKind { .. })
    ));
    assert_eq!(store.head("local", "main").unwrap(), None);
    assert!(store.events("local", "main").unwrap().is_empty());
}

#[test]
fn evidence_preserves_declared_scope_without_becoming_trusted_verification() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("evidence.db")).unwrap();
    let candidate = snapshot(&mut store, b"candidate");
    let output = store
        .put(&Object::Blob {
            bytes: b"caller supplied output".to_vec(),
        })
        .unwrap();
    let record = Object::EvidenceRecord {
        candidate,
        outcome: EvidenceOutcome::Pass,
        provenance: "An unauthenticated caller claims this passed".into(),
        output: Some(output),
    };
    let id = store.put(&record).unwrap();
    assert_eq!(store.get(id).unwrap(), record);
    assert!(store.events("local", "main").unwrap().is_empty());
    assert_eq!(store.head("local", "main").unwrap(), None);
}

#[test]
fn unrelated_or_future_databases_are_not_silently_adopted() {
    let dir = tempdir().unwrap();
    let unrelated = dir.path().join("unrelated.db");
    let connection = rusqlite::Connection::open(&unrelated).unwrap();
    connection
        .execute("CREATE TABLE user_data(value TEXT)", [])
        .unwrap();
    drop(connection);
    assert!(matches!(
        Store::open(unrelated),
        Err(Error::UnsupportedDatabase(_))
    ));
    let future = dir.path().join("future.db");
    drop(Store::open(&future).unwrap());
    let connection = rusqlite::Connection::open(&future).unwrap();
    connection.pragma_update(None, "user_version", 2).unwrap();
    drop(connection);
    assert!(matches!(
        Store::open(future),
        Err(Error::UnsupportedDatabase(_))
    ));
}
