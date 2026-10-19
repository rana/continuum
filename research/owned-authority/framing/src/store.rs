//! Owned journal authority for valid v1 objects and complete acceptance outcomes.
use crate::{Error, Object, ObjectId, Result, journal::Journal, object::append_bytes};
use serde::{Deserialize, Serialize};
use std::{collections::BTreeMap, path::Path};

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Head {
    pub root: ObjectId,
    pub generation: u64,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Request {
    pub acceptor: String,
    pub target: String,
    pub operation_id: String,
    pub expected: Option<Head>,
    pub candidate: ObjectId,
}
impl Request {
    pub fn canonical_bytes(&self) -> Result<Vec<u8>> {
        let mut bytes = b"continuum.accept\0\0\x01".to_vec();
        for name in [&self.acceptor, &self.target, &self.operation_id] {
            validate_name(name)?;
            append_bytes(&mut bytes, name.as_bytes())?;
        }
        match self.expected {
            None => bytes.push(0),
            Some(head) => {
                if head.generation == 0 || head.generation > i64::MAX as u64 {
                    return Err(bad("generation range"));
                }
                bytes.push(1);
                bytes.extend(head.root.bytes());
                bytes.extend(head.generation.to_be_bytes());
            }
        }
        bytes.extend(self.candidate.bytes());
        Ok(bytes)
    }
}
fn validate_name(name: &str) -> Result<()> {
    if name.trim().is_empty() || name.len() > 256 || name.chars().any(char::is_control) {
        return Err(bad("invalid name"));
    }
    Ok(())
}
fn bad(message: &str) -> Error {
    Error::Invalid(message.into())
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Receipt {
    pub sequence: u64,
    pub request: Request,
    pub outcome: String,
    pub observed: Option<Head>,
    pub resulting: Option<Head>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Acceptance {
    pub receipt: Receipt,
    pub replayed: bool,
}
#[derive(Serialize, Deserialize)]
#[serde(tag = "record", deny_unknown_fields)]
enum Event {
    ObjectV1 {
        canonical: Vec<u8>,
    },
    AcceptanceV1 {
        request_bytes: Vec<u8>,
        receipt: Box<Receipt>,
    },
}
#[derive(Default)]
struct State {
    objects: BTreeMap<ObjectId, Object>,
    heads: BTreeMap<(String, String), Head>,
    receipts: BTreeMap<(String, String), (Vec<u8>, Receipt)>,
    sequence: u64,
}
impl State {
    fn replay(records: &[Vec<u8>]) -> Result<Self> {
        let mut state = Self::default();
        for bytes in records {
            let event: Event = serde_json::from_slice(bytes)?;
            if serde_json::to_vec(&event)? != *bytes {
                return Err(bad("noncanonical event"));
            }
            state.apply(event)?;
        }
        Ok(state)
    }
    fn kind(&self, id: ObjectId, expected: &str) -> Result<()> {
        if self.objects.get(&id).is_none_or(|o| o.kind() != expected) {
            return Err(bad("missing object or wrong kind"));
        }
        Ok(())
    }
    fn object(&self, bytes: &[u8]) -> Result<(ObjectId, Object)> {
        let object = Object::from_canonical(bytes)?;
        match &object {
            Object::Blob { .. } => (),
            Object::Snapshot { entries } => {
                for entry in entries {
                    self.kind(entry.blob, "blob")?;
                }
            }
            Object::EvidenceRecord {
                candidate, output, ..
            } => {
                self.kind(*candidate, "snapshot")?;
                if let Some(id) = output {
                    self.kind(*id, "blob")?;
                }
            }
        }
        Ok((object.id()?, object))
    }
    fn evaluate(&self, request: &Request) -> Result<Acceptance> {
        let bytes = request.canonical_bytes()?;
        let key = (request.acceptor.clone(), request.operation_id.clone());
        if let Some((old, receipt)) = self.receipts.get(&key) {
            if old != &bytes {
                return Err(Error::OperationConflict);
            }
            return Ok(Acceptance {
                receipt: receipt.clone(),
                replayed: true,
            });
        }
        self.kind(request.candidate, "snapshot")?;
        let observed = self
            .heads
            .get(&(request.acceptor.clone(), request.target.clone()))
            .copied();
        let matches = observed == request.expected;
        let resulting = if matches {
            let generation = observed
                .map_or(0, |h| h.generation)
                .checked_add(1)
                .filter(|n| *n <= i64::MAX as u64)
                .ok_or_else(|| bad("generation exhausted"))?;
            Some(Head {
                root: request.candidate,
                generation,
            })
        } else {
            observed
        };
        let sequence = self
            .sequence
            .checked_add(1)
            .filter(|n| *n <= i64::MAX as u64)
            .ok_or_else(|| bad("sequence exhausted"))?;
        Ok(Acceptance {
            receipt: Receipt {
                sequence,
                request: request.clone(),
                outcome: if matches {
                    "accepted"
                } else {
                    "precondition_failed"
                }
                .into(),
                observed,
                resulting,
            },
            replayed: false,
        })
    }
    fn apply(&mut self, event: Event) -> Result<()> {
        match event {
            Event::ObjectV1 { canonical } => {
                let (id, object) = self.object(&canonical)?;
                if self.objects.insert(id, object).is_some() {
                    return Err(bad("duplicate object event"));
                }
            }
            Event::AcceptanceV1 {
                request_bytes,
                receipt,
            } => {
                let receipt = *receipt;
                if receipt.request.canonical_bytes()? != request_bytes {
                    return Err(bad("request binding"));
                }
                let expected = self.evaluate(&receipt.request)?;
                if expected.replayed || expected.receipt != receipt {
                    return Err(bad("invalid historical receipt"));
                }
                if receipt.outcome == "accepted" {
                    self.heads.insert(
                        (
                            receipt.request.acceptor.clone(),
                            receipt.request.target.clone(),
                        ),
                        receipt.resulting.ok_or_else(|| bad("missing head"))?,
                    );
                }
                self.sequence = receipt.sequence;
                self.receipts.insert(
                    (
                        receipt.request.acceptor.clone(),
                        receipt.request.operation_id.clone(),
                    ),
                    (request_bytes, receipt),
                );
            }
        }
        Ok(())
    }
}

pub struct Store {
    journal: Journal,
    state: State,
}
impl Store {
    pub fn open(path: &Path) -> Result<Self> {
        let journal = Journal::open(path)?;
        let state = State::replay(journal.records()?)?;
        Ok(Self { journal, state })
    }
    pub fn export(&self, destination: &Path, fault: &str) -> Result<()> {
        self.healthy()?;
        crate::archive::publish(destination, &self.journal.image()?, fault)
    }
    pub fn restore(source: &Path, destination: &Path, fault: &str) -> Result<()> {
        let image = crate::archive::read(source)?;
        State::replay(&crate::decode(&image).map_err(|_| bad("archive framing"))?)?;
        Journal::install(destination, &image, fault)?;
        Ok(())
    }
    fn healthy(&self) -> Result<()> {
        self.journal.records()?;
        Ok(())
    }
    pub fn put(&mut self, object: Object) -> Result<ObjectId> {
        self.healthy()?;
        let canonical = object.canonical_bytes()?;
        let (id, _) = self.state.object(&canonical)?;
        if self.state.objects.contains_key(&id) {
            return Ok(id);
        }
        let event = Event::ObjectV1 { canonical };
        self.journal.append(serde_json::to_vec(&event)?, "none")?;
        self.state.apply(event)?;
        Ok(id)
    }
    pub fn get(&self, id: ObjectId) -> Result<&Object> {
        self.healthy()?;
        self.state
            .objects
            .get(&id)
            .ok_or_else(|| bad("object not found"))
    }
    pub fn head(&self, acceptor: &str, target: &str) -> Result<Option<Head>> {
        self.healthy()?;
        validate_name(acceptor)?;
        validate_name(target)?;
        Ok(self
            .state
            .heads
            .get(&(acceptor.into(), target.into()))
            .copied())
    }
    pub fn receipt(&self, acceptor: &str, operation: &str) -> Result<Option<&Receipt>> {
        self.healthy()?;
        validate_name(acceptor)?;
        validate_name(operation)?;
        Ok(self
            .state
            .receipts
            .get(&(acceptor.into(), operation.into()))
            .map(|(_, r)| r))
    }
    pub fn accept(&mut self, request: Request, fault: &str) -> Result<Acceptance> {
        self.healthy()?;
        let result = self.state.evaluate(&request)?;
        if result.replayed {
            return Ok(result);
        }
        let event = Event::AcceptanceV1 {
            request_bytes: request.canonical_bytes()?,
            receipt: Box::new(result.receipt.clone()),
        };
        self.journal.append(serde_json::to_vec(&event)?, fault)?;
        self.state.apply(event)?;
        Ok(result)
    }
}
