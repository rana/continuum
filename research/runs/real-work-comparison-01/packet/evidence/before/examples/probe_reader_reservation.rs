//! Controlled SQLite reader/open experiment; not a throughput benchmark.
use continuum_core::{AcceptRequest, Object, SnapshotEntry, Store};
use rusqlite::{Connection, OpenFlags};
use serde_json::{Value, json};
use std::{error::Error, fs, path::PathBuf, process::Command, time::Instant};

fn invoke(
    binary: &PathBuf,
    db: &PathBuf,
    command: &str,
    arguments: &[String],
) -> Result<Value, Box<dyn Error>> {
    let start = Instant::now();
    let output = Command::new(binary)
        .arg(command)
        .arg(db)
        .args(arguments)
        .output()?;
    let argv = [
        vec![
            binary.display().to_string(),
            command.to_owned(),
            db.display().to_string(),
        ],
        arguments.to_vec(),
    ]
    .concat();
    Ok(json!({"argv": argv,
        "returncode": output.status.code(), "stdout": String::from_utf8(output.stdout)?,
        "stderr": String::from_utf8(output.stderr)?, "elapsed_seconds": start.elapsed().as_secs_f64()}))
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let [binary_flag, binary, directory_flag, directory] = args.as_slice() else {
        return Err(
            "usage: probe_reader_reservation --binary PATH --directory NEW_DIRECTORY".into(),
        );
    };
    if binary_flag != "--binary" || directory_flag != "--directory" {
        return Err("unexpected flags".into());
    }
    let binary = fs::canonicalize(binary)?;
    let directory = PathBuf::from(directory);
    fs::create_dir(&directory)?;
    let db = directory.canonicalize()?.join("probe.db");
    let mut store = Store::open(&db)?;
    let blob = store.put(&Object::Blob {
        bytes: b"reader-reservation-probe\n".to_vec(),
    })?;
    let root = store.put(&Object::Snapshot {
        entries: vec![SnapshotEntry {
            path: "probe.txt".into(),
            blob,
        }],
    })?;
    let request = AcceptRequest {
        acceptor: "probe".into(),
        target: "main".into(),
        operation_id: "initial".into(),
        expected: None,
        candidate: root,
    };
    let receipt = store.accept(&request)?.receipt;
    let commands = [
        ("get", vec![blob.to_string()]),
        ("head", vec!["probe".into(), "main".into()]),
        ("receipt", vec!["probe".into(), "initial".into()]),
    ];
    let baseline: Vec<_> = commands
        .iter()
        .map(|(name, args)| invoke(&binary, &db, name, args))
        .collect::<Result<_, _>>()?;
    assert!(baseline.iter().all(|r| r["returncode"] == 0));
    let writer = Connection::open(&db)?;
    assert_eq!(
        writer.query_row("PRAGMA journal_mode", [], |r| r.get::<_, String>(0))?,
        "wal"
    );
    writer.execute_batch("BEGIN IMMEDIATE")?;
    let transaction_open_before = !writer.is_autocommit();
    // Same rusqlite/bundled SQLite as this probe's native Store. No writer open gate.
    let control = Connection::open_with_flags(&db, OpenFlags::SQLITE_OPEN_READ_ONLY)?;
    let start = Instant::now();
    let observed: (String, i64) = control.query_row(
        "SELECT root,generation FROM heads WHERE acceptor='probe' AND target='main'",
        [],
        |r| Ok((r.get(0)?, r.get(1)?)),
    )?;
    let stored_receipt: String = control.query_row(
        "SELECT receipt FROM events WHERE acceptor='probe' AND operation_id='initial'",
        [],
        |r| r.get(0),
    )?;
    let object_bytes: i64 = control.query_row(
        "SELECT length(canonical) FROM objects WHERE id=?1",
        [blob.to_string()],
        |r| r.get(0),
    )?;
    let control_seconds = start.elapsed().as_secs_f64();
    assert_eq!(observed.0, root.to_string());
    assert_eq!(observed.1, 1);
    assert_eq!(
        serde_json::from_str::<Value>(&stored_receipt)?,
        json!(receipt)
    );
    assert!(object_bytes > 0);
    let held: Vec<_> = commands
        .iter()
        .map(|(name, args)| invoke(&binary, &db, name, args))
        .collect::<Result<_, _>>()?;
    for result in &held {
        assert_eq!(result["returncode"], 1);
        assert_eq!(result["stdout"], "");
        let error: Value = serde_json::from_str(result["stderr"].as_str().unwrap())?;
        assert_eq!(error["error"], "database error: database is locked");
    }
    let transaction_open_after = !writer.is_autocommit();
    writer.execute_batch("ROLLBACK")?;
    let released: Vec<_> = commands
        .iter()
        .map(|(name, args)| invoke(&binary, &db, name, args))
        .collect::<Result<_, _>>()?;
    for (before, after) in baseline.iter().zip(&released) {
        assert_eq!(after["returncode"], 0);
        assert_eq!(before["stdout"], after["stdout"]);
    }
    assert_eq!(store.events("probe", "main")?, vec![receipt.clone()]);
    assert_eq!(store.head("probe", "main")?, receipt.resulting);
    let result = json!({"schema":"continuum.reader_reservation_probe.v1", "sqlite_version":rusqlite::version(),
        "reservation":"BEGIN IMMEDIATE; no data changes", "writer_transaction_open_before":transaction_open_before,
        "writer_transaction_open_after":transaction_open_after, "baseline":baseline, "held":held, "released":released,
        "read_only_control":{"root":observed.0,"generation":observed.1,"receipt":serde_json::from_str::<Value>(&stored_receipt)?,
            "canonical_object_bytes":object_bytes,"elapsed_seconds":control_seconds,"flags":"SQLITE_OPEN_READ_ONLY"},
        "logical_history_unchanged":true,
        "scope":"Three sequential native CLI commands, one held writer reservation, same-build SQLite read-only control. No throughput/capacity or read-only Store implementation claim."});
    fs::write(
        directory.join("result.json"),
        serde_json::to_vec_pretty(&result)?,
    )?;
    println!("{}", serde_json::to_string_pretty(&result)?);
    Ok(())
}
