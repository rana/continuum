//! Disposable local journal: cooperative one-writer lock and explicit boundary.
//! No acceptance semantics or qualification for retained work.
use crate::{decode, encode};
use sha2::{Digest, Sha256};
use std::{
    fs::{self, File, OpenOptions},
    io::{self, Write},
    path::Path,
};

const LIMIT: u64 = 1_048_576;
const MAGIC: &[u8; 8] = b"CTJBD001";

fn invalid(message: &str) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, message)
}
fn boundary(image: &[u8]) -> Vec<u8> {
    let mut bytes = MAGIC.to_vec();
    bytes.extend_from_slice(&(image.len() as u64).to_le_bytes());
    bytes.extend_from_slice(&Sha256::digest(image));
    let checksum = Sha256::new()
        .chain_update(b"continuum:boundary:v1\0")
        .chain_update(&bytes)
        .finalize();
    bytes.extend_from_slice(&checksum);
    bytes
}

fn recover(path: &Path) -> io::Result<Vec<Vec<u8>>> {
    // No prefix is exposed on extra bytes, missing bytes or pending publication.
    if path.join("boundary.pending").try_exists()? {
        return Err(invalid("pending boundary: preserve and refuse"));
    }
    let marker = fs::read(path.join("boundary"))?;
    if marker.len() != 80 || &marker[..8] != MAGIC {
        return Err(invalid("invalid boundary"));
    }
    let length = u64::from_le_bytes(marker[8..16].try_into().unwrap());
    if length > LIMIT || fs::metadata(path.join("journal"))?.len() != length {
        return Err(invalid("boundary length mismatch: preserve and refuse"));
    }
    let image = fs::read(path.join("journal"))?;
    if marker != boundary(&image) {
        return Err(invalid("boundary digest mismatch"));
    }
    decode(&image).map_err(|_| invalid("invalid committed framing"))
}

pub struct Journal {
    // Lock lifetime covers all recovery and mutation, including failed sync.
    _lock: File,
    directory: std::path::PathBuf,
    records: Vec<Vec<u8>>,
    poisoned: bool,
}

impl Journal {
    pub fn init(path: &Path) -> io::Result<()> {
        fs::create_dir(path)?;
        let lock = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .open(path.join("lock"))?;
        lock.try_lock().map_err(io::Error::other)?;
        let journal = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(path.join("journal"))?;
        journal.sync_all()?;
        let mut marker = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(path.join("boundary"))?;
        marker.write_all(&boundary(&[]))?;
        marker.sync_all()?;
        File::open(path)?.sync_all()?;
        File::open(path.parent().ok_or_else(|| invalid("parent required"))?)?.sync_all()
    }

    pub fn open(path: &Path) -> io::Result<Self> {
        let lock = OpenOptions::new()
            .read(true)
            .write(true)
            .open(path.join("lock"))?;
        lock.try_lock().map_err(io::Error::other)?;
        let records = recover(path)?;
        Ok(Self {
            _lock: lock,
            directory: path.into(),
            records,
            poisoned: false,
        })
    }

    pub fn records(&self) -> io::Result<&[Vec<u8>]> {
        if self.poisoned {
            return Err(invalid("uncertain write: handle poisoned"));
        }
        Ok(&self.records)
    }

    /// Fault labels are an explicit laboratory interface, not production recovery.
    pub fn append(&mut self, payload: Vec<u8>, fault: &str) -> io::Result<()> {
        if self.poisoned {
            return Err(invalid("uncertain write: handle poisoned"));
        }
        if ![
            "none",
            "after-data",
            "pending",
            "after-commit",
            "after-rename",
            "sync-error",
        ]
        .contains(&fault)
        {
            return Err(invalid("unknown fault"));
        }
        let old_length = encode(&self.records)
            .map_err(|_| invalid("invalid memory framing"))?
            .len();
        let mut next = self.records.clone();
        next.push(payload);
        let image = encode(&next).map_err(|_| invalid("payload too large"))?;
        if image.len() as u64 > LIMIT {
            return Err(invalid("journal limit"));
        }
        // Every I/O failure from here requires abandoning this handle. No reread
        // can convert uncertain synchronization into a successful acknowledgement.
        self.poisoned = true;
        let mut file = OpenOptions::new()
            .append(true)
            .open(self.directory.join("journal"))?;
        file.write_all(&image[old_length..])?;
        if fault == "sync-error" {
            return Err(io::Error::other("injected unknown sync outcome"));
        }
        file.sync_all()?;
        if fault == "after-data" {
            std::process::exit(74);
        }
        let temporary = self.directory.join("boundary.pending");
        let mut marker = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&temporary)?;
        marker.write_all(&boundary(&image))?;
        marker.sync_all()?;
        if fault == "pending" {
            std::process::exit(75);
        }
        fs::rename(&temporary, self.directory.join("boundary"))?;
        if fault == "after-rename" {
            std::process::exit(77);
        }
        File::open(&self.directory)?.sync_all()?;
        if fault == "after-commit" {
            std::process::exit(76);
        }
        self.records = next;
        self.poisoned = false;
        Ok(())
    }
}
