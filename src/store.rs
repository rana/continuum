use crate::{Error, Object, ObjectId, Result, object::append_bytes};
use rusqlite::{Connection, OptionalExtension, TransactionBehavior, params};
use serde::{Deserialize, Serialize};
use std::{collections::BTreeSet, path::Path, time::Duration};

const APPLICATION_ID: i64 = 0x434f4e54;
const DATABASE_VERSION: i64 = 1;

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Head {
    pub root: ObjectId,
    pub generation: u64,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct AcceptRequest {
    pub acceptor: String,
    pub target: String,
    pub operation_id: String,
    pub expected: Option<Head>,
    pub candidate: ObjectId,
}

impl AcceptRequest {
    fn canonical_bytes(&self) -> Result<Vec<u8>> {
        let mut out = b"continuum.accept\0\x00\x01".to_vec();
        for value in [&self.acceptor, &self.target, &self.operation_id] {
            validate_name(value)?;
            append_bytes(&mut out, value.as_bytes())?;
        }
        match self.expected {
            None => out.push(0),
            Some(head) => {
                if head.generation == 0 || head.generation > i64::MAX as u64 {
                    return Err(Error::Invalid(
                        "expected generation must be in 1..=i64::MAX".into(),
                    ));
                }
                out.push(1);
                out.extend(head.root.bytes());
                out.extend(head.generation.to_be_bytes());
            }
        }
        out.extend(self.candidate.bytes());
        Ok(out)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    Accepted,
    PreconditionFailed,
}

/// A historical result. It is not a statement about the head at read time.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Receipt {
    pub sequence: u64,
    pub request: AcceptRequest,
    pub outcome: Outcome,
    pub observed: Option<Head>,
    pub resulting: Option<Head>,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct Acceptance {
    pub receipt: Receipt,
    pub replayed: bool,
}

pub struct Store {
    connection: Connection,
}

impl Store {
    /// Opens or creates a local database. WAL + FULL synchronization provide
    /// SQLite's durability guarantees, subject to OS/filesystem/device behavior.
    pub fn open(path: impl AsRef<Path>) -> Result<Self> {
        let mut connection = Connection::open(path)?;
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.pragma_update(None, "foreign_keys", "ON")?;
        connection.pragma_update(None, "synchronous", "FULL")?;
        {
            let tx = connection.transaction_with_behavior(TransactionBehavior::Immediate)?;
            let application: i64 = tx.pragma_query_value(None, "application_id", |r| r.get(0))?;
            let version: i64 = tx.pragma_query_value(None, "user_version", |r| r.get(0))?;
            if application == 0 && version == 0 {
                let tables: i64 = tx.query_row(
                    "SELECT count(*) FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'",
                    [],
                    |r| r.get(0),
                )?;
                if tables != 0 {
                    return Err(Error::UnsupportedDatabase(
                        "refusing to initialize a nonempty unrelated database".into(),
                    ));
                }
                tx.execute_batch(SCHEMA)?;
                tx.pragma_update(None, "application_id", APPLICATION_ID)?;
                tx.pragma_update(None, "user_version", DATABASE_VERSION)?;
            } else if application != APPLICATION_ID || version != DATABASE_VERSION {
                return Err(Error::UnsupportedDatabase(format!(
                    "application={application}, version={version}"
                )));
            }
            tx.commit()?;
        }
        let journal_mode: String =
            connection.pragma_query_value(None, "journal_mode", |r| r.get(0))?;
        if journal_mode != "wal" {
            let mode: String = connection.query_row("PRAGMA journal_mode=WAL", [], |r| r.get(0))?;
            if mode != "wal" {
                return Err(Error::UnsupportedDatabase(
                    "WAL mode is required; use a local file-backed database".into(),
                ));
            }
        }
        Ok(Self { connection })
    }

    pub fn put(&mut self, object: &Object) -> Result<ObjectId> {
        let canonical = object.canonical_bytes()?;
        let id = ObjectId::of(&canonical);
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        match object {
            Object::Blob { .. } => {}
            Object::Snapshot { entries } => {
                let mut checked = BTreeSet::new();
                for entry in entries {
                    if checked.insert(entry.blob) {
                        require_kind(&tx, entry.blob, "blob")?;
                    }
                }
            }
            Object::EvidenceRecord {
                candidate, output, ..
            } => {
                require_kind(&tx, *candidate, "snapshot")?;
                if let Some(output) = output {
                    require_kind(&tx, *output, "blob")?;
                }
            }
        }
        let existing: Option<Vec<u8>> = tx
            .query_row(
                "SELECT canonical FROM objects WHERE id=?1",
                [id.to_string()],
                |r| r.get(0),
            )
            .optional()?;
        match existing {
            Some(bytes) if bytes != canonical => return Err(Error::Integrity(id)),
            Some(_) => {}
            None => {
                tx.execute(
                    "INSERT INTO objects(id,canonical) VALUES (?1,?2)",
                    params![id.to_string(), canonical],
                )?;
            }
        }
        tx.commit()?;
        Ok(id)
    }

    pub fn get(&self, id: ObjectId) -> Result<Object> {
        load_object(&self.connection, id)
    }

    pub fn head(&self, acceptor: &str, target: &str) -> Result<Option<Head>> {
        validate_name(acceptor)?;
        validate_name(target)?;
        read_head(&self.connection, acceptor, target)
    }

    pub fn receipt(&self, acceptor: &str, operation_id: &str) -> Result<Option<Receipt>> {
        validate_name(acceptor)?;
        validate_name(operation_id)?;
        let value: Option<String> = self
            .connection
            .query_row(
                "SELECT receipt FROM events WHERE acceptor=?1 AND operation_id=?2",
                params![acceptor, operation_id],
                |r| r.get(0),
            )
            .optional()?;
        value
            .map(|json| serde_json::from_str(&json).map_err(Error::from))
            .transpose()
    }

    pub fn events(&self, acceptor: &str, target: &str) -> Result<Vec<Receipt>> {
        validate_name(acceptor)?;
        validate_name(target)?;
        let mut statement = self.connection.prepare(
            "SELECT receipt FROM events WHERE acceptor=?1 AND target=?2 ORDER BY sequence",
        )?;
        let rows = statement.query_map(params![acceptor, target], |r| r.get::<_, String>(0))?;
        rows.map(|row| Ok(serde_json::from_str(&row?)?)).collect()
    }

    /// Atomically records one result and, when its full expected head matches,
    /// advances the target. No authentication or evidence policy is performed.
    pub fn accept(&mut self, request: &AcceptRequest) -> Result<Acceptance> {
        let canonical_request = request.canonical_bytes()?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let old: Option<(Vec<u8>, String)> = tx
            .query_row(
                "SELECT request,receipt FROM events WHERE acceptor=?1 AND operation_id=?2",
                params![request.acceptor, request.operation_id],
                |r| Ok((r.get(0)?, r.get(1)?)),
            )
            .optional()?;
        if let Some((previous, receipt)) = old {
            if previous != canonical_request {
                return Err(Error::OperationConflict);
            }
            return Ok(Acceptance {
                receipt: serde_json::from_str(&receipt)?,
                replayed: true,
            });
        }
        require_kind(&tx, request.candidate, "snapshot")?;
        let observed = read_head(&tx, &request.acceptor, &request.target)?;
        let matches = observed == request.expected;
        let resulting = if matches {
            let generation = observed
                .map_or(0, |h| h.generation)
                .checked_add(1)
                .filter(|n| *n <= i64::MAX as u64)
                .ok_or_else(|| Error::Invalid("target generation exhausted".into()))?;
            Some(Head {
                root: request.candidate,
                generation,
            })
        } else {
            observed
        };
        let last: i64 = tx.query_row("SELECT coalesce(max(sequence),0) FROM events", [], |r| {
            r.get(0)
        })?;
        let sequence = last
            .checked_add(1)
            .ok_or_else(|| Error::Invalid("event sequence exhausted".into()))?;
        let receipt = Receipt {
            sequence: sequence as u64,
            request: request.clone(),
            outcome: if matches {
                Outcome::Accepted
            } else {
                Outcome::PreconditionFailed
            },
            observed,
            resulting,
        };
        tx.execute(
            "INSERT INTO events(sequence,acceptor,target,operation_id,request,receipt) VALUES (?1,?2,?3,?4,?5,?6)",
            params![sequence, request.acceptor, request.target, request.operation_id, canonical_request, serde_json::to_string(&receipt)?],
        )?;
        if matches {
            let head = resulting.ok_or_else(|| Error::Invalid("missing resulting head".into()))?;
            tx.execute(
                "INSERT INTO heads(acceptor,target,root,generation) VALUES (?1,?2,?3,?4)
                 ON CONFLICT(acceptor,target) DO UPDATE SET root=excluded.root,generation=excluded.generation",
                params![request.acceptor, request.target, head.root.to_string(), head.generation as i64],
            )?;
        }
        failpoint("before_commit");
        tx.commit()?;
        failpoint("after_commit");
        Ok(Acceptance {
            receipt,
            replayed: false,
        })
    }
}

fn validate_name(value: &str) -> Result<()> {
    if value.trim().is_empty() || value.len() > 256 || value.chars().any(char::is_control) {
        return Err(Error::Invalid("namespace and operation names must contain 1..=256 UTF-8 bytes without control characters".into()));
    }
    Ok(())
}

fn read_head(connection: &Connection, acceptor: &str, target: &str) -> Result<Option<Head>> {
    let row: Option<(String, i64)> = connection
        .query_row(
            "SELECT root,generation FROM heads WHERE acceptor=?1 AND target=?2",
            params![acceptor, target],
            |r| Ok((r.get(0)?, r.get(1)?)),
        )
        .optional()?;
    row.map(|(root, generation)| {
        if generation <= 0 {
            return Err(Error::Invalid("invalid persisted generation".into()));
        }
        Ok(Head {
            root: root.parse()?,
            generation: generation as u64,
        })
    })
    .transpose()
}

fn load_object(connection: &Connection, id: ObjectId) -> Result<Object> {
    let bytes: Option<Vec<u8>> = connection
        .query_row(
            "SELECT canonical FROM objects WHERE id=?1",
            [id.to_string()],
            |r| r.get(0),
        )
        .optional()?;
    let bytes = bytes.ok_or(Error::NotFound(id))?;
    if ObjectId::of(&bytes) != id {
        return Err(Error::Integrity(id));
    }
    Object::from_canonical(&bytes)
}

fn require_kind(connection: &Connection, id: ObjectId, expected: &'static str) -> Result<()> {
    if load_object(connection, id)?.kind() != expected {
        return Err(Error::WrongKind { id, expected });
    }
    Ok(())
}

fn failpoint(_name: &str) {
    #[cfg(feature = "fault-injection")]
    if std::env::var("CONTINUUM_FAILPOINT").as_deref() == Ok(_name) {
        // exit bypasses Rust destructors: SQLite must recover without a clean
        // Transaction drop. This tests process death, not power-loss behavior.
        std::process::exit(86);
    }
}

const SCHEMA: &str = "
CREATE TABLE objects (
    id TEXT PRIMARY KEY NOT NULL,
    canonical BLOB NOT NULL
) STRICT;
CREATE TABLE heads (
    acceptor TEXT NOT NULL,
    target TEXT NOT NULL,
    root TEXT NOT NULL REFERENCES objects(id),
    generation INTEGER NOT NULL CHECK (generation > 0),
    PRIMARY KEY (acceptor,target)
) STRICT;
CREATE TABLE events (
    sequence INTEGER PRIMARY KEY,
    acceptor TEXT NOT NULL,
    target TEXT NOT NULL,
    operation_id TEXT NOT NULL,
    request BLOB NOT NULL,
    receipt TEXT NOT NULL,
    UNIQUE (acceptor,operation_id)
) STRICT;
CREATE INDEX events_target ON events(acceptor,target,sequence);
CREATE TRIGGER objects_no_update BEFORE UPDATE ON objects BEGIN SELECT RAISE(ABORT,'immutable object'); END;
CREATE TRIGGER objects_no_delete BEFORE DELETE ON objects BEGIN SELECT RAISE(ABORT,'immutable object'); END;
CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append-only event'); END;
CREATE TRIGGER events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'append-only event'); END;
";
