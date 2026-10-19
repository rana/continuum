//! Bounded, deterministic projections of caller-authored continuing work.
//!
//! All persisted values use existing v1 Blob objects. This module performs no
//! dispatch and grants no action authority. A context acknowledgement checks
//! explicit references, not authentication, delivery, or understanding.

use crate::{Error, Head, Object, ObjectId, Result, Store};
use serde::{Deserialize, Serialize, de};
use std::{
    collections::{BTreeMap, BTreeSet},
    fmt,
};

pub const MAX_CONTEXT_INPUT_BYTES: usize = 256 * 1024;
pub const MAX_CONTEXT_BYTES: u32 = 256 * 1024;
pub const MAX_CONTEXT_RECORDS: usize = 256;
pub const MAX_CONTEXT_TEXT_BYTES: usize = 8192;
const MAX_REFERENCE_BYTES: usize = 16 * 1024 * 1024;
pub const SELECTOR_REVISION: &str = "continuum.whole_records.v1";
pub const WORK_STATE_SCHEMA: &str = "continuum.work_state.v1";
pub const PREPARE_CONTEXT_SCHEMA: &str = "continuum.prepare_context.v1";
pub const CONTEXT_PACK_SCHEMA: &str = "continuum.context_pack.v1";
pub const CONTEXT_ACKNOWLEDGEMENT_SCHEMA: &str = "continuum.context_acknowledgement.v1";

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Objective {
    pub id: String,
    pub statement: String,
    pub done_when: String,
    pub constraints: Vec<String>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DispatchState {
    NeverDispatched,
    MayHaveBeenSent,
    ReceiptRecorded,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum NextAction {
    IssueFirstRequestIfAuthorized,
    ReconcileExistingOperation,
    InspectRecordedReceipt,
}

impl DispatchState {
    pub fn conditional_next_action(self) -> NextAction {
        match self {
            Self::NeverDispatched => NextAction::IssueFirstRequestIfAuthorized,
            Self::MayHaveBeenSent => NextAction::ReconcileExistingOperation,
            Self::ReceiptRecorded => NextAction::InspectRecordedReceipt,
        }
    }
}

/// Dispatch and outcome fields are authored claims, not instrumented events.
/// A receipt is exact opaque data; its request binding or truth is not inferred.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Attempt {
    pub id: String,
    pub operation_id: String,
    pub source_snapshot: ObjectId,
    pub summary: String,
    pub dispatch_state: DispatchState,
    pub request: ObjectId,
    #[serde(default)]
    pub receipt: Option<ObjectId>,
    pub outcome_note: String,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DecisionState {
    Active,
    Historical,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Decision {
    pub id: String,
    pub state: DecisionState,
    pub statement: String,
    pub basis_attempt_ids: Vec<String>,
    pub reopen_when: String,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Uncertainty {
    pub id: String,
    pub question: String,
    pub why_it_matters: String,
}

/// An authored offer. Storing this record does not send or accept it.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Handoff {
    pub id: String,
    pub from_worker: String,
    pub to_worker: String,
    pub scope: String,
    pub required_decision_ids: Vec<String>,
}

/// One objective and one offered handoff, with their declared local records.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WorkState {
    pub schema: String,
    pub id: String,
    pub source_snapshot: ObjectId,
    pub objective: Objective,
    pub attempts: Vec<Attempt>,
    pub decisions: Vec<Decision>,
    pub uncertainties: Vec<Uncertainty>,
    pub handoff: Handoff,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct AcceptanceAnchor {
    pub acceptor: String,
    pub target: String,
    pub expected: Head,
    pub work_state_path: String,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PrepareContextRequest {
    pub schema: String,
    pub work_state: ObjectId,
    pub max_bytes: u32,
    #[serde(default)]
    pub anchor: Option<AcceptanceAnchor>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RecordKind {
    WorkState,
    Objective,
    Attempt,
    Decision,
    Uncertainty,
    Handoff,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SelectionReason {
    WorkIdentity,
    ObjectiveAndConstraints,
    AttemptRecovery,
    ActiveDecision,
    HandoffDependency,
    UnresolvedUncertainty,
    OfferedHandoff,
    OptionalHistory,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Selection {
    pub id: String,
    pub kind: RecordKind,
    pub reason: SelectionReason,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Omission {
    pub id: String,
    pub kind: RecordKind,
    pub reason: String,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ContextPack {
    pub schema: String,
    pub work_state: ObjectId,
    pub work_state_id: String,
    pub source_snapshot: ObjectId,
    pub handoff_id: String,
    pub selector_revision: String,
    pub budget_method: String,
    pub max_bytes: u32,
    pub rendered: ObjectId,
    pub rendered_bytes: u32,
    pub included: Vec<Selection>,
    pub omitted: Vec<Omission>,
    pub anchor: Option<AcceptanceAnchor>,
    pub limits: Vec<String>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum FreshnessStatus {
    UnanchoredFreshnessUnchecked,
    MatchesAtObservation,
    StaleAtObservation,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FreshnessObservation {
    pub status: FreshnessStatus,
    pub observed: Option<Head>,
}

#[derive(Clone, Debug, Serialize)]
pub struct PreparedContext {
    pub context_pack: ObjectId,
    pub manifest: ContextPack,
    pub freshness: FreshnessObservation,
}

#[derive(Clone, Debug, Serialize)]
pub struct ContextInspection {
    pub context_pack: ObjectId,
    pub manifest: ContextPack,
    pub rendered: String,
    pub freshness: FreshnessObservation,
}

#[derive(Clone, Debug, Serialize)]
pub struct ContextVerification {
    pub context_pack: ObjectId,
    pub exact_projection_verified: bool,
    pub rendered_bytes: u32,
    pub freshness: FreshnessObservation,
    pub action_authority_verified: bool,
}

/// A recipient's explicit context-reference declaration. No execution outcome,
/// handoff acceptance, or semantic understanding is represented by this type.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ContextAcknowledgement {
    pub schema: String,
    pub id: String,
    pub context_pack: ObjectId,
    pub handoff_id: String,
    pub recipient_worker: String,
    pub included_ids: Vec<String>,
    pub omitted_ids: Vec<String>,
    pub note: String,
}

#[derive(Clone, Debug, Serialize)]
pub struct AcknowledgementVerification {
    pub acknowledgement: ObjectId,
    pub context_pack: ObjectId,
    pub handoff_id: String,
    pub recipient_worker: String,
    pub reference_consistency_verified: bool,
    pub recipient_authenticated: bool,
    pub understanding_verified: bool,
    pub external_effect_verified: bool,
    pub freshness: FreshnessObservation,
}

fn invalid(message: impl Into<String>) -> Error {
    Error::Invalid(message.into())
}

fn stable_id(value: &str) -> Result<()> {
    if value.is_empty()
        || value.len() > 128
        || value.starts_with("sha256:")
        || !value
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b"-_.:".contains(&b))
    {
        return Err(invalid(
            "stable IDs must be 1..128 ASCII letters/digits/-_.: and distinct from content IDs",
        ));
    }
    Ok(())
}

fn bounded_text(value: &str) -> Result<()> {
    if value.trim().is_empty() || value.len() > MAX_CONTEXT_TEXT_BYTES || value.contains('\0') {
        return Err(invalid(
            "context text must be nonempty, NUL-free, and at most 8192 UTF-8 bytes",
        ));
    }
    Ok(())
}

fn unique_ids(values: &[String]) -> Result<BTreeSet<&str>> {
    if values.len() > MAX_CONTEXT_RECORDS {
        return Err(invalid("too many ID references"));
    }
    let mut result = BTreeSet::new();
    for value in values {
        stable_id(value)?;
        if !result.insert(value.as_str()) {
            return Err(invalid("duplicate stable ID reference"));
        }
    }
    Ok(result)
}

/// Reject duplicate object keys at every depth, including escaped spellings,
/// before typed decoding. JSON bytes remain untouched in their source Blob.
pub fn decode_context_json<T: de::DeserializeOwned>(bytes: &[u8]) -> Result<T> {
    if bytes.len() > MAX_CONTEXT_INPUT_BYTES {
        return Err(invalid("context JSON exceeds 256 KiB"));
    }
    let mut decoder = serde_json::Deserializer::from_slice(bytes);
    UniqueJson::deserialize(&mut decoder)?;
    decoder.end()?;
    Ok(serde_json::from_slice(bytes)?)
}

struct UniqueJson;
impl<'de> Deserialize<'de> for UniqueJson {
    fn deserialize<D: de::Deserializer<'de>>(decoder: D) -> std::result::Result<Self, D::Error> {
        struct Visitor;
        impl<'de> de::Visitor<'de> for Visitor {
            type Value = UniqueJson;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                f.write_str("JSON with unique object keys")
            }
            fn visit_bool<E: de::Error>(self, _: bool) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_i64<E: de::Error>(self, _: i64) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_u64<E: de::Error>(self, _: u64) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_f64<E: de::Error>(self, _: f64) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_str<E: de::Error>(self, _: &str) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_unit<E: de::Error>(self) -> std::result::Result<Self::Value, E> {
                Ok(UniqueJson)
            }
            fn visit_seq<A: de::SeqAccess<'de>>(
                self,
                mut seq: A,
            ) -> std::result::Result<Self::Value, A::Error> {
                while seq.next_element::<UniqueJson>()?.is_some() {}
                Ok(UniqueJson)
            }
            fn visit_map<A: de::MapAccess<'de>>(
                self,
                mut map: A,
            ) -> std::result::Result<Self::Value, A::Error> {
                let mut keys = BTreeSet::new();
                while let Some(key) = map.next_key::<String>()? {
                    if !keys.insert(key) {
                        return Err(de::Error::custom("duplicate JSON object key"));
                    }
                    map.next_value::<UniqueJson>()?;
                }
                Ok(UniqueJson)
            }
        }
        decoder.deserialize_any(Visitor)
    }
}

pub fn parse_work_state(bytes: &[u8]) -> Result<WorkState> {
    let state: WorkState = decode_context_json(bytes)?;
    if state.schema != WORK_STATE_SCHEMA {
        return Err(invalid("unsupported work-state schema"));
    }
    if 3 + state.attempts.len() + state.decisions.len() + state.uncertainties.len()
        > MAX_CONTEXT_RECORDS
    {
        return Err(invalid("work state exceeds 256 records"));
    }
    let mut ids = BTreeSet::new();
    let mut record_id = |id: &str| -> Result<()> {
        stable_id(id)?;
        if !ids.insert(id.to_owned()) {
            return Err(invalid("duplicate work-state record ID"));
        }
        Ok(())
    };
    record_id(&state.id)?;
    record_id(&state.objective.id)?;
    record_id(&state.handoff.id)?;
    bounded_text(&state.objective.statement)?;
    bounded_text(&state.objective.done_when)?;
    if state.objective.constraints.len() > 32 {
        return Err(invalid("too many objective constraints"));
    }
    for constraint in &state.objective.constraints {
        bounded_text(constraint)?;
    }
    let mut operations = BTreeSet::new();
    let mut attempts = BTreeSet::new();
    for attempt in &state.attempts {
        record_id(&attempt.id)?;
        stable_id(&attempt.operation_id)?;
        if !operations.insert(&attempt.operation_id) {
            return Err(invalid(
                "duplicate operation ID; one declared attempt per operation in v1",
            ));
        }
        attempts.insert(attempt.id.as_str());
        bounded_text(&attempt.summary)?;
        bounded_text(&attempt.outcome_note)?;
        if (attempt.dispatch_state == DispatchState::ReceiptRecorded) != attempt.receipt.is_some() {
            return Err(invalid(
                "only receipt_recorded requires and permits an attempt receipt",
            ));
        }
    }
    let mut decisions = BTreeSet::new();
    for decision in &state.decisions {
        record_id(&decision.id)?;
        decisions.insert(decision.id.as_str());
        bounded_text(&decision.statement)?;
        bounded_text(&decision.reopen_when)?;
        if !unique_ids(&decision.basis_attempt_ids)?.is_subset(&attempts) {
            return Err(invalid("decision has a dangling attempt reference"));
        }
    }
    for uncertainty in &state.uncertainties {
        record_id(&uncertainty.id)?;
        bounded_text(&uncertainty.question)?;
        bounded_text(&uncertainty.why_it_matters)?;
    }
    stable_id(&state.handoff.from_worker)?;
    stable_id(&state.handoff.to_worker)?;
    bounded_text(&state.handoff.scope)?;
    if !unique_ids(&state.handoff.required_decision_ids)?.is_subset(&decisions) {
        return Err(invalid("handoff has a dangling decision reference"));
    }
    Ok(state)
}

fn blob(store: &Store, id: ObjectId) -> Result<Vec<u8>> {
    match store.get(id)? {
        Object::Blob { bytes } => Ok(bytes),
        _ => Err(Error::WrongKind {
            id,
            expected: "blob",
        }),
    }
}

// This only recognizes a declared JSON schema; opaque receipts are never
// interpreted as successful effects. Duplicate schema keys cannot hide it.
fn is_context_acknowledgement(bytes: &[u8]) -> bool {
    struct SchemaProbe;
    impl<'de> de::Visitor<'de> for SchemaProbe {
        type Value = bool;
        fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
            f.write_str("a JSON object")
        }
        fn visit_map<A: de::MapAccess<'de>>(
            self,
            mut map: A,
        ) -> std::result::Result<bool, A::Error> {
            let mut found = false;
            while let Some((key, value)) = map.next_entry::<String, serde_json::Value>()? {
                found |= key == "schema" && value.as_str() == Some(CONTEXT_ACKNOWLEDGEMENT_SCHEMA);
            }
            Ok(found)
        }
    }
    use serde::Deserializer;
    let mut decoder = serde_json::Deserializer::from_slice(bytes);
    decoder.deserialize_map(SchemaProbe).unwrap_or(false)
}

fn validate_custody(
    store: &Store,
    state: &WorkState,
    request: &PrepareContextRequest,
) -> Result<()> {
    let mut checked: BTreeMap<ObjectId, (&str, bool)> = BTreeMap::new();
    let mut total = 0usize;
    let mut require = |id: ObjectId, kind: &'static str, attempt_receipt: bool| -> Result<()> {
        if let std::collections::btree_map::Entry::Vacant(entry) = checked.entry(id) {
            let object = store.get(id)?;
            total = total
                .checked_add(object.canonical_bytes()?.len())
                .ok_or_else(|| invalid("reference byte total overflow"))?;
            if total > MAX_REFERENCE_BYTES {
                return Err(invalid("direct referenced objects exceed 16 MiB"));
            }
            let ack =
                matches!(&object, Object::Blob { bytes } if is_context_acknowledgement(bytes));
            entry.insert((object.kind(), ack));
        }
        let (actual, ack) = checked[&id];
        if actual != kind {
            return Err(Error::WrongKind { id, expected: kind });
        }
        if attempt_receipt && ack {
            return Err(invalid(
                "a context acknowledgement is not an attempt receipt",
            ));
        }
        Ok(())
    };
    require(state.source_snapshot, "snapshot", false)?;
    for attempt in &state.attempts {
        require(attempt.source_snapshot, "snapshot", false)?;
        require(attempt.request, "blob", false)?;
        if let Some(receipt) = attempt.receipt {
            require(receipt, "blob", true)?;
        }
    }
    if let Some(anchor) = &request.anchor {
        if anchor.expected.generation == 0 || anchor.expected.generation > i64::MAX as u64 {
            return Err(invalid("anchor generation must be in 1..=i64::MAX"));
        }
        require(anchor.expected.root, "snapshot", false)?;
        let Object::Snapshot { entries } = store.get(anchor.expected.root)? else {
            unreachable!()
        };
        if !entries
            .iter()
            .any(|entry| entry.path == anchor.work_state_path && entry.blob == request.work_state)
        {
            return Err(invalid(
                "anchor snapshot path does not bind the exact work-state Blob",
            ));
        }
    }
    Ok(())
}

fn limits() -> Vec<String> {
    [
        "Authored claims are unverified; current action authority and external-effect truth are not established.",
        "Conditional guidance assumes the authored dispatch state is accurate; this store is not an external dispatch ledger.",
        "Only this WorkState's declared records and direct object references are checked; source files are not materialized.",
        "Whole records only; unrequired historical decisions may be omitted; no truncation or token estimate.",
        "Head freshness is observed once; later effects need action-time authority and expected-head checks.",
        "Context acknowledgements check references, not authenticated authorship, delivery, understanding, acceptance, or completion.",
    ].into_iter().map(str::to_owned).collect()
}

#[derive(Serialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
enum RenderRecord<'a> {
    Objective {
        authored: &'a Objective,
    },
    Attempt {
        authored: &'a Attempt,
        conditional_next_action: NextAction,
        guidance_basis: &'static str,
    },
    Decision {
        authored: &'a Decision,
        basis_unresolved: bool,
        basis_validity: &'static str,
    },
    Uncertainty {
        authored: &'a Uncertainty,
    },
    Handoff {
        authored: &'a Handoff,
    },
}

fn push_line(out: &mut Vec<u8>, value: &impl Serialize) -> Result<()> {
    serde_json::to_writer(&mut *out, value)?;
    out.push(b'\n');
    Ok(())
}

fn render(
    state: &WorkState,
    request: &PrepareContextRequest,
    selected: &BTreeSet<&str>,
) -> Result<(Vec<u8>, Vec<Selection>, Vec<Omission>)> {
    let mut out = Vec::new();
    push_line(
        &mut out,
        &serde_json::json!({
            "kind":"work_state", "schema":"continuum.rendered_context.v1", "id":state.id,
            "work_state":request.work_state, "source_snapshot":state.source_snapshot,
            "selector_revision":SELECTOR_REVISION, "budget_method":"utf8_bytes_including_newlines",
            "max_bytes":request.max_bytes, "anchor":request.anchor, "limits":limits()
        }),
    )?;
    let mut included = Vec::new();
    let mut select = |id: &str, kind, reason| {
        included.push(Selection {
            id: id.into(),
            kind,
            reason,
        })
    };
    select(
        &state.id,
        RecordKind::WorkState,
        SelectionReason::WorkIdentity,
    );
    push_line(
        &mut out,
        &RenderRecord::Objective {
            authored: &state.objective,
        },
    )?;
    select(
        &state.objective.id,
        RecordKind::Objective,
        SelectionReason::ObjectiveAndConstraints,
    );
    let mut attempts: Vec<_> = state.attempts.iter().collect();
    attempts.sort_by_key(|a| &a.id);
    for attempt in attempts {
        push_line(
            &mut out,
            &RenderRecord::Attempt {
                authored: attempt,
                conditional_next_action: attempt.dispatch_state.conditional_next_action(),
                guidance_basis: "authored_dispatch_state_not_independently_verified",
            },
        )?;
        select(
            &attempt.id,
            RecordKind::Attempt,
            SelectionReason::AttemptRecovery,
        );
    }
    let mut decisions: Vec<_> = state.decisions.iter().collect();
    decisions.sort_by_key(|d| &d.id);
    let mut omitted = Vec::new();
    for decision in decisions {
        if !selected.contains(decision.id.as_str()) {
            omitted.push(Omission {
                id: decision.id.clone(),
                kind: RecordKind::Decision,
                reason: "byte_budget_optional_history".into(),
            });
            continue;
        }
        let basis_unresolved = decision.basis_attempt_ids.iter().any(|id| {
            state
                .attempts
                .iter()
                .any(|a| a.id == *id && a.dispatch_state == DispatchState::MayHaveBeenSent)
        });
        push_line(
            &mut out,
            &RenderRecord::Decision {
                authored: decision,
                basis_unresolved,
                basis_validity: "not_established_by_dispatch_state_or_blob_custody",
            },
        )?;
        let reason = if decision.state == DecisionState::Active {
            SelectionReason::ActiveDecision
        } else if state.handoff.required_decision_ids.contains(&decision.id) {
            SelectionReason::HandoffDependency
        } else {
            SelectionReason::OptionalHistory
        };
        select(&decision.id, RecordKind::Decision, reason);
    }
    let mut uncertainties: Vec<_> = state.uncertainties.iter().collect();
    uncertainties.sort_by_key(|u| &u.id);
    for uncertainty in uncertainties {
        push_line(
            &mut out,
            &RenderRecord::Uncertainty {
                authored: uncertainty,
            },
        )?;
        select(
            &uncertainty.id,
            RecordKind::Uncertainty,
            SelectionReason::UnresolvedUncertainty,
        );
    }
    push_line(
        &mut out,
        &RenderRecord::Handoff {
            authored: &state.handoff,
        },
    )?;
    select(
        &state.handoff.id,
        RecordKind::Handoff,
        SelectionReason::OfferedHandoff,
    );
    push_line(
        &mut out,
        &serde_json::json!({"kind":"coverage", "included_ids":included.iter().map(|s| &s.id).collect::<Vec<_>>(), "omitted":omitted}),
    )?;
    Ok((out, included, omitted))
}

fn project(
    store: &Store,
    request: &PrepareContextRequest,
) -> Result<(WorkState, ContextPack, Vec<u8>)> {
    if request.schema != PREPARE_CONTEXT_SCHEMA {
        return Err(invalid("unsupported prepare-context schema"));
    }
    if request.max_bytes == 0 || request.max_bytes > MAX_CONTEXT_BYTES {
        return Err(invalid("context byte budget must be in 1..=262144"));
    }
    let state = parse_work_state(&blob(store, request.work_state)?)?;
    validate_custody(store, &state, request)?;
    let mut selected: BTreeSet<_> = state
        .decisions
        .iter()
        .filter(|d| {
            d.state == DecisionState::Active || state.handoff.required_decision_ids.contains(&d.id)
        })
        .map(|d| d.id.as_str())
        .collect();
    let mandatory = render(&state, request, &selected)?;
    if mandatory.0.len() > request.max_bytes as usize {
        return Err(invalid(format!(
            "byte budget cannot retain critical records and coverage: need {} bytes, budget {}",
            mandatory.0.len(),
            request.max_bytes
        )));
    }
    let mut optional: Vec<_> = state
        .decisions
        .iter()
        .filter(|d| !selected.contains(d.id.as_str()))
        .collect();
    optional.sort_by_key(|d| &d.id);
    for decision in optional {
        selected.insert(&decision.id);
        if render(&state, request, &selected)?.0.len() > request.max_bytes as usize {
            selected.remove(decision.id.as_str());
        }
    }
    let (rendered, included, omitted) = render(&state, request, &selected)?;
    let manifest = ContextPack {
        schema: CONTEXT_PACK_SCHEMA.into(),
        work_state: request.work_state,
        work_state_id: state.id.clone(),
        source_snapshot: state.source_snapshot,
        handoff_id: state.handoff.id.clone(),
        selector_revision: SELECTOR_REVISION.into(),
        budget_method: "utf8_bytes_including_newlines".into(),
        max_bytes: request.max_bytes,
        rendered: Object::Blob {
            bytes: rendered.clone(),
        }
        .id()?,
        rendered_bytes: rendered.len() as u32,
        included,
        omitted,
        anchor: request.anchor.clone(),
        limits: limits(),
    };
    Ok((state, manifest, rendered))
}

fn observe_freshness(
    store: &Store,
    anchor: Option<&AcceptanceAnchor>,
) -> Result<FreshnessObservation> {
    match anchor {
        None => Ok(FreshnessObservation {
            status: FreshnessStatus::UnanchoredFreshnessUnchecked,
            observed: None,
        }),
        Some(anchor) => {
            let observed = store.head(&anchor.acceptor, &anchor.target)?;
            Ok(FreshnessObservation {
                status: if observed == Some(anchor.expected) {
                    FreshnessStatus::MatchesAtObservation
                } else {
                    FreshnessStatus::StaleAtObservation
                },
                observed,
            })
        }
    }
}

pub fn prepare_context(
    store: &mut Store,
    request: &PrepareContextRequest,
) -> Result<PreparedContext> {
    let (_, manifest, rendered) = project(store, request)?;
    let freshness = observe_freshness(store, request.anchor.as_ref())?;
    if freshness.status == FreshnessStatus::StaleAtObservation {
        return Err(invalid("prepare-context anchor is stale at observation"));
    }
    // Immutable children precede the manifest. A failure can leave unreferenced
    // Blobs; there is no accepted-state mutation or multi-object transaction.
    store.put(&Object::Blob { bytes: rendered })?;
    let context_pack = store.put(&Object::Blob {
        bytes: serde_json::to_vec(&manifest)?,
    })?;
    Ok(PreparedContext {
        context_pack,
        manifest,
        freshness,
    })
}

fn checked_pack(store: &Store, id: ObjectId) -> Result<(WorkState, ContextPack, Vec<u8>)> {
    let bytes = blob(store, id)?;
    let manifest: ContextPack = decode_context_json(&bytes)?;
    if manifest.schema != CONTEXT_PACK_SCHEMA || manifest.selector_revision != SELECTOR_REVISION {
        return Err(invalid(
            "unsupported context-pack schema or selector revision",
        ));
    }
    let request = PrepareContextRequest {
        schema: PREPARE_CONTEXT_SCHEMA.into(),
        work_state: manifest.work_state,
        max_bytes: manifest.max_bytes,
        anchor: manifest.anchor.clone(),
    };
    let (state, expected, rendered) = project(store, &request)?;
    if manifest != expected || bytes != serde_json::to_vec(&expected)? {
        return Err(invalid(
            "context manifest does not match the exact deterministic projection",
        ));
    }
    if blob(store, manifest.rendered)? != rendered {
        return Err(invalid(
            "rendered context does not match the deterministic selector",
        ));
    }
    Ok((state, manifest, rendered))
}

pub fn inspect_context(store: &Store, id: ObjectId) -> Result<ContextInspection> {
    let (_, manifest, rendered) = checked_pack(store, id)?;
    let freshness = observe_freshness(store, manifest.anchor.as_ref())?;
    let rendered =
        String::from_utf8(rendered).map_err(|_| invalid("rendered context is not UTF-8"))?;
    Ok(ContextInspection {
        context_pack: id,
        manifest,
        rendered,
        freshness,
    })
}

pub fn verify_context(store: &Store, id: ObjectId) -> Result<ContextVerification> {
    let (_, manifest, _) = checked_pack(store, id)?;
    Ok(ContextVerification {
        context_pack: id,
        exact_projection_verified: true,
        rendered_bytes: manifest.rendered_bytes,
        freshness: observe_freshness(store, manifest.anchor.as_ref())?,
        action_authority_verified: false,
    })
}

/// This is an at-observation-time comparison, not authorization for a later effect.
pub fn verify_current_context(store: &Store, id: ObjectId) -> Result<ContextVerification> {
    let verified = verify_context(store, id)?;
    if verified.freshness.status != FreshnessStatus::MatchesAtObservation {
        return Err(invalid(
            "context has no matching current anchor at observation; historical verification remains available",
        ));
    }
    Ok(verified)
}

fn check_acknowledgement(store: &Store, bytes: &[u8]) -> Result<AcknowledgementVerification> {
    let acknowledgement: ContextAcknowledgement = decode_context_json(bytes)?;
    if acknowledgement.schema != CONTEXT_ACKNOWLEDGEMENT_SCHEMA {
        return Err(invalid("unsupported context-acknowledgement schema"));
    }
    stable_id(&acknowledgement.id)?;
    stable_id(&acknowledgement.recipient_worker)?;
    bounded_text(&acknowledgement.note)?;
    let (state, manifest, _) = checked_pack(store, acknowledgement.context_pack)?;
    if acknowledgement.recipient_worker != state.handoff.to_worker
        || acknowledgement.handoff_id != state.handoff.id
    {
        return Err(invalid(
            "acknowledgement must name the offered recipient and handoff",
        ));
    }
    let included: BTreeSet<_> = manifest.included.iter().map(|s| s.id.as_str()).collect();
    let omitted: BTreeSet<_> = manifest.omitted.iter().map(|s| s.id.as_str()).collect();
    if included.contains(acknowledgement.id.as_str())
        || omitted.contains(acknowledgement.id.as_str())
    {
        return Err(invalid("acknowledgement needs its own stable record ID"));
    }
    if unique_ids(&acknowledgement.included_ids)? != included
        || unique_ids(&acknowledgement.omitted_ids)? != omitted
    {
        return Err(invalid(
            "acknowledgement selection references do not match the context pack",
        ));
    }
    Ok(AcknowledgementVerification {
        acknowledgement: Object::Blob {
            bytes: bytes.to_vec(),
        }
        .id()?,
        context_pack: acknowledgement.context_pack,
        handoff_id: acknowledgement.handoff_id,
        recipient_worker: acknowledgement.recipient_worker,
        reference_consistency_verified: true,
        recipient_authenticated: false,
        understanding_verified: false,
        external_effect_verified: false,
        freshness: observe_freshness(store, manifest.anchor.as_ref())?,
    })
}

pub fn acknowledge_handoff(
    store: &mut Store,
    exact_json: &[u8],
) -> Result<AcknowledgementVerification> {
    let verification = check_acknowledgement(store, exact_json)?;
    store.put(&Object::Blob {
        bytes: exact_json.to_vec(),
    })?;
    Ok(verification)
}

pub fn verify_handoff(
    store: &Store,
    acknowledgement: ObjectId,
) -> Result<AcknowledgementVerification> {
    check_acknowledgement(store, &blob(store, acknowledgement)?)
}
