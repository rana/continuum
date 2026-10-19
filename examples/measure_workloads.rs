//! A bounded, single-process workload baseline, not a comparative benchmark.
//! See docs/experiments/release-baseline.md for timing and storage boundaries.

use continuum_core::context::{self, AcceptanceAnchor, FreshnessStatus, PrepareContextRequest};
use continuum_core::{AcceptRequest, Head, Object, Outcome, Result, SnapshotEntry, Store};
use serde::Serialize;
use serde_json::json;
use sha2::{Digest, Sha256};
use std::{env, error::Error, io, path::PathBuf, time::Instant};

const PAYLOAD_BYTES: usize = 1024;
const CONTEXT_BUDGET: u32 = 8192;

#[derive(Serialize)]
struct Measurement {
    operation: &'static str,
    sample_count: usize,
    minimum_ns: u64,
    p50_ns: u64,
    p95_ns: u64,
    maximum_ns: u64,
    total_timed_ns: u64,
    operations_per_timed_second: Option<f64>,
    samples_ns: Vec<u64>,
}

fn measurement(operation: &'static str, samples_ns: Vec<u64>) -> Measurement {
    let mut sorted = samples_ns.clone();
    sorted.sort_unstable();
    let percentile = |p: usize| sorted[(sorted.len() * p).div_ceil(100) - 1];
    let total_timed_ns: u64 = samples_ns.iter().sum();
    Measurement {
        operation,
        sample_count: sorted.len(),
        minimum_ns: sorted[0],
        p50_ns: percentile(50),
        p95_ns: percentile(95),
        maximum_ns: sorted[sorted.len() - 1],
        total_timed_ns,
        operations_per_timed_second: (total_timed_ns != 0)
            .then(|| sorted.len() as f64 * 1_000_000_000.0 / total_timed_ns as f64),
        samples_ns,
    }
}

fn timed<T>(samples: &mut Vec<u64>, operation: impl FnOnce() -> Result<T>) -> Result<T> {
    let start = Instant::now();
    let value = operation()?;
    samples.push(
        start
            .elapsed()
            .as_nanos()
            .try_into()
            .expect("elapsed u64 ns"),
    );
    Ok(value)
}

fn fingerprint<T: Serialize>(digest: &mut Sha256, value: &T) -> serde_json::Result<()> {
    let bytes = serde_json::to_vec(value)?;
    digest.update((bytes.len() as u64).to_be_bytes());
    digest.update(bytes);
    Ok(())
}

fn arguments() -> std::result::Result<(usize, PathBuf), Box<dyn Error>> {
    let mut samples = 100;
    let mut directory = env::temp_dir();
    let mut args = env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--samples" => samples = args.next().ok_or("--samples needs an integer")?.parse()?,
            "--directory" => {
                directory = args
                    .next()
                    .ok_or("--directory needs an existing path")?
                    .into();
            }
            "--help" | "-h" => {
                println!(
                    "measure_workloads [--samples N] [--directory EXISTING_LOCAL_DIRECTORY]\n\
                     N defaults to 100 and must be in 1..=10000.\n\
                     Creates and removes a fresh temporary database under the directory.\n\
                     Emits JSON only after all correctness checks and cleanup succeed."
                );
                std::process::exit(0);
            }
            _ => return Err(format!("unknown argument: {arg}").into()),
        }
    }
    if !(1..=10000).contains(&samples) {
        return Err("--samples must be in 1..=10000".into());
    }
    Ok((samples, directory.canonicalize()?))
}

fn main() -> std::result::Result<(), Box<dyn Error>> {
    let (count, directory) = arguments()?;
    let workload_start = Instant::now();
    let temporary = tempfile::Builder::new()
        .prefix("continuum-baseline-")
        .tempdir_in(&directory)?;
    let mut store = Store::open(temporary.path().join("work.db"))?;
    let mut measurements = Vec::new();
    let mut semantics = Sha256::new();
    semantics.update(b"continuum.measure_workloads.semantic.v1\0");
    let mut dataset = Sha256::new();
    dataset.update(b"continuum.measure_workloads.fixtures.v1\0");
    let mut fixtures = Vec::with_capacity(count);
    let mut blob_ids = Vec::with_capacity(count);
    for index in 0..count {
        let mut bytes = vec![0; PAYLOAD_BYTES];
        bytes[..8].copy_from_slice(&(index as u64).to_le_bytes());
        let mut state = (index as u64 + 1).wrapping_mul(0x9e3779b97f4a7c15);
        for byte in &mut bytes[8..] {
            state ^= state << 13;
            state ^= state >> 7;
            state ^= state << 17;
            *byte = state as u8;
        }
        let object = Object::Blob { bytes };
        let canonical = object.canonical_bytes()?;
        dataset.update((canonical.len() as u64).to_be_bytes());
        dataset.update(canonical);
        blob_ids.push(object.id()?);
        fixtures.push(object);
    }

    let mut samples = Vec::with_capacity(count);
    for (object, expected) in fixtures.iter().zip(&blob_ids) {
        let id = timed(&mut samples, || store.put(object))?;
        assert_eq!(id, *expected);
        fingerprint(&mut semantics, &id)?;
    }
    measurements.push(measurement("put_unique_1024_byte_blob", samples));

    let mut samples = Vec::with_capacity(count);
    for (expected, id) in fixtures.iter().zip(&blob_ids) {
        let object = timed(&mut samples, || store.get(*id))?;
        assert_eq!(object, *expected);
    }
    measurements.push(measurement("get_existing_1024_byte_blob", samples));

    // Snapshot construction and insertion are setup, outside acceptance timing.
    let mut snapshots = Vec::with_capacity(count);
    for id in &blob_ids {
        snapshots.push(store.put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "src/payload.bin".into(),
                blob: *id,
            }],
        })?);
    }
    let mut accepted = Vec::with_capacity(count);
    let mut head = None;
    let mut samples = Vec::with_capacity(count);
    for (index, candidate) in snapshots.iter().enumerate() {
        let request = AcceptRequest {
            acceptor: "baseline".into(),
            target: "main".into(),
            operation_id: format!("accept:{index:05}"),
            expected: head,
            candidate: *candidate,
        };
        let result = timed(&mut samples, || store.accept(&request))?;
        assert!(!result.replayed);
        assert_eq!(result.receipt.outcome, Outcome::Accepted);
        assert_eq!(result.receipt.request, request);
        assert_eq!(result.receipt.observed, head);
        head = Some(Head {
            root: *candidate,
            generation: index as u64 + 1,
        });
        assert_eq!(result.receipt.resulting, head);
        assert_eq!(store.head("baseline", "main")?, head);
        fingerprint(&mut semantics, &result.receipt)?;
        accepted.push(result.receipt);
    }
    measurements.push(measurement("accept_new_expected_head", samples));

    let mut samples = Vec::with_capacity(count);
    for (index, original) in accepted.iter().enumerate() {
        // Every original precondition precedes the final head, including None.
        let request = AcceptRequest {
            operation_id: format!("reject:{index:05}"),
            ..original.request.clone()
        };
        let result = timed(&mut samples, || store.accept(&request))?;
        assert!(!result.replayed);
        assert_eq!(result.receipt.outcome, Outcome::PreconditionFailed);
        assert_eq!(result.receipt.request, request);
        assert_eq!(result.receipt.observed, head);
        assert_eq!(result.receipt.resulting, head);
        assert_eq!(store.head("baseline", "main")?, head);
        fingerprint(&mut semantics, &result.receipt)?;
    }
    measurements.push(measurement("reject_stale_expected_head", samples));

    let mut samples = Vec::with_capacity(count);
    for original in &accepted {
        let result = timed(&mut samples, || store.accept(&original.request))?;
        assert!(result.replayed);
        assert_eq!(result.receipt, *original);
    }
    assert_eq!(store.head("baseline", "main")?, head);
    let events = store.events("baseline", "main")?;
    assert_eq!(events.len(), 2 * count);
    assert_eq!(&events[..count], accepted.as_slice());
    measurements.push(measurement("retry_exact_accepted_request", samples));

    // Each context has a distinct exact work state and its own accepted anchor.
    // All source objects, requests and anchors are installed before timing it.
    let mut requests = Vec::with_capacity(count);
    for (index, (source, request_blob)) in snapshots.iter().zip(&blob_ids).enumerate() {
        let bytes = serde_json::to_vec(&json!({
            "schema": context::WORK_STATE_SCHEMA,
            "id": format!("work:{index:05}"), "source_snapshot": source,
            "objective": {"id": "objective:baseline",
                "statement": "Measure a bounded native continuation workload.",
                "done_when": "Measured operations satisfy their checked outcomes.",
                "constraints": ["No model or external dispatch occurs."]},
            "attempts": [{"id": "attempt:one", "operation_id": format!("operation:{index:05}"),
                "source_snapshot": source, "summary": "An authored uncertain operation.",
                "dispatch_state": "may_have_been_sent", "request": request_blob,
                "receipt": null, "outcome_note": "The dispatch state is a fixture, not external evidence."}],
            "decisions": [{"id": "decision:one", "state": "active",
                "statement": "Reconcile the existing operation before any retry.",
                "basis_attempt_ids": ["attempt:one"], "reopen_when": "A bound receipt arrives."}],
            "uncertainties": [{"id": "uncertainty:one", "question": "Was the operation dispatched?",
                "why_it_matters": "An unchecked repeat could duplicate its effect."}],
            "handoff": {"id": "handoff:one", "from_worker": "worker:producer",
                "to_worker": "worker:consumer", "scope": "Inspect the exact recovery context.",
                "required_decision_ids": ["decision:one"]}
        }))?;
        assert_eq!(context::parse_work_state(&bytes)?.source_snapshot, *source);
        let work_state = store.put(&Object::Blob { bytes })?;
        let root = store.put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "work/state.json".into(),
                blob: work_state,
            }],
        })?;
        let target = format!("context:{index:05}");
        let accepted_anchor = store.accept(&AcceptRequest {
            acceptor: "baseline".into(),
            target: target.clone(),
            operation_id: format!("anchor:{index:05}"),
            expected: None,
            candidate: root,
        })?;
        assert!(!accepted_anchor.replayed);
        assert_eq!(accepted_anchor.receipt.outcome, Outcome::Accepted);
        let expected = Head {
            root,
            generation: 1,
        };
        assert_eq!(accepted_anchor.receipt.resulting, Some(expected));
        requests.push(PrepareContextRequest {
            schema: context::PREPARE_CONTEXT_SCHEMA.into(),
            work_state,
            max_bytes: CONTEXT_BUDGET,
            anchor: Some(AcceptanceAnchor {
                acceptor: "baseline".into(),
                target,
                expected,
                work_state_path: "work/state.json".into(),
            }),
        });
    }

    let mut packs = Vec::with_capacity(count);
    let mut samples = Vec::with_capacity(count);
    for request in &requests {
        let pack = timed(&mut samples, || {
            context::prepare_context(&mut store, request)
        })?;
        assert_eq!(pack.manifest.work_state, request.work_state);
        assert!(pack.manifest.omitted.is_empty());
        assert_eq!(pack.manifest.included.len(), 6);
        assert!(pack.manifest.rendered_bytes <= CONTEXT_BUDGET);
        assert_eq!(pack.freshness.status, FreshnessStatus::MatchesAtObservation);
        fingerprint(&mut semantics, &pack.manifest)?;
        packs.push(pack);
    }
    measurements.push(measurement("prepare_unique_anchored_context", samples));

    let mut samples = Vec::with_capacity(count);
    for (request, original) in requests.iter().zip(&packs) {
        let repeated = timed(&mut samples, || {
            context::prepare_context(&mut store, request)
        })?;
        assert_eq!(repeated.context_pack, original.context_pack);
        assert_eq!(repeated.manifest, original.manifest);
        assert_eq!(repeated.freshness, original.freshness);
    }
    measurements.push(measurement("prepare_existing_anchored_context", samples));

    for (name, current) in [
        ("verify_historical_context", false),
        ("verify_current_context", true),
    ] {
        let mut samples = Vec::with_capacity(count);
        for pack in &packs {
            let verified = timed(&mut samples, || {
                if current {
                    context::verify_current_context(&store, pack.context_pack)
                } else {
                    context::verify_context(&store, pack.context_pack)
                }
            })?;
            assert!(verified.exact_projection_verified);
            assert!(!verified.action_authority_verified);
            assert_eq!(verified.context_pack, pack.context_pack);
            assert_eq!(verified.rendered_bytes, pack.manifest.rendered_bytes);
            assert_eq!(verified.freshness, pack.freshness);
        }
        measurements.push(measurement(name, samples));
    }

    let workload_wall_ns = workload_start.elapsed().as_nanos();
    drop(store);
    temporary.close()?;
    let report = json!({
        "schema": "continuum.workload_baseline.v1",
        "fixture_version": "continuum.measure_workloads.fixtures.v1",
        "crate_version": env!("CARGO_PKG_VERSION"),
        "build": {"debug_assertions": cfg!(debug_assertions),
            "target_os": env::consts::OS, "target_arch": env::consts::ARCH,
            "profile_and_toolchain": "Record the actual build command and rustc -Vv alongside this output."},
        "dataset": {"samples_per_operation": count, "blob_payload_bytes": PAYLOAD_BYTES,
            "blob_fixture_sha256": format!("{:x}", dataset.finalize()),
            "snapshot_entries": 1, "context_included_records": 6, "context_max_bytes": CONTEXT_BUDGET,
            "context_rendered_bytes": packs.iter().map(|p| p.manifest.rendered_bytes).collect::<Vec<_>>()},
        "execution": {"processes": 1, "store_connections": 1,
            "database_parent_directory": directory, "temporary_database_removed": true,
            "store_configuration": {"journal_mode": "wal", "synchronous": "full", "busy_timeout_ms": 5000},
            "configuration_basis": "Store::open configuration; not proof of physical storage durability.",
            "workload_wall_ns_before_report_and_cleanup": workload_wall_ns},
        "timing": {"clock": "std::time::Instant", "unit": "nanoseconds",
            "percentiles": "nearest rank, ceil(p*n)-1; descriptive samples, no confidence interval",
            "warmup": "none removed; operations run in the listed order on one growing database",
            "includes": "one in-process public API call, result construction, timer overhead",
            "excludes": "compilation, process startup, fixture generation, setup between groups, assertions, JSON output, connection close and cleanup",
            "throughput_scope": "operation count / sum of timed calls; excludes gaps and is not sustained end-to-end throughput",
            "cache_scope": "no cache flush; read and verification inputs were previously inserted in this process"},
        "correctness": {"all_checks_passed": true,
            "semantic_fingerprint_sha256": format!("{:x}", semantics.finalize()),
            "main_target_event_count": events.len(), "main_target_final_head": head,
            "checked": ["exact blob IDs and recovered bytes", "successful conditional head transitions",
                "durable stale-precondition results without head movement", "exact historical retries without new events",
                "complete six-record context selections", "identical repeated context preparation",
                "historical and current projection verification without action authority"]},
        "measurements": measurements,
        "limits": ["single worker, small fixed-shape objects and contexts",
            "not a cold-cache, contention, recovery, network or model benchmark",
            "file-backed does not imply physical disk: record filesystem and host outside this process",
            "no Git, Scion, language or other hardware comparison is established"]
    });
    serde_json::to_writer_pretty(io::stdout().lock(), &report)?;
    println!();
    Ok(())
}
