//! Same-version, bounded exact-image export. Trusted Unix directory tree only.
use crate::{Error, Result};
use sha2::{Digest, Sha256};
#[cfg(unix)]
use std::os::unix::fs::OpenOptionsExt;
use std::{
    fs::{self, File, OpenOptions},
    io::{Read, Write},
    path::Path,
    sync::atomic::{AtomicU64, Ordering},
};

const MAGIC: &[u8; 8] = b"CTJEX001";
const MAX: usize = 1_048_576;
static STAGE: AtomicU64 = AtomicU64::new(0);
fn bad(message: &str) -> Error {
    Error::Invalid(message.into())
}

pub fn read(path: &Path) -> Result<Vec<u8>> {
    let mut bytes = Vec::new();
    File::open(path)?
        .take((MAX + 49) as u64)
        .read_to_end(&mut bytes)?;
    if bytes.len() < 48 || &bytes[..8] != MAGIC {
        return Err(bad("archive version/length"));
    }
    let length = u64::from_le_bytes(bytes[8..16].try_into().unwrap());
    if length > MAX as u64 || bytes.len() != 48 + length as usize {
        return Err(bad("archive length"));
    }
    let end = bytes.len() - 32;
    let digest = Sha256::new()
        .chain_update(b"continuum:export:v1\0")
        .chain_update(&bytes[..end])
        .finalize();
    if bytes[end..] != digest[..] {
        return Err(bad("archive checksum"));
    }
    Ok(bytes[16..end].to_vec())
}

pub fn publish(path: &Path, image: &[u8], fault: &str) -> Result<()> {
    if image.len() > MAX {
        return Err(bad("archive image limit"));
    }
    if ![
        "none",
        "export-before-link",
        "export-after-link",
        "export-after-sync",
    ]
    .contains(&fault)
    {
        return Err(bad("unknown export fault"));
    }
    let destination = std::path::absolute(path)?;
    let parent = destination
        .parent()
        .ok_or_else(|| bad("export parent required"))?;
    let parent_handle = File::open(parent)?;
    // Stage within the same parent so hard-link publication cannot cross devices.
    let (stage, mut file) = loop {
        let sequence = STAGE.fetch_add(1, Ordering::Relaxed);
        if sequence > 1024 {
            return Err(bad("stage attempts exhausted"));
        }
        let stage = parent.join(format!(
            ".continuum-export-{}-{sequence}",
            std::process::id()
        ));
        let mut options = OpenOptions::new();
        options.write(true).create_new(true);
        #[cfg(unix)]
        options.mode(0o600);
        match options.open(&stage) {
            Ok(file) => break (stage, file),
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => continue,
            Err(e) => return Err(e.into()),
        }
    };
    let mut bytes = MAGIC.to_vec();
    bytes.extend_from_slice(&(image.len() as u64).to_le_bytes());
    bytes.extend_from_slice(image);
    let digest = Sha256::new()
        .chain_update(b"continuum:export:v1\0")
        .chain_update(&bytes)
        .finalize();
    bytes.extend_from_slice(&digest);
    file.write_all(&bytes)?;
    file.sync_all()?;
    if fault == "export-before-link" {
        std::process::exit(83);
    }
    // Atomic no-overwrite creation. On uncertain error, preserve stage/evidence.
    fs::hard_link(&stage, &destination)?;
    if fault == "export-after-link" {
        std::process::exit(84);
    }
    fs::remove_file(&stage)?;
    parent_handle.sync_all()?;
    if fault == "export-after-sync" {
        std::process::exit(85);
    }
    Ok(())
}
