use continuum_core::context::{self, PrepareContextRequest};
use continuum_core::{AcceptRequest, EvidenceOutcome, Object, Outcome, SnapshotEntry, Store};
use serde::de::DeserializeOwned;
use serde_json::{Value, json};
use std::{error::Error, fs, io::Read};

type CliResult<T> = Result<T, Box<dyn Error>>;

const HELP: &str = "Continuum experimental native core
  continuum init DB
  continuum backup DB NEW_FILE
  continuum blob DB FILE
  continuum put DB OBJECT.json
  continuum get DB OBJECT_ID
  continuum head DB ACCEPTOR TARGET
  continuum accept DB REQUEST.json
  continuum receipt DB ACCEPTOR OPERATION_ID
  continuum events DB ACCEPTOR TARGET
  continuum prepare-context DB REQUEST.json
  continuum inspect-context DB CONTEXT_PACK_ID
  continuum verify-context DB CONTEXT_PACK_ID
  continuum verify-current-context DB CONTEXT_PACK_ID
  continuum acknowledge-handoff DB ACKNOWLEDGEMENT.json
  continuum verify-handoff DB ACKNOWLEDGEMENT_ID
  continuum demo DB

Output is JSON. Acceptance performs a local conditional state transition;
it does not authenticate the acceptor or validate declared evidence.
Context commands preserve exact source/rendered Blobs and conditional guidance.
Handoff acknowledgements validate context references only, not external effects.
";

fn read_context_bytes(path: &str) -> CliResult<Vec<u8>> {
    let mut bytes = Vec::new();
    fs::File::open(path)?
        .take(context::MAX_CONTEXT_INPUT_BYTES as u64 + 1)
        .read_to_end(&mut bytes)?;
    if bytes.len() > context::MAX_CONTEXT_INPUT_BYTES {
        return Err("context input exceeds 256 KiB".into());
    }
    Ok(bytes)
}

fn read_json<T: DeserializeOwned>(path: &str) -> CliResult<T> {
    let mut bytes = Vec::new();
    fs::File::open(path)?
        .take(continuum_core::MAX_OBJECT_BYTES as u64 + 1)
        .read_to_end(&mut bytes)?;
    if bytes.len() > continuum_core::MAX_OBJECT_BYTES {
        return Err("JSON input exceeds 16 MiB".into());
    }
    Ok(serde_json::from_slice(&bytes)?)
}

fn run(args: &[String]) -> CliResult<Value> {
    let [command, database, rest @ ..] = args else {
        return Err(HELP.into());
    };
    let required_args = match command.as_str() {
        "init" | "demo" => 0,
        "backup"
        | "blob"
        | "put"
        | "get"
        | "accept"
        | "prepare-context"
        | "inspect-context"
        | "verify-context"
        | "verify-current-context"
        | "acknowledge-handoff"
        | "verify-handoff" => 1,
        "head" | "receipt" | "events" => 2,
        _ => return Err(HELP.into()),
    };
    if rest.len() != required_args {
        return Err(HELP.into());
    }
    if !matches!(command.as_str(), "init" | "demo") && !std::path::Path::new(database).is_file() {
        return Err("database does not exist; run continuum init first".into());
    }
    let mut store = Store::open(database)?;
    match (command.as_str(), rest) {
        ("init", []) => Ok(json!({"database": database, "schema_version": 1})),
        ("backup", [path]) => Ok(json!(store.backup_export(path)?)),
        ("blob", [path]) => {
            let mut bytes = Vec::new();
            fs::File::open(path)?
                .take(continuum_core::MAX_OBJECT_BYTES as u64 + 1)
                .read_to_end(&mut bytes)?;
            let id = store.put(&Object::Blob { bytes })?;
            Ok(json!({"id": id, "type": "blob"}))
        }
        ("put", [path]) => {
            let object: Object = read_json(path)?;
            let id = store.put(&object)?;
            Ok(json!({"id": id, "type": object.kind()}))
        }
        ("get", [id]) => {
            let id = id.parse()?;
            Ok(
                json!({"id": id, "format_version": continuum_core::FORMAT_VERSION, "object": store.get(id)?}),
            )
        }
        ("head", [acceptor, target]) => Ok(json!(store.head(acceptor, target)?)),
        ("accept", [path]) => Ok(json!(store.accept(&read_json::<AcceptRequest>(path)?)?)),
        ("receipt", [acceptor, operation]) => Ok(json!(store.receipt(acceptor, operation)?)),
        ("events", [acceptor, target]) => Ok(json!(store.events(acceptor, target)?)),
        ("prepare-context", [path]) => {
            let request: PrepareContextRequest =
                context::decode_context_json(&read_context_bytes(path)?)?;
            Ok(json!(context::prepare_context(&mut store, &request)?))
        }
        ("inspect-context", [id]) => Ok(json!(context::inspect_context(&store, id.parse()?)?)),
        ("verify-context", [id]) => Ok(json!(context::verify_context(&store, id.parse()?)?)),
        ("verify-current-context", [id]) => {
            Ok(json!(context::verify_current_context(&store, id.parse()?)?))
        }
        ("acknowledge-handoff", [path]) => Ok(json!(context::acknowledge_handoff(
            &mut store,
            &read_context_bytes(path)?
        )?)),
        ("verify-handoff", [id]) => Ok(json!(context::verify_handoff(&store, id.parse()?)?)),
        ("demo", []) => demo(&mut store),
        _ => Err(HELP.into()),
    }
}

fn snapshot(store: &mut Store, bytes: &[u8]) -> CliResult<continuum_core::ObjectId> {
    let blob = store.put(&Object::Blob {
        bytes: bytes.to_vec(),
    })?;
    Ok(store.put(&Object::Snapshot {
        entries: vec![SnapshotEntry {
            path: "hello.txt".into(),
            blob,
        }],
    })?)
}

fn demo(store: &mut Store) -> CliResult<Value> {
    if store.head("demo", "main")?.is_some() {
        return Err("demo requires a database without an existing demo/main head".into());
    }
    let initial = snapshot(store, b"hello\n")?;
    let revised = snapshot(store, b"hello, agents\n")?;
    let alternative = snapshot(store, b"hello, workstations\n")?;
    let initial_request = AcceptRequest {
        acceptor: "demo".into(),
        target: "main".into(),
        operation_id: "initial".into(),
        expected: None,
        candidate: initial,
    };
    let first = store.accept(&initial_request)?;
    let next_request = AcceptRequest {
        operation_id: "agent-a".into(),
        expected: first.receipt.resulting,
        candidate: revised,
        ..initial_request.clone()
    };
    let next = store.accept(&next_request)?;
    let stale = store.accept(&AcceptRequest {
        operation_id: "agent-b".into(),
        candidate: alternative,
        ..next_request
    })?;
    let replayed_initial = store.accept(&initial_request)?;
    let evidence = store.put(&Object::EvidenceRecord {
        candidate: initial,
        outcome: EvidenceOutcome::Unknown,
        provenance: "Demonstration declaration only; no verifier executed".into(),
        output: None,
    })?;
    assert_eq!(stale.receipt.outcome, Outcome::PreconditionFailed);
    assert_eq!(replayed_initial.receipt, first.receipt);
    Ok(json!({
        "demonstration": "immutable objects, stale-head rejection, durable retry after head movement",
        "initial": first,
        "advanced": next,
        "stale_proposal": stale,
        "replayed_original": replayed_initial,
        "current_head": store.head("demo", "main")?,
        "untrusted_evidence": evidence,
        "events": store.events("demo", "main")?.len()
    }))
}

fn main() {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.is_empty() || args == ["--help"] || args == ["-h"] {
        print!("{HELP}");
        return;
    }
    match run(&args) {
        Ok(value) => println!(
            "{}",
            serde_json::to_string_pretty(&value).expect("JSON value serializes")
        ),
        Err(error) => {
            eprintln!("{}", json!({"error": error.to_string()}));
            std::process::exit(1);
        }
    }
}
