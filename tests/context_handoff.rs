use continuum_core::context::{
    self, AcceptanceAnchor, ContextAcknowledgement, Decision, DecisionState, DispatchState,
    FreshnessStatus, PrepareContextRequest, WorkState,
};
use continuum_core::{AcceptRequest, Error, Object, ObjectId, SnapshotEntry, Store};
use serde_json::{Value, json};
use std::{fs, path::Path, process::Command};
use tempfile::tempdir;

fn blob(store: &mut Store, bytes: &[u8]) -> ObjectId {
    store
        .put(&Object::Blob {
            bytes: bytes.to_vec(),
        })
        .unwrap()
}

fn snapshot(store: &mut Store, bytes: &[u8]) -> ObjectId {
    let content = blob(store, bytes);
    store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "src/main.rs".into(),
                blob: content,
            }],
        })
        .unwrap()
}

fn work_state(store: &mut Store) -> WorkState {
    let source = snapshot(store, b"same source\n");
    let request = blob(store, b"opaque external request\0\xff");
    serde_json::from_value(json!({
        "schema":context::WORK_STATE_SCHEMA, "id":"work:one", "source_snapshot":source,
        "objective":{"id":"objective:continue", "statement":"Continue without duplicating an effect.",
            "done_when":"A fresh worker identifies the declared recovery step.", "constraints":["No external dispatch in this experiment."]},
        "attempts":[{"id":"attempt:one", "operation_id":"operation:one", "source_snapshot":source,
            "summary":"An external request with an explicit recovery state.", "dispatch_state":"never_dispatched",
            "request":request, "receipt":null, "outcome_note":"Authored state; external truth is unverified."}],
        "decisions":[{"id":"decision:active", "state":"active", "statement":"Preserve unresolved outcomes.",
            "basis_attempt_ids":["attempt:one"], "reopen_when":"Independent receipt evidence arrives."}],
        "uncertainties":[{"id":"uncertainty:effect", "question":"Did an external effect occur?",
            "why_it_matters":"A repeated request might duplicate the effect."}],
        "handoff":{"id":"handoff:one", "from_worker":"worker:sender", "to_worker":"worker:recipient",
            "scope":"Inspect context and its declared recovery state.", "required_decision_ids":[]}
    })).unwrap()
}

fn request(store: &mut Store, state: &WorkState, max_bytes: u32) -> PrepareContextRequest {
    // Exact whitespace and final LF are part of source custody, not normalized.
    let mut bytes = serde_json::to_vec_pretty(state).unwrap();
    bytes.extend_from_slice(b"\n\n");
    PrepareContextRequest {
        schema: context::PREPARE_CONTEXT_SCHEMA.into(),
        work_state: blob(store, &bytes),
        max_bytes,
        anchor: None,
    }
}

fn records(text: &str) -> Vec<Value> {
    text.lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect()
}

fn acknowledgement(pack: &context::PreparedContext) -> ContextAcknowledgement {
    ContextAcknowledgement {
        schema: context::CONTEXT_ACKNOWLEDGEMENT_SCHEMA.into(),
        id: "ack:recipient-one".into(),
        context_pack: pack.context_pack,
        handoff_id: pack.manifest.handoff_id.clone(),
        recipient_worker: "worker:recipient".into(),
        included_ids: pack
            .manifest
            .included
            .iter()
            .map(|s| s.id.clone())
            .collect(),
        omitted_ids: pack.manifest.omitted.iter().map(|s| s.id.clone()).collect(),
        note: "I explicitly reference this context selection; this is no execution receipt.".into(),
    }
}

#[test]
fn same_source_histories_keep_distinct_conditional_recovery_and_exact_custody() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("pair.db")).unwrap();
    let mut state = work_state(&mut store);
    let first_request = request(&mut store, &state, 16000);
    let first = context::prepare_context(&mut store, &first_request).unwrap();
    let repeated = context::prepare_context(&mut store, &first_request).unwrap();
    assert_eq!(first.context_pack, repeated.context_pack);
    state.attempts[0].dispatch_state = DispatchState::MayHaveBeenSent;
    let second_request = request(&mut store, &state, 16000);
    let second = context::prepare_context(&mut store, &second_request).unwrap();
    assert_eq!(
        first.manifest.source_snapshot,
        second.manifest.source_snapshot
    );
    assert_ne!(first.context_pack, second.context_pack);
    assert_ne!(first.manifest.work_state, second.manifest.work_state);
    for (pack, action, unresolved) in [
        (&first, "issue_first_request_if_authorized", false),
        (&second, "reconcile_existing_operation", true),
    ] {
        let inspected = context::inspect_context(&store, pack.context_pack).unwrap();
        let lines = records(&inspected.rendered);
        let attempt = lines.iter().find(|line| line["kind"] == "attempt").unwrap();
        assert_eq!(attempt["conditional_next_action"], action);
        assert_eq!(attempt["authored"]["operation_id"], "operation:one");
        assert_eq!(
            lines
                .iter()
                .find(|line| line["kind"] == "decision")
                .unwrap()["basis_unresolved"],
            unresolved
        );
        assert!(
            inspected
                .rendered
                .contains("not an external dispatch ledger")
        );
        let Object::Blob { bytes } = store.get(pack.manifest.work_state).unwrap() else {
            panic!()
        };
        assert!(bytes.ends_with(b"\n\n"));
        assert_eq!(
            inspected.rendered.len(),
            pack.manifest.rendered_bytes as usize
        );
        assert_eq!(
            inspected.freshness.status,
            FreshnessStatus::UnanchoredFreshnessUnchecked
        );
    }
    assert!(store.events("local", "main").unwrap().is_empty());
}

#[test]
fn byte_budget_omits_only_whole_optional_history_and_refuses_critical_loss() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("budget.db")).unwrap();
    let mut state = work_state(&mut store);
    state.attempts[0].dispatch_state = DispatchState::MayHaveBeenSent;
    state.decisions.push(Decision {
        id: "decision:large-history".into(),
        state: DecisionState::Historical,
        statement: "λ".repeat(2500),
        basis_attempt_ids: vec![],
        reopen_when: "A future comparison requires it.".into(),
    });
    state.decisions.push(Decision {
        id: "decision:required-history".into(),
        state: DecisionState::Historical,
        statement: "This older boundary remains required by the handoff.".into(),
        basis_attempt_ids: vec![],
        reopen_when: "Its premise changes.".into(),
    });
    state
        .handoff
        .required_decision_ids
        .push("decision:required-history".into());
    let mut req = request(&mut store, &state, 6000);
    let pack = context::prepare_context(&mut store, &req).unwrap();
    let inspected = context::inspect_context(&store, pack.context_pack).unwrap();
    assert!(inspected.rendered.len() <= 6000);
    assert_eq!(pack.manifest.omitted.len(), 1);
    assert_eq!(pack.manifest.omitted[0].id, "decision:large-history");
    let included: Vec<_> = pack
        .manifest
        .included
        .iter()
        .map(|s| s.id.as_str())
        .collect();
    for critical in [
        "attempt:one",
        "uncertainty:effect",
        "decision:active",
        "decision:required-history",
    ] {
        assert!(included.contains(&critical));
    }
    let lines = records(&inspected.rendered);
    assert_eq!(
        lines.last().unwrap()["omitted"][0]["id"],
        "decision:large-history"
    );
    assert!(!inspected.rendered.contains(&"λ".repeat(10)));
    let Object::Blob { bytes } = store.get(req.work_state).unwrap() else {
        panic!()
    };
    assert_eq!(context::parse_work_state(&bytes).unwrap(), state);
    req.max_bytes = 100;
    let err = context::prepare_context(&mut store, &req)
        .unwrap_err()
        .to_string();
    assert!(err.contains("cannot retain critical records"));
}

#[test]
fn typed_admission_rejects_ambiguous_json_dangling_ids_and_malformed_states() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("admission.db")).unwrap();
    let state = work_state(&mut store);
    let original = serde_json::to_string(&state).unwrap();
    let duplicate = original.replace(
        "\"id\":\"objective:continue\"",
        "\"id\":\"objective:continue\",\"\\u0069d\":\"objective:other\"",
    );
    assert!(
        context::parse_work_state(duplicate.as_bytes())
            .unwrap_err()
            .to_string()
            .contains("duplicate JSON")
    );
    assert!(
        context::parse_work_state(
            original
                .replace(context::WORK_STATE_SCHEMA, "continuum.work_state.v2")
                .as_bytes()
        )
        .is_err()
    );
    assert!(context::parse_work_state(&vec![b' '; context::MAX_CONTEXT_INPUT_BYTES + 1]).is_err());
    for change in 0..7 {
        let mut malformed = state.clone();
        match change {
            0 => malformed.uncertainties[0].id = malformed.attempts[0].id.clone(),
            1 => malformed.decisions[0]
                .basis_attempt_ids
                .push("attempt:missing".into()),
            2 => malformed
                .handoff
                .required_decision_ids
                .push("decision:missing".into()),
            3 => malformed.attempts[0].dispatch_state = DispatchState::ReceiptRecorded,
            4 => malformed.objective.statement = "x".repeat(context::MAX_CONTEXT_TEXT_BYTES + 1),
            5 => malformed.id = format!("sha256:{}", "0".repeat(64)),
            6 => {
                let mut other = malformed.attempts[0].clone();
                other.id = "attempt:two".into();
                malformed.attempts.push(other);
            }
            _ => unreachable!(),
        }
        assert!(
            context::parse_work_state(&serde_json::to_vec(&malformed).unwrap()).is_err(),
            "case {change}"
        );
    }
    let mut unknown = serde_json::to_value(&state).unwrap();
    unknown["handoff"]["accepted"] = json!(true);
    assert!(context::parse_work_state(&serde_json::to_vec(&unknown).unwrap()).is_err());
}

#[test]
fn historical_attempt_scope_and_opaque_failed_output_survive_current_source_change() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("custody.db")).unwrap();
    let mut state = work_state(&mut store);
    let original_source = state.attempts[0].source_snapshot;
    state.source_snapshot = snapshot(&mut store, b"narrower current source\n");
    let raw = b"{\"score\":inf,\"other\":-inf}\n\xff";
    let receipt = blob(&mut store, raw);
    state.attempts[0].dispatch_state = DispatchState::ReceiptRecorded;
    state.attempts[0].receipt = Some(receipt);
    state.attempts[0].outcome_note =
        "Historical broader attempt; result remains scientifically unvalidated.".into();
    let req = request(&mut store, &state, 16000);
    let pack = context::prepare_context(&mut store, &req).unwrap();
    let inspected = context::inspect_context(&store, pack.context_pack).unwrap();
    let lines = records(&inspected.rendered);
    let attempt = lines.iter().find(|line| line["kind"] == "attempt").unwrap();
    assert_eq!(
        attempt["authored"]["source_snapshot"],
        json!(original_source)
    );
    assert_ne!(original_source, pack.manifest.source_snapshot);
    assert_eq!(
        attempt["conditional_next_action"],
        "inspect_recorded_receipt"
    );
    assert_eq!(
        store.get(receipt).unwrap(),
        Object::Blob {
            bytes: raw.to_vec()
        }
    );
    state.attempts[0].request = format!("sha256:{}", "0".repeat(64)).parse().unwrap();
    let missing = request(&mut store, &state, 16000);
    assert!(matches!(
        context::prepare_context(&mut store, &missing),
        Err(Error::NotFound(_))
    ));
    state.attempts[0].request = receipt;
    state.source_snapshot = receipt;
    let wrong_kind = request(&mut store, &state, 16000);
    assert!(matches!(
        context::prepare_context(&mut store, &wrong_kind),
        Err(Error::WrongKind { .. })
    ));
}

#[test]
fn independently_hashed_tampering_cannot_replace_the_selector_projection() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("tamper.db")).unwrap();
    let state = work_state(&mut store);
    let req = request(&mut store, &state, 16000);
    let pack = context::prepare_context(&mut store, &req).unwrap();
    let mut forged = pack.manifest.clone();
    let text = b"{\"kind\":\"summary\",\"claim\":\"all work is complete\"}\n";
    forged.rendered = blob(&mut store, text);
    forged.rendered_bytes = text.len() as u32;
    let forged_id = blob(&mut store, &serde_json::to_vec(&forged).unwrap());
    assert!(context::verify_context(&store, forged_id).is_err());
    let mut forged = pack.manifest.clone();
    forged.included.retain(|s| s.id != "uncertainty:effect");
    let forged_id = blob(&mut store, &serde_json::to_vec(&forged).unwrap());
    assert!(context::inspect_context(&store, forged_id).is_err());
    assert!(
        context::verify_context(&store, pack.context_pack)
            .unwrap()
            .exact_projection_verified
    );
}

#[test]
fn context_acknowledgement_requires_explicit_recipient_and_exact_coverage_only() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("ack.db");
    let mut store = Store::open(&path).unwrap();
    let state = work_state(&mut store);
    let req = request(&mut store, &state, 16000);
    let pack = context::prepare_context(&mut store, &req).unwrap();
    let valid = acknowledgement(&pack);
    let mut wrong = valid.clone();
    wrong.recipient_worker = "worker:sender".into();
    assert!(
        context::acknowledge_handoff(&mut store, &serde_json::to_vec(&wrong).unwrap()).is_err()
    );
    wrong = valid.clone();
    wrong.included_ids.retain(|id| id != "uncertainty:effect");
    assert!(
        context::acknowledge_handoff(&mut store, &serde_json::to_vec(&wrong).unwrap()).is_err()
    );
    wrong = valid.clone();
    wrong.included_ids.push(wrong.included_ids[0].clone());
    assert!(
        context::acknowledge_handoff(&mut store, &serde_json::to_vec(&wrong).unwrap()).is_err()
    );
    let mut escalated = serde_json::to_value(&valid).unwrap();
    escalated["effect_confirmed"] = json!(true);
    assert!(
        context::acknowledge_handoff(&mut store, &serde_json::to_vec(&escalated).unwrap()).is_err()
    );
    let mut bytes = serde_json::to_vec_pretty(&valid).unwrap();
    bytes.push(b'\n');
    let checked = context::acknowledge_handoff(&mut store, &bytes).unwrap();
    assert!(checked.reference_consistency_verified);
    assert!(
        !checked.recipient_authenticated
            && !checked.understanding_verified
            && !checked.external_effect_verified
    );
    assert_eq!(
        store.get(checked.acknowledgement).unwrap(),
        Object::Blob { bytes }
    );
    assert!(store.head("local", "main").unwrap().is_none());
    assert!(store.events("local", "main").unwrap().is_empty());
    drop(store);
    let reopened = Store::open(path).unwrap();
    assert_eq!(
        context::verify_handoff(&reopened, checked.acknowledgement)
            .unwrap()
            .context_pack,
        pack.context_pack
    );
}

#[test]
fn context_acknowledgement_cannot_be_relabelled_as_an_attempt_receipt() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("roles.db")).unwrap();
    let mut state = work_state(&mut store);
    let req = request(&mut store, &state, 16000);
    let pack = context::prepare_context(&mut store, &req).unwrap();
    let ack = acknowledgement(&pack);
    let acknowledged =
        context::acknowledge_handoff(&mut store, &serde_json::to_vec(&ack).unwrap()).unwrap();
    state.attempts[0].dispatch_state = DispatchState::ReceiptRecorded;
    for receipt in [
        acknowledged.acknowledgement,
        blob(
            &mut store,
            b"{\"schema\":\"continuum.context_acknowledgement.v1\",\"schema\":\"something_else\"}",
        ),
    ] {
        state.attempts[0].receipt = Some(receipt);
        let req = request(&mut store, &state, 16000);
        assert!(
            context::prepare_context(&mut store, &req)
                .unwrap_err()
                .to_string()
                .contains("not an attempt receipt")
        );
    }
}

#[test]
fn bound_anchor_can_become_stale_without_corrupting_historical_context() {
    let dir = tempdir().unwrap();
    let mut store = Store::open(dir.path().join("anchor.db")).unwrap();
    let state = work_state(&mut store);
    let mut req = request(&mut store, &state, 16000);
    let wrapper = store
        .put(&Object::Snapshot {
            entries: vec![SnapshotEntry {
                path: "work/state.json".into(),
                blob: req.work_state,
            }],
        })
        .unwrap();
    let transition = AcceptRequest {
        acceptor: "local".into(),
        target: "work".into(),
        operation_id: "initial".into(),
        expected: None,
        candidate: wrapper,
    };
    let first = store
        .accept(&transition)
        .unwrap()
        .receipt
        .resulting
        .unwrap();
    req.anchor = Some(AcceptanceAnchor {
        acceptor: "local".into(),
        target: "work".into(),
        expected: first,
        work_state_path: "work/state.json".into(),
    });
    let pack = context::prepare_context(&mut store, &req).unwrap();
    assert_eq!(pack.freshness.status, FreshnessStatus::MatchesAtObservation);
    assert!(
        !context::verify_current_context(&store, pack.context_pack)
            .unwrap()
            .action_authority_verified
    );
    let exact = context::inspect_context(&store, pack.context_pack)
        .unwrap()
        .rendered;
    let mut unrelated = req.clone();
    unrelated.anchor.as_mut().unwrap().work_state_path = "other.json".into();
    assert!(context::prepare_context(&mut store, &unrelated).is_err());
    // Identical accepted bytes at a new generation still make the old anchor stale.
    store
        .accept(&AcceptRequest {
            operation_id: "advance".into(),
            expected: Some(first),
            ..transition
        })
        .unwrap();
    let historical = context::verify_context(&store, pack.context_pack).unwrap();
    assert!(historical.exact_projection_verified);
    assert_eq!(
        historical.freshness.status,
        FreshnessStatus::StaleAtObservation
    );
    assert_eq!(
        context::inspect_context(&store, pack.context_pack)
            .unwrap()
            .rendered,
        exact
    );
    assert!(context::verify_current_context(&store, pack.context_pack).is_err());
    assert!(context::prepare_context(&mut store, &req).is_err());
    let ack = context::acknowledge_handoff(
        &mut store,
        &serde_json::to_vec(&acknowledgement(&pack)).unwrap(),
    )
    .unwrap();
    assert_eq!(ack.freshness.status, FreshnessStatus::StaleAtObservation);
    req.anchor = None;
    let unanchored = context::prepare_context(&mut store, &req).unwrap();
    assert!(context::verify_current_context(&store, unanchored.context_pack).is_err());
}

fn cli(database: &Path, command: &str, argument: &str) -> Value {
    let output = Command::new(env!("CARGO_BIN_EXE_continuum"))
        .arg(command)
        .arg(database)
        .arg(argument)
        .output()
        .unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    serde_json::from_slice(&output.stdout).unwrap()
}

#[test]
fn separately_started_cli_processes_prepare_inspect_and_acknowledge_exact_context() {
    let dir = tempdir().unwrap();
    let database = dir.path().join("processes.db");
    let mut store = Store::open(&database).unwrap();
    let mut state = work_state(&mut store);
    state.attempts[0].dispatch_state = DispatchState::MayHaveBeenSent;
    let req = request(&mut store, &state, 16000);
    let file = dir.path().join("prepare.json");
    fs::write(&file, serde_json::to_vec(&req).unwrap()).unwrap();
    drop(store);
    let prepared = cli(&database, "prepare-context", file.to_str().unwrap());
    let id = prepared["context_pack"].as_str().unwrap();
    let received = cli(&database, "inspect-context", id);
    let text = received["rendered"].as_str().unwrap();
    assert!(text.contains("reconcile_existing_operation"));
    assert!(text.contains("uncertainty:effect"));
    let pack = context::PreparedContext {
        context_pack: id.parse().unwrap(),
        manifest: serde_json::from_value(prepared["manifest"].clone()).unwrap(),
        freshness: serde_json::from_value(prepared["freshness"].clone()).unwrap(),
    };
    let ack_file = dir.path().join("ack.json");
    fs::write(
        &ack_file,
        serde_json::to_vec(&acknowledgement(&pack)).unwrap(),
    )
    .unwrap();
    let ack = cli(&database, "acknowledge-handoff", ack_file.to_str().unwrap());
    let verified = cli(
        &database,
        "verify-handoff",
        ack["acknowledgement"].as_str().unwrap(),
    );
    assert_eq!(verified["reference_consistency_verified"], true);
    assert_eq!(verified["understanding_verified"], false);
    assert_eq!(
        cli(&database, "verify-context", id)["exact_projection_verified"],
        true
    );
}
