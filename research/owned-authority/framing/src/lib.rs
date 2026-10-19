//! Disposable framing primitive, not an acceptance engine.
pub mod journal;

use sha2::{Digest, Sha256};
use std::io::{self, Write};

const MAGIC: &[u8; 8] = b"CTJFR001";
const DOMAIN: &[u8] = b"continuum:journal-frame:v1\0";
pub const MAX_PAYLOAD: usize = 65_536;

#[derive(Debug, PartialEq, Eq)]
pub enum Invalid {
    Truncated,
    Version,
    Length,
    Sequence,
    Chain,
    Digest,
}

/// Exact finite image decoder: no accepted prefix is returned on any bad tail.
/// A complete frame is a syntactic boundary, never evidence of completed sync.
pub fn decode(mut image: &[u8]) -> Result<Vec<Vec<u8>>, Invalid> {
    let mut records = Vec::new();
    let mut previous = [0u8; 32];
    while !image.is_empty() {
        if image.len() < 52 {
            return Err(Invalid::Truncated);
        }
        if &image[..8] != MAGIC {
            return Err(Invalid::Version);
        }
        let n = u32::from_le_bytes(image[8..12].try_into().unwrap()) as usize;
        if n > MAX_PAYLOAD {
            return Err(Invalid::Length);
        }
        if u64::from_le_bytes(image[12..20].try_into().unwrap()) != records.len() as u64 {
            return Err(Invalid::Sequence);
        }
        if image[20..52] != previous {
            return Err(Invalid::Chain);
        }
        let end = 52 + n;
        if image.len() < end + 32 {
            return Err(Invalid::Truncated);
        }
        let digest: [u8; 32] = Sha256::new()
            .chain_update(DOMAIN)
            .chain_update(&image[..end])
            .finalize()
            .into();
        if image[end..end + 32] != digest {
            return Err(Invalid::Digest);
        }
        records.push(image[52..end].to_vec());
        previous = digest;
        image = &image[end + 32..];
    }
    Ok(records)
}

/// Build a disposable complete image. Sequence here is frame ordinal, NOT the
/// domain's global acceptance sequence. No operation semantics are interpreted.
pub fn encode(records: &[Vec<u8>]) -> Result<Vec<u8>, Invalid> {
    let mut image = Vec::new();
    let mut previous = [0u8; 32];
    for (ordinal, payload) in records.iter().enumerate() {
        if payload.len() > MAX_PAYLOAD {
            return Err(Invalid::Length);
        }
        let start = image.len();
        image.extend_from_slice(MAGIC);
        image.extend_from_slice(&(payload.len() as u32).to_le_bytes());
        image.extend_from_slice(&(ordinal as u64).to_le_bytes());
        image.extend_from_slice(&previous);
        image.extend_from_slice(payload);
        previous = Sha256::new()
            .chain_update(DOMAIN)
            .chain_update(&image[start..])
            .finalize()
            .into();
        image.extend_from_slice(&previous);
    }
    Ok(image)
}

/// Exclusive fresh-file creation only; never open an existing image for writes.
/// On ANY error preserve the path, return the error and do not retry it. Parent
/// directory durability and a production ownership protocol are not provided.
pub fn create(path: &std::path::Path, records: &[Vec<u8>]) -> io::Result<()> {
    let image = encode(records)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidInput, format!("{e:?}")))?;
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)?;
    file.write_all(&image)?;
    file.sync_all()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn frame_boundary_is_not_acknowledgement_history() {
        let records = vec![
            b"source".to_vec(),
            b"failed approach".to_vec(),
            b"proposal".to_vec(),
        ];
        let image = encode(&records).unwrap();
        assert_eq!(decode(&image), Ok(records.clone()));
        let mut boundary = 0;
        for (i, record) in records.iter().enumerate() {
            boundary += 84 + record.len();
            assert_eq!(decode(&image[..boundary]), Ok(records[..=i].to_vec()));
        }
        // Losing an entire final frame is undetectable without an external
        // committed-boundary protocol. Explicitly demonstrate this limitation.
        assert_eq!(decode(&[]), Ok(vec![]));
    }
    #[test]
    fn every_nonboundary_cut_and_every_single_byte_flip_refuses() {
        let image = encode(&[b"a".to_vec(), b"bc".to_vec()]).unwrap();
        for cut in 1..image.len() {
            if cut != 85 {
                assert!(decode(&image[..cut]).is_err(), "cut {cut}");
            }
        }
        for i in 0..image.len() {
            let mut bad = image.clone();
            bad[i] ^= 1;
            assert!(decode(&bad).is_err(), "byte {i}");
        }
    }
    #[test]
    fn bounded_length_and_reordered_records_refuse() {
        assert_eq!(encode(&[vec![0; MAX_PAYLOAD + 1]]), Err(Invalid::Length));
        let image = encode(&[b"a".to_vec(), b"b".to_vec()]).unwrap();
        assert!(decode(&[&image[85..], &image[..85]].concat()).is_err());
        let max = vec![vec![7; MAX_PAYLOAD]];
        assert_eq!(decode(&encode(&max).unwrap()), Ok(max));
    }
}

// Compile-time reuse of the project's original canonical codec only. The
// laboratory does not link continuum-core, rusqlite or any SQLite store code.
#[path = "../../../../src/object.rs"]
mod object;
pub use object::{EvidenceOutcome, Object, ObjectId, SnapshotEntry};
pub mod store;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("invalid input: {0}")]
    Invalid(String),
    #[error("operation ID was already used for a different request")]
    OperationConflict,
    #[error("filesystem: {0}")]
    Io(#[from] std::io::Error),
    #[error("record encoding: {0}")]
    Json(#[from] serde_json::Error),
}
pub type Result<T, E = Error> = std::result::Result<T, E>;
