use crate::{Error, Result};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{fmt, str::FromStr};

pub const FORMAT_VERSION: u16 = 1;
pub const MAX_OBJECT_BYTES: usize = 16 * 1024 * 1024;
const MAGIC: &[u8] = b"continuum.object\0";
const MAX_ENTRIES: usize = 4096;
const MAX_PATH_BYTES: usize = 4096;

/// SHA-256 of the full domain-separated canonical envelope.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub struct ObjectId([u8; 32]);

impl ObjectId {
    pub(crate) fn of(bytes: &[u8]) -> Self {
        Self(Sha256::digest(bytes).into())
    }

    pub(crate) fn bytes(self) -> [u8; 32] {
        self.0
    }
}

impl fmt::Display for ObjectId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("sha256:")?;
        for byte in self.0 {
            write!(f, "{byte:02x}")?;
        }
        Ok(())
    }
}

impl FromStr for ObjectId {
    type Err = Error;

    fn from_str(value: &str) -> Result<Self> {
        let hex = value
            .strip_prefix("sha256:")
            .filter(|s| {
                s.len() == 64
                    && s.bytes()
                        .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            })
            .ok_or_else(|| {
                Error::Invalid("expected sha256: followed by 64 lowercase hex digits".into())
            })?;
        let mut bytes = [0; 32];
        for (i, byte) in bytes.iter_mut().enumerate() {
            *byte = u8::from_str_radix(&hex[2 * i..2 * i + 2], 16)
                .map_err(|_| Error::Invalid("invalid object ID".into()))?;
        }
        Ok(Self(bytes))
    }
}

impl TryFrom<String> for ObjectId {
    type Error = Error;
    fn try_from(value: String) -> Result<Self> {
        value.parse()
    }
}

impl From<ObjectId> for String {
    fn from(value: ObjectId) -> Self {
        value.to_string()
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SnapshotEntry {
    pub path: String,
    pub blob: ObjectId,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum EvidenceOutcome {
    Unknown,
    Pass,
    Fail,
}

/// JSON is an input/output projection. It does not define object identity.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case", deny_unknown_fields)]
pub enum Object {
    Blob {
        bytes: Vec<u8>,
    },
    Snapshot {
        entries: Vec<SnapshotEntry>,
    },
    /// Untrusted declared evidence, tied to one exact snapshot.
    EvidenceRecord {
        candidate: ObjectId,
        outcome: EvidenceOutcome,
        provenance: String,
        output: Option<ObjectId>,
    },
}

impl Object {
    pub fn kind(&self) -> &'static str {
        match self {
            Self::Blob { .. } => "blob",
            Self::Snapshot { .. } => "snapshot",
            Self::EvidenceRecord { .. } => "evidence_record",
        }
    }

    pub fn id(&self) -> Result<ObjectId> {
        Ok(ObjectId::of(&self.canonical_bytes()?))
    }

    /// V1: magic, u16 BE version, u8 kind, then fixed-order typed fields.
    /// Variable byte strings and entry counts have u32 BE lengths. IDs are
    /// raw 32-byte SHA-256 values. Snapshot entries sort by UTF-8 path bytes.
    pub fn canonical_bytes(&self) -> Result<Vec<u8>> {
        let mut out = MAGIC.to_vec();
        out.extend(FORMAT_VERSION.to_be_bytes());
        match self {
            Self::Blob { bytes } => {
                out.push(1);
                append_bytes(&mut out, bytes)?;
            }
            Self::Snapshot { entries } => {
                if entries.len() > MAX_ENTRIES {
                    return Err(Error::Invalid("too many snapshot entries".into()));
                }
                let mut ordered: Vec<_> = entries.iter().collect();
                ordered.sort_by(|a, b| a.path.as_bytes().cmp(b.path.as_bytes()));
                for (i, entry) in ordered.iter().enumerate() {
                    validate_path(&entry.path)?;
                    if i > 0 && ordered[i - 1].path == entry.path {
                        return Err(Error::Invalid("duplicate snapshot path".into()));
                    }
                    for (offset, _) in entry.path.match_indices('/') {
                        let prefix = &entry.path[..offset];
                        if ordered
                            .binary_search_by(|e| e.path.as_str().cmp(prefix))
                            .is_ok()
                        {
                            return Err(Error::Invalid(
                                "a snapshot path is both a file and a directory".into(),
                            ));
                        }
                    }
                }
                out.push(2);
                out.extend((ordered.len() as u32).to_be_bytes());
                for entry in ordered {
                    append_bytes(&mut out, entry.path.as_bytes())?;
                    out.extend(entry.blob.bytes());
                }
            }
            Self::EvidenceRecord {
                candidate,
                outcome,
                provenance,
                output,
            } => {
                out.push(3);
                out.extend(candidate.bytes());
                out.push(match outcome {
                    EvidenceOutcome::Unknown => 0,
                    EvidenceOutcome::Pass => 1,
                    EvidenceOutcome::Fail => 2,
                });
                append_bytes(&mut out, provenance.as_bytes())?;
                match output {
                    None => out.push(0),
                    Some(id) => {
                        out.push(1);
                        out.extend(id.bytes());
                    }
                }
            }
        }
        if out.len() > MAX_OBJECT_BYTES {
            return Err(Error::Invalid(
                "object exceeds the 16 MiB envelope limit".into(),
            ));
        }
        Ok(out)
    }

    pub fn from_canonical(bytes: &[u8]) -> Result<Self> {
        if bytes.len() > MAX_OBJECT_BYTES {
            return Err(Error::Invalid(
                "object exceeds the 16 MiB envelope limit".into(),
            ));
        }
        let mut r = Reader { bytes, offset: 0 };
        if r.take(MAGIC.len())? != MAGIC {
            return Err(Error::Invalid("wrong object domain".into()));
        }
        if r.take(2)? != FORMAT_VERSION.to_be_bytes() {
            return Err(Error::Invalid("unsupported object format version".into()));
        }
        let object = match r.byte()? {
            1 => Self::Blob {
                bytes: r.variable()?.to_vec(),
            },
            2 => {
                let count = r.u32()? as usize;
                if count > MAX_ENTRIES {
                    return Err(Error::Invalid("too many snapshot entries".into()));
                }
                let mut entries = Vec::with_capacity(count);
                for _ in 0..count {
                    entries.push(SnapshotEntry {
                        path: r.string()?,
                        blob: r.id()?,
                    });
                }
                Self::Snapshot { entries }
            }
            3 => {
                let candidate = r.id()?;
                let outcome = match r.byte()? {
                    0 => EvidenceOutcome::Unknown,
                    1 => EvidenceOutcome::Pass,
                    2 => EvidenceOutcome::Fail,
                    _ => return Err(Error::Invalid("unknown evidence outcome".into())),
                };
                let provenance = r.string()?;
                let output = match r.byte()? {
                    0 => None,
                    1 => Some(r.id()?),
                    _ => return Err(Error::Invalid("invalid optional object ID".into())),
                };
                Self::EvidenceRecord {
                    candidate,
                    outcome,
                    provenance,
                    output,
                }
            }
            _ => return Err(Error::Invalid("unknown object kind".into())),
        };
        if r.offset != bytes.len() || object.canonical_bytes()? != bytes {
            return Err(Error::Invalid("noncanonical object encoding".into()));
        }
        Ok(object)
    }
}

pub(crate) fn append_bytes(out: &mut Vec<u8>, bytes: &[u8]) -> Result<()> {
    if bytes.len() > MAX_OBJECT_BYTES || out.len() + 4 + bytes.len() > MAX_OBJECT_BYTES {
        return Err(Error::Invalid(
            "encoded value exceeds the 16 MiB limit".into(),
        ));
    }
    out.extend((bytes.len() as u32).to_be_bytes());
    out.extend(bytes);
    Ok(())
}

fn validate_path(path: &str) -> Result<()> {
    if path.is_empty()
        || path.len() > MAX_PATH_BYTES
        || path.contains(['\\', '\0'])
        || path
            .split('/')
            .any(|part| part.is_empty() || part == "." || part == "..")
    {
        return Err(Error::Invalid(
            "snapshot paths must be normalized relative UTF-8 paths".into(),
        ));
    }
    Ok(())
}

struct Reader<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> Reader<'a> {
    fn take(&mut self, len: usize) -> Result<&'a [u8]> {
        let end = self
            .offset
            .checked_add(len)
            .ok_or_else(|| Error::Invalid("object length overflow".into()))?;
        let bytes = self
            .bytes
            .get(self.offset..end)
            .ok_or_else(|| Error::Invalid("truncated object".into()))?;
        self.offset = end;
        Ok(bytes)
    }

    fn byte(&mut self) -> Result<u8> {
        Ok(self.take(1)?[0])
    }
    fn u32(&mut self) -> Result<u32> {
        let mut bytes = [0; 4];
        bytes.copy_from_slice(self.take(4)?);
        Ok(u32::from_be_bytes(bytes))
    }
    fn variable(&mut self) -> Result<&'a [u8]> {
        let len = self.u32()? as usize;
        self.take(len)
    }
    fn string(&mut self) -> Result<String> {
        String::from_utf8(self.variable()?.to_vec())
            .map_err(|_| Error::Invalid("invalid UTF-8 string".into()))
    }
    fn id(&mut self) -> Result<ObjectId> {
        let mut bytes = [0; 32];
        bytes.copy_from_slice(self.take(32)?);
        Ok(ObjectId(bytes))
    }
}
