//! Experimental, single-node repository primitives.
//!
//! Content identity and conditional publication are implemented here. Acceptor
//! names are namespaces, not authenticated identities. Recorded evidence is a
//! caller's declaration, not a trusted verification result.

mod object;
mod store;

pub use object::{
    EvidenceOutcome, FORMAT_VERSION, MAX_OBJECT_BYTES, Object, ObjectId, SnapshotEntry,
};
pub use store::{AcceptRequest, Acceptance, Head, Outcome, Receipt, Store};

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("invalid input: {0}")]
    Invalid(String),
    #[error("object not found: {0}")]
    NotFound(ObjectId),
    #[error("object {id} must be {expected}")]
    WrongKind {
        id: ObjectId,
        expected: &'static str,
    },
    #[error("object integrity check failed: {0}")]
    Integrity(ObjectId),
    #[error("operation ID was already used for a different request")]
    OperationConflict,
    #[error("unsupported database: {0}")]
    UnsupportedDatabase(String),
    #[error("database error: {0}")]
    Database(#[from] rusqlite::Error),
    #[error("record encoding error: {0}")]
    Json(#[from] serde_json::Error),
}

pub type Result<T> = std::result::Result<T, Error>;
