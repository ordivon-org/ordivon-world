use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::model::{EgressEvidence, Mutation, WORLD_SCHEMA_VERSION};

const GENESIS_HASH: &str = "genesis";
const EVENT_HASH_DOMAIN: &[u8] = b"ordivon-link/network-world-event/v1\0";
const MAX_EVENT_BYTES: u64 = 16 * 1024;
const MAX_EVENTS: usize = 10_000;
static TEMP_SEQUENCE: AtomicU64 = AtomicU64::new(0);

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct WorldEvent {
    pub schema_version: u32,
    pub world_id: String,
    pub sequence: u64,
    pub runtime_revision: u64,
    pub previous_hash: String,
    pub kind: EventKind,
    pub event_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum EventKind {
    Created {
        manifest_revision: String,
    },
    Mutated {
        mutation: Mutation,
    },
    Frozen,
    Reset,
    EgressObserved {
        evidence: EgressEvidence,
    },
    ServiceConnectionObserved {
        service_id: String,
        observed_at_revision: u64,
    },
    Destroyed,
}

#[derive(Debug, Clone)]
pub struct ObserverLog {
    root: PathBuf,
}

#[derive(Debug, Error)]
pub enum ObserverError {
    #[error("observer I/O failed: {0}")]
    Io(#[from] std::io::Error),
    #[error("observer event is not valid JSON: {0}")]
    Json(#[from] serde_json::Error),
    #[error("observer event file must contain between 1 and {MAX_EVENT_BYTES} bytes")]
    InvalidEventSize,
    #[error("observer event limit of {MAX_EVENTS} exceeded")]
    TooManyEvents,
    #[error("observer event schema version {0} is unsupported")]
    UnsupportedSchema(u32),
    #[error("observer event world id mismatch")]
    WorldMismatch,
    #[error("observer sequence is broken at event {0}")]
    BrokenSequence(u64),
    #[error("observer hash chain is broken at event {0}")]
    BrokenChain(u64),
    #[error("observer event hash is invalid at event {0}")]
    InvalidHash(u64),
    #[error("observer directory contains unexpected entry `{0}`")]
    UnexpectedEntry(String),
    #[error("observer path is not an owned regular directory")]
    UnsafePath,
    #[error("observer head changed concurrently")]
    Conflict,
}

#[derive(Serialize)]
struct EventMaterial<'a> {
    schema_version: u32,
    world_id: &'a str,
    sequence: u64,
    runtime_revision: u64,
    previous_hash: &'a str,
    kind: &'a EventKind,
}

impl ObserverLog {
    pub fn new(root: impl Into<PathBuf>) -> Self {
        Self { root: root.into() }
    }

    pub fn events_directory(&self, world_id: &str) -> Result<PathBuf, ObserverError> {
        validate_world_id(world_id)?;
        Ok(self.root.join(world_id).join("events"))
    }

    pub fn read_verified(&self, world_id: &str) -> Result<Vec<WorldEvent>, ObserverError> {
        let events_directory = self.events_directory(world_id)?;
        if !events_directory.exists() {
            return Err(std::io::Error::from(std::io::ErrorKind::NotFound).into());
        }
        let lock = self.open_lock(world_id)?;
        File::lock_shared(&lock)?;
        read_event_files(&events_directory, world_id)
    }

    pub(crate) fn read_verified_or_empty(
        &self,
        world_id: &str,
    ) -> Result<Vec<WorldEvent>, ObserverError> {
        let events_directory = self.events_directory(world_id)?;
        if !events_directory.exists() {
            return Ok(Vec::new());
        }
        self.read_verified(world_id)
    }

    pub(crate) fn append_checked(
        &self,
        world_id: &str,
        expected_head: Option<&str>,
        runtime_revision: u64,
        kind: EventKind,
    ) -> Result<WorldEvent, ObserverError> {
        let lock = self.open_lock(world_id)?;
        File::lock(&lock)?;
        let events_directory = self.events_directory(world_id)?;
        let events = read_event_files(&events_directory, world_id)?;
        if events.len() >= MAX_EVENTS {
            return Err(ObserverError::TooManyEvents);
        }
        let actual_head = events.last().map(|event| event.event_hash.as_str());
        if actual_head != expected_head {
            return Err(ObserverError::Conflict);
        }

        let sequence = events.len() as u64;
        let previous_hash = actual_head.unwrap_or(GENESIS_HASH).to_owned();
        let mut event = WorldEvent {
            schema_version: WORLD_SCHEMA_VERSION,
            world_id: world_id.to_owned(),
            sequence,
            runtime_revision,
            previous_hash,
            kind,
            event_hash: String::new(),
        };
        event.event_hash = event_hash(&event);
        persist_event(&events_directory, &event)?;
        Ok(event)
    }

    fn open_lock(&self, world_id: &str) -> Result<File, ObserverError> {
        validate_world_id(world_id)?;
        ensure_directory(&self.root, 0o700)?;
        let world_directory = self.root.join(world_id);
        ensure_directory(&world_directory, 0o700)?;
        let events_directory = world_directory.join("events");
        ensure_directory(&events_directory, 0o700)?;

        let mut options = OpenOptions::new();
        options.create(true).read(true).write(true);
        #[cfg(unix)]
        {
            use std::os::unix::fs::OpenOptionsExt;
            options.mode(0o600);
        }
        let lock_path = world_directory.join("observer.lock");
        if let Ok(metadata) = fs::symlink_metadata(&lock_path)
            && !metadata.file_type().is_file()
        {
            return Err(ObserverError::UnsafePath);
        }
        Ok(options.open(lock_path)?)
    }
}

fn read_event_files(directory: &Path, world_id: &str) -> Result<Vec<WorldEvent>, ObserverError> {
    ensure_existing_directory(directory)?;
    let mut entries = Vec::new();
    for entry in fs::read_dir(directory)? {
        let entry = entry?;
        let file_type = entry.file_type()?;
        let name = entry
            .file_name()
            .into_string()
            .map_err(|_| ObserverError::UnexpectedEntry("non-utf8".to_owned()))?;
        if !file_type.is_file() {
            return Err(ObserverError::UnexpectedEntry(name));
        }
        entries.push((name, entry.path()));
    }
    entries.sort_by(|left, right| left.0.cmp(&right.0));
    if entries.len() > MAX_EVENTS {
        return Err(ObserverError::TooManyEvents);
    }

    let mut events = Vec::with_capacity(entries.len());
    let mut previous = GENESIS_HASH.to_owned();
    for (index, (name, path)) in entries.into_iter().enumerate() {
        let expected_name = event_file_name(index as u64);
        if name != expected_name {
            return Err(ObserverError::UnexpectedEntry(name));
        }
        let metadata = fs::symlink_metadata(&path)?;
        if !metadata.file_type().is_file()
            || metadata.len() == 0
            || metadata.len() > MAX_EVENT_BYTES
        {
            return Err(ObserverError::InvalidEventSize);
        }
        let encoded = fs::read(path)?;
        if encoded.len() as u64 != metadata.len() {
            return Err(ObserverError::InvalidEventSize);
        }
        let event: WorldEvent = serde_json::from_slice(&encoded)?;
        let expected_sequence = events.len() as u64;
        if event.schema_version != WORLD_SCHEMA_VERSION {
            return Err(ObserverError::UnsupportedSchema(event.schema_version));
        }
        if event.world_id != world_id {
            return Err(ObserverError::WorldMismatch);
        }
        if event.sequence != expected_sequence {
            return Err(ObserverError::BrokenSequence(event.sequence));
        }
        if event.previous_hash != previous {
            return Err(ObserverError::BrokenChain(event.sequence));
        }
        if event.event_hash != event_hash(&event) {
            return Err(ObserverError::InvalidHash(event.sequence));
        }
        previous.clone_from(&event.event_hash);
        events.push(event);
    }
    Ok(events)
}

fn persist_event(directory: &Path, event: &WorldEvent) -> Result<(), ObserverError> {
    let encoded = serde_json::to_vec(event)?;
    if encoded.is_empty() || encoded.len() as u64 > MAX_EVENT_BYTES {
        return Err(ObserverError::InvalidEventSize);
    }
    let temporary = directory
        .parent()
        .ok_or(ObserverError::UnsafePath)?
        .join(format!(
            ".pending-{}-{}",
            std::process::id(),
            TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed)
        ));
    let final_path = directory.join(event_file_name(event.sequence));
    if fs::symlink_metadata(&final_path).is_ok() {
        return Err(ObserverError::UnexpectedEntry(
            final_path
                .file_name()
                .and_then(|name| name.to_str())
                .unwrap_or("non-utf8")
                .to_owned(),
        ));
    }

    let result = (|| {
        let mut options = OpenOptions::new();
        options.create_new(true).write(true);
        #[cfg(unix)]
        {
            use std::os::unix::fs::OpenOptionsExt;
            options.mode(0o600);
        }
        let mut file = options.open(&temporary)?;
        file.write_all(&encoded)?;
        file.sync_all()?;
        set_file_read_only(&temporary)?;
        fs::rename(&temporary, &final_path)?;
        sync_directory(directory)?;
        Ok::<(), ObserverError>(())
    })();
    if result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    result
}

fn event_file_name(sequence: u64) -> String {
    format!("{sequence:020}.json")
}

fn event_hash(event: &WorldEvent) -> String {
    let material = EventMaterial {
        schema_version: event.schema_version,
        world_id: &event.world_id,
        sequence: event.sequence,
        runtime_revision: event.runtime_revision,
        previous_hash: &event.previous_hash,
        kind: &event.kind,
    };
    let encoded = serde_json::to_vec(&material).expect("event material is serializable");
    let mut hasher = Sha256::new();
    hasher.update(EVENT_HASH_DOMAIN);
    hasher.update(encoded);
    let digest: String = hasher
        .finalize()
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    format!("sha256:{digest}")
}

fn validate_world_id(world_id: &str) -> Result<(), ObserverError> {
    let digest = world_id
        .strip_prefix("nw1-")
        .ok_or(ObserverError::UnsafePath)?;
    if digest.len() != 64
        || !digest
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(ObserverError::UnsafePath);
    }
    Ok(())
}

fn ensure_directory(path: &Path, unix_mode: u32) -> Result<(), ObserverError> {
    match fs::symlink_metadata(path) {
        Ok(metadata) if metadata.file_type().is_dir() => {
            validate_private_directory_permissions(&metadata)?;
        }
        Ok(_) => return Err(ObserverError::UnsafePath),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            match create_directory(path, unix_mode) {
                Ok(()) => {
                    if let Some(parent) = path.parent() {
                        sync_directory(parent)?;
                    }
                }
                Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => {
                    let metadata = fs::symlink_metadata(path)?;
                    if !metadata.file_type().is_dir() {
                        return Err(ObserverError::UnsafePath);
                    }
                    validate_private_directory_permissions(&metadata)?;
                }
                Err(error) => return Err(error.into()),
            }
        }
        Err(error) => return Err(error.into()),
    }
    Ok(())
}

fn ensure_existing_directory(path: &Path) -> Result<(), ObserverError> {
    let metadata = fs::symlink_metadata(path)?;
    if !metadata.file_type().is_dir() {
        return Err(ObserverError::UnsafePath);
    }
    Ok(())
}

fn sync_directory(path: &Path) -> Result<(), std::io::Error> {
    File::open(path)?.sync_all()
}

#[cfg(unix)]
fn create_directory(path: &Path, mode: u32) -> Result<(), std::io::Error> {
    use std::os::unix::fs::DirBuilderExt;
    let mut builder = fs::DirBuilder::new();
    builder.mode(mode).create(path)
}

#[cfg(not(unix))]
fn create_directory(path: &Path, _mode: u32) -> Result<(), std::io::Error> {
    fs::create_dir(path)
}

#[cfg(unix)]
fn validate_private_directory_permissions(metadata: &fs::Metadata) -> Result<(), ObserverError> {
    use std::os::unix::fs::PermissionsExt;
    if metadata.permissions().mode() & 0o077 != 0 {
        return Err(ObserverError::UnsafePath);
    }
    Ok(())
}

#[cfg(not(unix))]
fn validate_private_directory_permissions(_metadata: &fs::Metadata) -> Result<(), ObserverError> {
    Ok(())
}

#[cfg(unix)]
fn set_file_read_only(path: &Path) -> Result<(), std::io::Error> {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(0o400))
}

#[cfg(not(unix))]
fn set_file_read_only(path: &Path) -> Result<(), std::io::Error> {
    let mut permissions = fs::metadata(path)?.permissions();
    permissions.set_readonly(true);
    fs::set_permissions(path, permissions)
}
