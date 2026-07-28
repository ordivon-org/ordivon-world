use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::{Component, Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

use anyhow::{Context, Result, anyhow, bail};
use serde::{Deserialize, Serialize};

use crate::model::{
    ActorView, EgressEvidence, EgressResult, Mutation, NetworkWorldManifest, WORLD_SCHEMA_VERSION,
    WorldPhase, WorldState,
};
use crate::observer::{EventKind, ObserverError, ObserverLog, WorldEvent};

const MANIFEST_FILE: &str = "manifest.json";
const ACTOR_PROJECTION_FILE: &str = "projection.json";
const MAX_MANIFEST_BYTES: u64 = 1024 * 1024;
const MAX_ACTOR_VIEW_BYTES: u64 = 4 * 1024 * 1024;
const MAX_CONFLICT_RETRIES: usize = 16;
static TEMP_SEQUENCE: AtomicU64 = AtomicU64::new(0);

#[derive(Debug, Clone)]
pub struct Controller {
    authority_root: PathBuf,
    observer: ObserverLog,
    actor_root: PathBuf,
}

#[derive(Debug, Clone)]
pub struct ActorSurface {
    actor_root: PathBuf,
    world_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct WorldInspection {
    pub schema_version: u32,
    pub manifest: NetworkWorldManifest,
    pub state: WorldState,
    pub observer_event_count: usize,
    pub observer_head_hash: String,
    pub actor_projection_current: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(tag = "status", rename_all = "snake_case", deny_unknown_fields)]
enum ActorProjection {
    Active {
        schema_version: u32,
        world_id: String,
        runtime_revision: u64,
        view: ActorView,
    },
    Destroyed {
        schema_version: u32,
        world_id: String,
        runtime_revision: u64,
    },
}

enum Replay {
    Active(WorldState),
    Destroyed(WorldEvent),
}

impl Controller {
    pub fn new(
        authority_root: impl Into<PathBuf>,
        observer_root: impl Into<PathBuf>,
        actor_root: impl Into<PathBuf>,
    ) -> Result<Self> {
        let authority_root = resolve_root_path(authority_root.into())?;
        let observer_root = resolve_root_path(observer_root.into())?;
        let actor_root = resolve_root_path(actor_root.into())?;
        validate_existing_root_permissions(&authority_root, true)?;
        validate_existing_root_permissions(&observer_root, true)?;
        validate_existing_root_permissions(&actor_root, false)?;
        let roots = [&authority_root, &observer_root, &actor_root];
        for (index, root) in roots.iter().enumerate() {
            for other in roots.iter().skip(index + 1) {
                if root == other || root.starts_with(other) || other.starts_with(root) {
                    bail!("authority, observer, and actor roots must be independent paths");
                }
            }
        }
        Ok(Self {
            authority_root,
            observer: ObserverLog::new(observer_root),
            actor_root,
        })
    }

    pub fn load_manifest(path: &Path) -> Result<NetworkWorldManifest> {
        let metadata = fs::metadata(path)
            .with_context(|| format!("failed to inspect manifest {}", path.display()))?;
        if !metadata.is_file() || metadata.len() == 0 || metadata.len() > MAX_MANIFEST_BYTES {
            bail!("manifest must be a regular file no larger than {MAX_MANIFEST_BYTES} bytes");
        }
        let input = fs::read_to_string(path)
            .with_context(|| format!("failed to read manifest {}", path.display()))?;
        let manifest = if path
            .extension()
            .is_some_and(|extension| extension == "json")
        {
            serde_json::from_str(&input)
                .with_context(|| format!("invalid JSON manifest {}", path.display()))?
        } else {
            toml::from_str(&input)
                .with_context(|| format!("invalid TOML manifest {}", path.display()))?
        };
        Ok(manifest)
    }

    pub fn validate_manifest(manifest: &NetworkWorldManifest) -> Result<()> {
        manifest.validate().map_err(Into::into)
    }

    pub fn create(&self, manifest: &NetworkWorldManifest) -> Result<WorldInspection> {
        manifest.validate()?;
        let normalized = manifest.normalized();
        let world_id = normalized.world_id();

        for _ in 0..MAX_CONFLICT_RETRIES {
            let events = self.observer.read_verified_or_empty(&world_id)?;
            if !events.is_empty() {
                match replay(&normalized, &events)? {
                    Replay::Active(_) => {
                        self.persist_manifest_idempotently(&normalized)?;
                        return self.inspect(&world_id);
                    }
                    Replay::Destroyed(_) => {
                        bail!("observer history exists; a destroyed world id cannot be recreated");
                    }
                }
            } else {
                self.persist_manifest_idempotently(&normalized)?;
                match self.observer.append_checked(
                    &world_id,
                    None,
                    0,
                    EventKind::Created {
                        manifest_revision: normalized.manifest_revision(),
                    },
                ) {
                    Ok(_) => return self.inspect(&world_id),
                    Err(ObserverError::Conflict) => continue,
                    Err(error) => return Err(error.into()),
                }
            }
        }
        bail!("world creation lost repeated concurrent observer races")
    }

    pub fn inspect(&self, world_id: &str) -> Result<WorldInspection> {
        let manifest = self.read_persisted_manifest(world_id)?;
        let events = self.observer.read_verified(world_id)?;
        let state = match replay(&manifest, &events)? {
            Replay::Active(state) => state,
            Replay::Destroyed(_) => bail!("world `{world_id}` is destroyed"),
        };
        let actor_projection_current = self.sync_actor_view(&state).is_ok();
        let head = events
            .last()
            .ok_or_else(|| anyhow!("observer log has no creation event"))?;
        Ok(WorldInspection {
            schema_version: WORLD_SCHEMA_VERSION,
            manifest,
            state,
            observer_event_count: events.len(),
            observer_head_hash: head.event_hash.clone(),
            actor_projection_current,
        })
    }

    pub fn actor_surface(&self, world_id: &str) -> Result<ActorSurface> {
        ActorSurface::open(self.actor_root.clone(), world_id.to_owned())
    }

    pub fn events(&self, world_id: &str) -> Result<Vec<WorldEvent>> {
        validate_world_id(world_id)?;
        Ok(self.observer.read_verified(world_id)?)
    }

    pub fn mutate(&self, world_id: &str, mutation: Mutation) -> Result<WorldState> {
        for _ in 0..MAX_CONFLICT_RETRIES {
            let (_, mut state, head) = self.load_active(world_id)?;
            if state.phase == WorldPhase::Frozen {
                bail!("world `{world_id}` is frozen");
            }
            if !state
                .mutation_changes(&mutation)
                .map_err(anyhow::Error::msg)?
            {
                let _ = self.sync_actor_view(&state);
                return Ok(state);
            }
            state
                .apply_mutation(&mutation)
                .map_err(anyhow::Error::msg)?;
            state.runtime_revision = next_revision(state.runtime_revision)?;
            match self.observer.append_checked(
                world_id,
                Some(&head),
                state.runtime_revision,
                EventKind::Mutated {
                    mutation: mutation.clone(),
                },
            ) {
                Ok(_) => {
                    let _ = self.sync_actor_view(&state);
                    return Ok(state);
                }
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("mutation lost repeated concurrent observer races")
    }

    pub fn observe_egress(
        &self,
        world_id: &str,
        boundary_id: &str,
        result: EgressResult,
        method: &str,
        detail: &str,
    ) -> Result<WorldState> {
        validate_evidence_label("method", method, 64)?;
        validate_evidence_label("detail", detail, 128)?;
        for _ in 0..MAX_CONFLICT_RETRIES {
            let (manifest, mut state, head) = self.load_active(world_id)?;
            if state.phase == WorldPhase::Frozen {
                bail!("world `{world_id}` is frozen");
            }
            if !manifest
                .external_boundaries
                .iter()
                .any(|boundary| boundary.id == boundary_id)
            {
                bail!("unknown external boundary `{boundary_id}`");
            }
            state.runtime_revision = next_revision(state.runtime_revision)?;
            let evidence = EgressEvidence {
                boundary_id: boundary_id.to_owned(),
                result,
                method: method.to_owned(),
                detail: detail.to_owned(),
                observed_at_revision: state.runtime_revision,
            };
            match self.observer.append_checked(
                world_id,
                Some(&head),
                state.runtime_revision,
                EventKind::EgressObserved {
                    evidence: evidence.clone(),
                },
            ) {
                Ok(_) => {
                    state.egress_evidence.push(evidence);
                    let _ = self.sync_actor_view(&state);
                    return Ok(state);
                }
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("egress observation lost repeated concurrent observer races")
    }

    pub fn freeze(&self, world_id: &str) -> Result<WorldState> {
        for _ in 0..MAX_CONFLICT_RETRIES {
            let (_, mut state, head) = self.load_active(world_id)?;
            if state.phase == WorldPhase::Frozen {
                let _ = self.sync_actor_view(&state);
                return Ok(state);
            }
            state.runtime_revision = next_revision(state.runtime_revision)?;
            state.phase = WorldPhase::Frozen;
            match self.observer.append_checked(
                world_id,
                Some(&head),
                state.runtime_revision,
                EventKind::Frozen,
            ) {
                Ok(_) => {
                    let _ = self.sync_actor_view(&state);
                    return Ok(state);
                }
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("freeze lost repeated concurrent observer races")
    }

    pub fn reset(&self, world_id: &str) -> Result<WorldState> {
        for _ in 0..MAX_CONFLICT_RETRIES {
            let (manifest, old_state, head) = self.load_active(world_id)?;
            let mut state = WorldState::baseline(&manifest).map_err(anyhow::Error::msg)?;
            state.runtime_revision = next_revision(old_state.runtime_revision)?;
            match self.observer.append_checked(
                world_id,
                Some(&head),
                state.runtime_revision,
                EventKind::Reset,
            ) {
                Ok(_) => {
                    let _ = self.sync_actor_view(&state);
                    return Ok(state);
                }
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("reset lost repeated concurrent observer races")
    }

    pub fn destroy(&self, world_id: &str) -> Result<WorldEvent> {
        validate_world_id(world_id)?;
        for _ in 0..MAX_CONFLICT_RETRIES {
            let events = self.observer.read_verified(world_id)?;
            if let Some(event) = events.last()
                && matches!(event.kind, EventKind::Destroyed)
            {
                self.finish_destroy(world_id, event.runtime_revision)?;
                return Ok(event.clone());
            }
            let manifest = self.read_persisted_manifest(world_id)?;
            let state = match replay(&manifest, &events)? {
                Replay::Active(state) => state,
                Replay::Destroyed(event) => {
                    self.finish_destroy(world_id, event.runtime_revision)?;
                    return Ok(event);
                }
            };
            let head = events
                .last()
                .ok_or_else(|| anyhow!("observer log has no creation event"))?;
            let revision = next_revision(state.runtime_revision)?;
            match self.observer.append_checked(
                world_id,
                Some(&head.event_hash),
                revision,
                EventKind::Destroyed,
            ) {
                Ok(event) => {
                    self.finish_destroy(world_id, event.runtime_revision)?;
                    return Ok(event);
                }
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("destroy lost repeated concurrent observer races")
    }

    pub(crate) fn observe_service_connection(
        &self,
        world_id: &str,
        service_id: &str,
        observed_at_revision: u64,
    ) -> Result<()> {
        for _ in 0..MAX_CONFLICT_RETRIES {
            let (manifest, state, head) = self.load_active(world_id)?;
            if manifest.service(service_id).is_none() {
                bail!("unknown service `{service_id}`");
            }
            let events = self.observer.read_verified(world_id)?;
            let already_observed = events.iter().any(|event| {
                matches!(
                    &event.kind,
                    EventKind::ServiceConnectionObserved {
                        service_id: observed_service,
                        observed_at_revision: observed_revision,
                    } if observed_service == service_id
                        && *observed_revision == observed_at_revision
                )
            });
            if already_observed {
                return Ok(());
            }
            match self.observer.append_checked(
                world_id,
                Some(&head),
                state.runtime_revision,
                EventKind::ServiceConnectionObserved {
                    service_id: service_id.to_owned(),
                    observed_at_revision,
                },
            ) {
                Ok(_) => return Ok(()),
                Err(ObserverError::Conflict) => continue,
                Err(error) => return Err(error.into()),
            }
        }
        bail!("connection observation lost repeated concurrent observer races")
    }

    pub(crate) fn load_active(
        &self,
        world_id: &str,
    ) -> Result<(NetworkWorldManifest, WorldState, String)> {
        let manifest = self.read_persisted_manifest(world_id)?;
        let events = self.observer.read_verified(world_id)?;
        let state = match replay(&manifest, &events)? {
            Replay::Active(state) => state,
            Replay::Destroyed(_) => bail!("world `{world_id}` is destroyed"),
        };
        let head = events
            .last()
            .ok_or_else(|| anyhow!("observer log has no creation event"))?
            .event_hash
            .clone();
        Ok((manifest, state, head))
    }

    fn persist_manifest_idempotently(&self, manifest: &NetworkWorldManifest) -> Result<()> {
        ensure_directory(&self.authority_root, 0o700, true)?;
        let world_id = manifest.world_id();
        let directory = self.authority_root.join(&world_id);
        ensure_directory(&directory, 0o700, true)?;
        let manifest_path = directory.join(MANIFEST_FILE);
        match fs::symlink_metadata(&manifest_path) {
            Ok(metadata) if metadata.file_type().is_file() => {
                let existing = self.read_persisted_manifest(&world_id)?;
                if existing != *manifest {
                    bail!("persisted manifest does not match its world identity");
                }
                return Ok(());
            }
            Ok(_) => bail!("persisted manifest path is not a regular file"),
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {}
            Err(error) => return Err(error.into()),
        }
        write_json_atomic(&manifest_path, manifest, 0o400)?;
        Ok(())
    }

    fn read_persisted_manifest(&self, world_id: &str) -> Result<NetworkWorldManifest> {
        validate_world_id(world_id)?;
        ensure_owned_existing_directory(&self.authority_root, true)?;
        let directory = self.authority_root.join(world_id);
        ensure_owned_existing_directory(&directory, true)?;
        let manifest: NetworkWorldManifest =
            read_bounded_json(&directory.join(MANIFEST_FILE), MAX_MANIFEST_BYTES)?;
        manifest.validate()?;
        if manifest.world_id() != world_id {
            bail!("world identity does not match persisted manifest");
        }
        Ok(manifest)
    }

    fn sync_actor_view(&self, state: &WorldState) -> Result<()> {
        ensure_directory(&self.actor_root, 0o755, false)?;
        let directory = self.actor_root.join(&state.world_id);
        ensure_directory(&directory, 0o755, false)?;
        let lock = open_private_lock(&directory.join("projection.lock"))?;
        File::lock(&lock)?;
        let projection_path = directory.join(ACTOR_PROJECTION_FILE);
        if let Some(existing) = read_optional_projection(&projection_path)? {
            match existing {
                ActorProjection::Destroyed { .. } => {
                    bail!("actor projection is tombstoned");
                }
                ActorProjection::Active {
                    runtime_revision, ..
                } if runtime_revision > state.runtime_revision => {
                    bail!("newer actor projection already exists");
                }
                ActorProjection::Active { .. } => {}
            }
        }
        let projection = ActorProjection::Active {
            schema_version: WORLD_SCHEMA_VERSION,
            world_id: state.world_id.clone(),
            runtime_revision: state.runtime_revision,
            view: state.actor_view(),
        };
        write_json_atomic(&projection_path, &projection, 0o444)
    }

    fn finish_destroy(&self, world_id: &str, runtime_revision: u64) -> Result<()> {
        self.tombstone_actor(world_id, runtime_revision)?;
        remove_owned_world_directory(&self.authority_root, world_id)?;
        Ok(())
    }

    fn tombstone_actor(&self, world_id: &str, runtime_revision: u64) -> Result<()> {
        ensure_directory(&self.actor_root, 0o755, false)?;
        let directory = self.actor_root.join(world_id);
        ensure_directory(&directory, 0o755, false)?;
        let lock = open_private_lock(&directory.join("projection.lock"))?;
        File::lock(&lock)?;
        let projection = ActorProjection::Destroyed {
            schema_version: WORLD_SCHEMA_VERSION,
            world_id: world_id.to_owned(),
            runtime_revision,
        };
        write_json_atomic(&directory.join(ACTOR_PROJECTION_FILE), &projection, 0o444)
    }
}

impl ActorSurface {
    pub fn open(actor_root: impl Into<PathBuf>, world_id: impl Into<String>) -> Result<Self> {
        let world_id = world_id.into();
        validate_world_id(&world_id)?;
        Ok(Self {
            actor_root: resolve_existing_root(actor_root.into())?,
            world_id,
        })
    }

    pub fn inspect(&self) -> Result<ActorView> {
        let directory = self.actor_root.join(&self.world_id);
        ensure_owned_existing_directory(&self.actor_root, false)?;
        ensure_owned_existing_directory(&directory, false)?;
        let projection: ActorProjection =
            read_bounded_json(&directory.join(ACTOR_PROJECTION_FILE), MAX_ACTOR_VIEW_BYTES)?;
        match projection {
            ActorProjection::Active {
                schema_version,
                world_id,
                runtime_revision,
                view,
            } if schema_version == WORLD_SCHEMA_VERSION
                && world_id == self.world_id
                && view.schema_version == WORLD_SCHEMA_VERSION
                && view.world_id == self.world_id
                && view.runtime_revision == runtime_revision =>
            {
                Ok(view)
            }
            ActorProjection::Destroyed { .. } => bail!("world `{}` is destroyed", self.world_id),
            ActorProjection::Active { .. } => {
                bail!("actor projection world identity or schema mismatch")
            }
        }
    }
}

fn replay(manifest: &NetworkWorldManifest, events: &[WorldEvent]) -> Result<Replay> {
    let first = events
        .first()
        .ok_or_else(|| anyhow!("observer log has no creation event"))?;
    match &first.kind {
        EventKind::Created { manifest_revision }
            if first.runtime_revision == 0
                && manifest_revision == &manifest.manifest_revision() => {}
        _ => bail!("observer creation event does not match manifest"),
    }
    let mut state = WorldState::baseline(manifest).map_err(anyhow::Error::msg)?;

    for (index, event) in events.iter().enumerate().skip(1) {
        let next = next_revision(state.runtime_revision)?;
        match &event.kind {
            EventKind::Created { .. } => bail!("observer contains a repeated creation event"),
            EventKind::Mutated { mutation } => {
                if state.phase == WorldPhase::Frozen || event.runtime_revision != next {
                    bail!("invalid mutation event lifecycle or revision");
                }
                state.apply_mutation(mutation).map_err(anyhow::Error::msg)?;
                state.runtime_revision = event.runtime_revision;
            }
            EventKind::Frozen => {
                if state.phase == WorldPhase::Frozen || event.runtime_revision != next {
                    bail!("invalid freeze event lifecycle or revision");
                }
                state.phase = WorldPhase::Frozen;
                state.runtime_revision = event.runtime_revision;
            }
            EventKind::Reset => {
                if event.runtime_revision != next {
                    bail!("invalid reset event revision");
                }
                state = WorldState::baseline(manifest).map_err(anyhow::Error::msg)?;
                state.runtime_revision = event.runtime_revision;
            }
            EventKind::EgressObserved { evidence } => {
                if state.phase == WorldPhase::Frozen
                    || event.runtime_revision != next
                    || evidence.observed_at_revision != event.runtime_revision
                    || !manifest
                        .external_boundaries
                        .iter()
                        .any(|boundary| boundary.id == evidence.boundary_id)
                {
                    bail!("invalid egress evidence event");
                }
                validate_evidence_label("method", &evidence.method, 64)?;
                validate_evidence_label("detail", &evidence.detail, 128)?;
                state.runtime_revision = event.runtime_revision;
                state.egress_evidence.push(evidence.clone());
            }
            EventKind::ServiceConnectionObserved {
                service_id,
                observed_at_revision,
            } => {
                if event.runtime_revision != state.runtime_revision
                    || *observed_at_revision > state.runtime_revision
                    || manifest.service(service_id).is_none()
                {
                    bail!("invalid service connection observation event");
                }
            }
            EventKind::Destroyed => {
                if event.runtime_revision != next || index + 1 != events.len() {
                    bail!("invalid destruction event lifecycle or revision");
                }
                return Ok(Replay::Destroyed(event.clone()));
            }
        }
    }
    Ok(Replay::Active(state))
}

fn validate_world_id(world_id: &str) -> Result<()> {
    let digest = world_id
        .strip_prefix("nw1-")
        .ok_or_else(|| anyhow!("invalid world id"))?;
    if digest.len() != 64
        || !digest
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        bail!("invalid world id");
    }
    Ok(())
}

fn next_revision(revision: u64) -> Result<u64> {
    revision
        .checked_add(1)
        .ok_or_else(|| anyhow!("world revision overflow"))
}

fn resolve_root_path(path: PathBuf) -> Result<PathBuf> {
    let absolute = absolute_without_parent_components(path)?;
    match fs::symlink_metadata(&absolute) {
        Ok(metadata) => {
            if !metadata.file_type().is_dir() {
                bail!("root path is not a regular directory");
            }
            Ok(fs::canonicalize(absolute)?)
        }
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            let parent = absolute
                .parent()
                .ok_or_else(|| anyhow!("root path has no parent"))?;
            let name = absolute
                .file_name()
                .ok_or_else(|| anyhow!("root path has no final component"))?;
            Ok(fs::canonicalize(parent)?.join(name))
        }
        Err(error) => Err(error.into()),
    }
}

fn resolve_existing_root(path: PathBuf) -> Result<PathBuf> {
    let absolute = absolute_without_parent_components(path)?;
    let metadata = fs::symlink_metadata(&absolute)?;
    if !metadata.file_type().is_dir() {
        bail!("actor root is not a regular directory");
    }
    Ok(fs::canonicalize(absolute)?)
}

fn validate_existing_root_permissions(path: &Path, private: bool) -> Result<()> {
    match fs::symlink_metadata(path) {
        Ok(metadata) => validate_directory_permissions(&metadata, private),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(()),
        Err(error) => Err(error.into()),
    }
}

fn absolute_without_parent_components(path: PathBuf) -> Result<PathBuf> {
    if path
        .components()
        .any(|component| matches!(component, Component::ParentDir))
    {
        bail!("root paths must not contain `..`");
    }
    if path.is_absolute() {
        Ok(path)
    } else {
        Ok(std::env::current_dir()?.join(path))
    }
}

fn read_bounded_json<T: for<'de> Deserialize<'de>>(path: &Path, maximum: u64) -> Result<T> {
    let metadata = fs::symlink_metadata(path)?;
    if !metadata.file_type().is_file() || metadata.len() == 0 || metadata.len() > maximum {
        bail!("persisted JSON is not a bounded regular file");
    }
    let input = fs::read(path)?;
    if input.len() as u64 != metadata.len() {
        bail!("persisted JSON changed while it was read");
    }
    Ok(serde_json::from_slice(&input)?)
}

fn read_optional_projection(path: &Path) -> Result<Option<ActorProjection>> {
    match fs::symlink_metadata(path) {
        Ok(_) => Ok(Some(read_bounded_json(path, MAX_ACTOR_VIEW_BYTES)?)),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(error) => Err(error.into()),
    }
}

fn write_json_atomic(path: &Path, value: &impl Serialize, mode: u32) -> Result<()> {
    if let Ok(metadata) = fs::symlink_metadata(path)
        && !metadata.file_type().is_file()
    {
        bail!("refusing to replace a non-regular persisted file");
    }
    let parent = path
        .parent()
        .ok_or_else(|| anyhow!("persisted path has no parent"))?;
    ensure_existing_directory(parent)?;
    let temporary = parent.join(format!(
        ".pending-{}-{}",
        std::process::id(),
        TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed)
    ));
    let encoded = serde_json::to_vec_pretty(value)?;

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
        file.write_all(b"\n")?;
        file.sync_all()?;
        set_file_mode(&temporary, mode)?;
        fs::rename(&temporary, path)?;
        sync_directory(parent)?;
        Ok::<(), anyhow::Error>(())
    })();
    if result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    result
}

fn open_private_lock(path: &Path) -> Result<File> {
    if let Ok(metadata) = fs::symlink_metadata(path)
        && !metadata.file_type().is_file()
    {
        bail!("lock path is not a regular file");
    }
    let mut options = OpenOptions::new();
    options.create(true).read(true).write(true);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        options.mode(0o600);
    }
    Ok(options.open(path)?)
}

fn validate_evidence_label(kind: &str, text: &str, maximum: usize) -> Result<()> {
    let mut characters = text.chars();
    let valid = text.len() <= maximum
        && characters
            .next()
            .is_some_and(|character| character.is_ascii_lowercase())
        && characters.all(|character| {
            character.is_ascii_lowercase()
                || character.is_ascii_digit()
                || matches!(character, '-' | '_')
        });
    if !valid {
        bail!("egress evidence {kind} must be a bounded public label");
    }
    Ok(())
}

fn ensure_directory(path: &Path, mode: u32, private: bool) -> Result<()> {
    match fs::symlink_metadata(path) {
        Ok(metadata) => {
            if !metadata.file_type().is_dir() {
                bail!("owned path is not a regular directory");
            }
            validate_directory_permissions(&metadata, private)?;
        }
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            match create_directory(path, mode) {
                Ok(()) => {
                    if let Some(parent) = path.parent() {
                        sync_directory(parent)?;
                    }
                }
                Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => {
                    ensure_owned_existing_directory(path, private)?;
                }
                Err(error) => return Err(error.into()),
            }
        }
        Err(error) => return Err(error.into()),
    }
    Ok(())
}

fn ensure_existing_directory(path: &Path) -> Result<()> {
    let metadata = fs::symlink_metadata(path)?;
    if !metadata.file_type().is_dir() {
        bail!("owned path is not a regular directory");
    }
    Ok(())
}

fn ensure_owned_existing_directory(path: &Path, private: bool) -> Result<()> {
    let metadata = fs::symlink_metadata(path)?;
    if !metadata.file_type().is_dir() {
        bail!("owned path is not a regular directory");
    }
    validate_directory_permissions(&metadata, private)
}

fn remove_owned_world_directory(root: &Path, world_id: &str) -> Result<()> {
    let directory = root.join(world_id);
    match fs::symlink_metadata(&directory) {
        Ok(metadata) if metadata.file_type().is_dir() => {
            fs::remove_dir_all(&directory)?;
            sync_directory(root)?;
        }
        Ok(_) => bail!("refusing to remove a non-directory world path"),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {}
        Err(error) => return Err(error.into()),
    }
    Ok(())
}

fn sync_directory(path: &Path) -> Result<()> {
    File::open(path)?.sync_all()?;
    Ok(())
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
fn validate_directory_permissions(metadata: &fs::Metadata, private: bool) -> Result<()> {
    use std::os::unix::fs::PermissionsExt;
    let forbidden = if private { 0o077 } else { 0o022 };
    if metadata.permissions().mode() & forbidden != 0 {
        bail!("owned root directory permissions are too broad");
    }
    Ok(())
}

#[cfg(not(unix))]
fn validate_directory_permissions(_metadata: &fs::Metadata, _private: bool) -> Result<()> {
    Ok(())
}

#[cfg(unix)]
fn set_file_mode(path: &Path, mode: u32) -> Result<()> {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(mode))?;
    Ok(())
}

#[cfg(not(unix))]
fn set_file_mode(path: &Path, _mode: u32) -> Result<()> {
    let mut permissions = fs::metadata(path)?.permissions();
    permissions.set_readonly(true);
    fs::set_permissions(path, permissions)?;
    Ok(())
}
