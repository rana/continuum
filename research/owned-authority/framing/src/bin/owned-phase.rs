//! Disposable measurement worker; no storage policy change or service interface.
use continuum_journal_framing::{
    Object, ObjectId,
    store::{Request, Store},
};
use serde::Deserialize;
use serde_json::{Value, json};
use std::{
    collections::BTreeMap, env, fs, hint::black_box, path::Path, process::Command, time::Instant,
};

#[derive(Deserialize)]
struct Spec {
    blob_id: ObjectId,
    blob: Object,
    head: Value,
    receipt: Value,
    first_request: Request,
    first_receipt: Value,
    latest_operation: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        return Err("usage: owned-phase DIRECTORY SPEC.json OWNED-STORE-CLI".into());
    }
    let path = Path::new(&args[1]);
    let spec: Spec = serde_json::from_slice(&fs::read(&args[2])?)?;
    let started = Instant::now();
    let mut store = Store::open(path)?;
    let open_ns = started.elapsed().as_nanos();
    let mut samples = Vec::new();
    let mut responses = BTreeMap::new();
    macro_rules! sample {
        ($name:literal, $expression:expr, $wanted:expr) => {{
            let started = Instant::now();
            let actual = black_box($expression);
            let elapsed_ns = started.elapsed().as_nanos();
            // Verification and JSON conversion are outside the measured interval.
            let response = serde_json::to_value(actual)?;
            assert_eq!(response, $wanted);
            responses.insert($name, response);
            samples.push(json!({"operation":$name,"elapsed_ns":elapsed_ns}));
        }};
    }
    let wanted_blob = serde_json::to_value(&spec.blob)?;
    for _ in 0..128 {
        let retry = spec.first_request.clone();
        let duplicate = spec.blob.clone();
        sample!("get", store.get(spec.blob_id)?, wanted_blob);
        sample!("head", store.head("probe", "source")?, spec.head);
        sample!(
            "receipt",
            store.receipt("probe", &spec.latest_operation)?,
            spec.receipt
        );
        sample!(
            "retry",
            store.accept(retry, "none")?,
            json!({"receipt":spec.first_receipt,"replayed":true})
        );
        sample!("duplicate_put", store.put(duplicate)?, json!(spec.blob_id));
    }
    let command = || {
        Command::new(&args[3])
            .args(["head", &args[1], "probe", "source"])
            .output()
    };
    let held = command()?;
    assert!(!held.status.success() && held.stdout.is_empty() && !held.stderr.is_empty());
    drop(store);
    let released = command()?;
    assert!(released.status.success());
    assert_eq!(
        serde_json::from_slice::<Value>(&released.stdout)?,
        spec.head
    );
    println!(
        "{}",
        json!({"open_ns":open_ns,"samples":samples,"responses":responses,
        "held_probe":{"returncode":held.status.code(),"stdout":String::from_utf8(held.stdout)?,"stderr":String::from_utf8(held.stderr)?},
        "released_probe":{"returncode":released.status.code(),"stdout":String::from_utf8(released.stdout)?,"stderr":String::from_utf8(released.stderr)?}})
    );
    Ok(())
}
