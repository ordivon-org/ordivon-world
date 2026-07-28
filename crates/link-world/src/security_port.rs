use std::fs::{self, File, OpenOptions};
use std::io::{Read, Write};
use std::net::TcpListener;
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, bail};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};

use crate::{
    Controller, EffectSemantics, EventKind, NetworkWorldManifest, WorldInspection, WorldPhase,
};

const PORT_SCHEMA_VERSION: u32 = 1;
const MAX_OPERATION_BYTES: u64 = 1024 * 1024;

#[derive(Debug, Clone)]
pub struct SecurityPortPaths {
    pub manifest: PathBuf,
    pub authority_root: PathBuf,
    pub observer_root: PathBuf,
    pub actor_root: PathBuf,
    pub operation_root: PathBuf,
    pub reconstruction_root: PathBuf,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, clap::ValueEnum)]
#[serde(rename_all = "snake_case")]
pub enum SecurityOperation {
    Prepare,
    Start,
    Freeze,
    Reset,
    Destroy,
    Reconstruct,
    Verify,
}

impl SecurityOperation {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Prepare => "prepare",
            Self::Start => "start",
            Self::Freeze => "freeze",
            Self::Reset => "reset",
            Self::Destroy => "destroy",
            Self::Reconstruct => "reconstruct",
            Self::Verify => "verify",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct BindingSnapshot {
    pub native_id: String,
    pub revision: String,
    pub root_digest: String,
    pub metadata: Value,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ResidualCheck {
    pub component: String,
    pub subject_id: String,
    pub status: String,
    pub detail: String,
    pub evidence_ref: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct OperationJournal {
    schema_version: u32,
    operation_id: String,
    operation: SecurityOperation,
    pre_runtime_revision: Option<u64>,
    state: JournalState,
    #[serde(default)]
    result: Option<Value>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
enum JournalState {
    Prepared,
    Succeeded,
}

#[derive(Debug, Clone)]
pub struct SecurityPort {
    paths: SecurityPortPaths,
    manifest: NetworkWorldManifest,
    controller: Controller,
}

impl SecurityPort {
    pub fn open(paths: SecurityPortPaths) -> Result<Self> {
        let manifest = Controller::load_manifest(&paths.manifest)?;
        Controller::validate_manifest(&manifest)?;
        validate_additional_roots(&paths)?;
        let controller = Controller::new(
            paths.authority_root.clone(),
            paths.observer_root.clone(),
            paths.actor_root.clone(),
        )?;
        Ok(Self {
            paths,
            manifest: manifest.normalized(),
            controller,
        })
    }

    pub fn snapshot(&self) -> BindingSnapshot {
        BindingSnapshot {
            native_id: self.manifest.world_id(),
            revision: self.manifest.manifest_revision(),
            root_digest: self.manifest.manifest_revision(),
            metadata: json!({
                "schema_version": PORT_SCHEMA_VERSION,
                "manifest_name": self.manifest.name,
                "world_schema_version": self.manifest.schema_version,
                "effect_semantics": EffectSemantics::network_world_v1(),
            }),
        }
    }

    pub fn execute(&self, operation: SecurityOperation, operation_id: &str) -> Result<Value> {
        self.execute_with_fault(operation, operation_id, false)
    }

    pub fn execute_with_fault(
        &self,
        operation: SecurityOperation,
        operation_id: &str,
        fault_after_effect: bool,
    ) -> Result<Value> {
        validate_operation_id(operation_id)?;
        if let Some(journal) = self.read_journal(operation_id)? {
            if journal.operation != operation {
                bail!("operation ID is bound to another Link operation");
            }
            if journal.state == JournalState::Succeeded {
                return journal
                    .result
                    .ok_or_else(|| anyhow::anyhow!("succeeded operation lacks a receipt"));
            }
            return self.reconcile(operation, operation_id);
        }

        let pre_runtime_revision = self
            .active_inspection()
            .ok()
            .map(|item| item.state.runtime_revision);
        self.write_journal(&OperationJournal {
            schema_version: PORT_SCHEMA_VERSION,
            operation_id: operation_id.to_owned(),
            operation,
            pre_runtime_revision,
            state: JournalState::Prepared,
            result: None,
        })?;
        let result = self.apply(operation, operation_id)?;
        if fault_after_effect {
            bail!("injected Link security-port response loss after native effect");
        }
        self.write_journal(&OperationJournal {
            schema_version: PORT_SCHEMA_VERSION,
            operation_id: operation_id.to_owned(),
            operation,
            pre_runtime_revision,
            state: JournalState::Succeeded,
            result: Some(result.clone()),
        })?;
        Ok(result)
    }

    pub fn reconcile(&self, operation: SecurityOperation, operation_id: &str) -> Result<Value> {
        validate_operation_id(operation_id)?;
        let journal = self
            .read_journal(operation_id)?
            .ok_or_else(|| anyhow::anyhow!("no matching Link operation journal"))?;
        if journal.operation != operation {
            bail!("operation ID is bound to another Link operation");
        }
        if journal.state == JournalState::Succeeded {
            return journal
                .result
                .ok_or_else(|| anyhow::anyhow!("succeeded operation lacks a receipt"));
        }

        let detail = match operation {
            SecurityOperation::Prepare | SecurityOperation::Start => {
                json!({"inspection": self.controller.inspect(&self.manifest.world_id())?})
            }
            SecurityOperation::Freeze => {
                let inspection = self.controller.inspect(&self.manifest.world_id())?;
                if inspection.state.phase != WorldPhase::Frozen {
                    bail!("Link World is not frozen");
                }
                json!({"inspection": inspection})
            }
            SecurityOperation::Reset => {
                let expected = journal
                    .pre_runtime_revision
                    .and_then(|revision| revision.checked_add(1))
                    .ok_or_else(|| anyhow::anyhow!("reset journal lacks a valid prior revision"))?;
                let events = self.controller.events(&self.manifest.world_id())?;
                let event = events
                    .last()
                    .ok_or_else(|| anyhow::anyhow!("Link observer has no events"))?;
                if event.runtime_revision != expected || !matches!(event.kind, EventKind::Reset) {
                    bail!("Link observer does not prove the original reset effect");
                }
                json!({
                    "inspection": self.controller.inspect(&self.manifest.world_id())?,
                    "proved_event": event,
                })
            }
            SecurityOperation::Destroy => {
                let events = self.controller.events(&self.manifest.world_id())?;
                let event = events
                    .last()
                    .ok_or_else(|| anyhow::anyhow!("Link observer has no events"))?;
                if !matches!(event.kind, EventKind::Destroyed) {
                    bail!("Link observer does not prove destruction");
                }
                json!({"proved_event": event, "observer_event_count": events.len()})
            }
            SecurityOperation::Verify => self.verify_detail()?,
            SecurityOperation::Reconstruct => {
                bail!("reconstruction outcome cannot be inferred after a lost response")
            }
        };
        let result = self.receipt(operation, operation_id, true, detail);
        self.write_journal(&OperationJournal {
            state: JournalState::Succeeded,
            result: Some(result.clone()),
            ..journal
        })?;
        Ok(result)
    }

    pub fn residual_checks(&self) -> Vec<ResidualCheck> {
        let world_id = self.manifest.world_id();
        let mut checks = Vec::new();
        let authority = self.paths.authority_root.join(&world_id);
        checks.push(ResidualCheck {
            component: "link".to_owned(),
            subject_id: format!("link-world:{world_id}:authority"),
            status: if authority.exists() {
                "unexpected_residual"
            } else {
                "clean"
            }
            .to_owned(),
            detail: if authority.exists() {
                "authoritative World state remains after destruction"
            } else {
                "authoritative World state is absent"
            }
            .to_owned(),
            evidence_ref: None,
        });

        match self.controller.events(&world_id) {
            Ok(events) => {
                let destroyed = events
                    .last()
                    .is_some_and(|event| matches!(event.kind, EventKind::Destroyed));
                checks.push(ResidualCheck {
                    component: "link".to_owned(),
                    subject_id: format!("link-world:{world_id}:observer"),
                    status: if destroyed {
                        "expected_retained"
                    } else {
                        "unexpected_residual"
                    }
                    .to_owned(),
                    detail: if destroyed {
                        "verified observer history ends in destruction and is retained"
                    } else {
                        "observer history does not prove destruction"
                    }
                    .to_owned(),
                    evidence_ref: Some(format!(
                        "file://{}",
                        self.paths.observer_root.join(&world_id).display()
                    )),
                });
            }
            Err(error) => checks.push(ResidualCheck {
                component: "link".to_owned(),
                subject_id: format!("link-world:{world_id}:observer"),
                status: "observer_unavailable".to_owned(),
                detail: bounded(&error.to_string()),
                evidence_ref: None,
            }),
        }

        let actor_projection = self
            .paths
            .actor_root
            .join(&world_id)
            .join("projection.json");
        let actor_destroyed = read_json_value(&actor_projection)
            .ok()
            .and_then(|value| {
                value
                    .get("status")
                    .and_then(Value::as_str)
                    .map(str::to_owned)
            })
            .as_deref()
            == Some("destroyed");
        checks.push(ResidualCheck {
            component: "link".to_owned(),
            subject_id: format!("link-world:{world_id}:actor-projection"),
            status: if actor_destroyed {
                "expected_retained"
            } else {
                "unknown"
            }
            .to_owned(),
            detail: if actor_destroyed {
                "evaluated-actor projection is a destruction tombstone"
            } else {
                "actor projection destruction tombstone could not be verified"
            }
            .to_owned(),
            evidence_ref: actor_projection
                .exists()
                .then(|| format!("file://{}", actor_projection.display())),
        });

        for service in self.manifest.nodes.iter().flat_map(|node| &node.services) {
            let Some(address) = service.fixture_address else {
                continue;
            };
            let (status, detail) = match TcpListener::bind(address) {
                Ok(listener) => {
                    drop(listener);
                    ("clean", "fixture address is no longer held by a listener")
                }
                Err(error) if error.kind() == std::io::ErrorKind::AddrInUse => (
                    "unexpected_residual",
                    "fixture address remains occupied after lifecycle shutdown",
                ),
                Err(_) => (
                    "unknown",
                    "fixture address could not be independently inspected",
                ),
            };
            checks.push(ResidualCheck {
                component: "link".to_owned(),
                subject_id: format!("link-world:{world_id}:fixture:{}", service.id),
                status: status.to_owned(),
                detail: detail.to_owned(),
                evidence_ref: None,
            });
        }

        checks.push(ResidualCheck {
            component: "link".to_owned(),
            subject_id: format!("link-world:{world_id}:operation-journal"),
            status: "expected_retained".to_owned(),
            detail: "component-side operation receipts are retained for reconciliation".to_owned(),
            evidence_ref: Some(format!("file://{}", self.operation_directory().display())),
        });
        checks
    }

    fn apply(&self, operation: SecurityOperation, operation_id: &str) -> Result<Value> {
        let world_id = self.manifest.world_id();
        let detail = match operation {
            SecurityOperation::Prepare => {
                json!({"inspection": self.controller.create(&self.manifest)?})
            }
            SecurityOperation::Start => {
                json!({"inspection": self.controller.inspect(&world_id)?})
            }
            SecurityOperation::Freeze => {
                let state = self.controller.freeze(&world_id)?;
                json!({
                    "state": state,
                    "inspection": self.controller.inspect(&world_id)?,
                })
            }
            SecurityOperation::Reset => {
                let state = self.controller.reset(&world_id)?;
                json!({
                    "state": state,
                    "inspection": self.controller.inspect(&world_id)?,
                })
            }
            SecurityOperation::Destroy => {
                let destroyed = self.controller.destroy(&world_id)?;
                let events = self.controller.events(&world_id)?;
                json!({"destroyed": destroyed, "observer_event_count": events.len()})
            }
            SecurityOperation::Reconstruct => self.reconstruct(operation_id)?,
            SecurityOperation::Verify => self.verify_detail()?,
        };
        Ok(self.receipt(operation, operation_id, false, detail))
    }

    fn reconstruct(&self, operation_id: &str) -> Result<Value> {
        let token = operation_token(operation_id);
        let root = self.paths.reconstruction_root.join(token);
        if root.exists() {
            fs::remove_dir_all(&root).context("failed to clear stale reconstruction root")?;
        }
        fs::create_dir_all(&root).context("failed to create reconstruction root")?;
        set_private_directory(&root)?;
        let result = (|| -> Result<Value> {
            let authority = root.join("authority");
            let observer = root.join("observer");
            let actor = root.join("actor");
            let controller = Controller::new(authority, observer, actor)?;
            let inspection = controller.create(&self.manifest)?;
            let destroyed = controller.destroy(&self.manifest.world_id())?;
            Ok(json!({
                "snapshot": self.snapshot(),
                "inspection": inspection,
                "destroyed": destroyed,
                "fresh_root_removed": true,
            }))
        })();
        if root.exists() {
            fs::remove_dir_all(&root).context("failed to remove reconstruction root")?;
        }
        result
    }

    fn verify_detail(&self) -> Result<Value> {
        let world_id = self.manifest.world_id();
        match self.controller.inspect(&world_id) {
            Ok(inspection) => Ok(json!({"mode": "active", "inspection": inspection})),
            Err(_) => {
                let events = self.controller.events(&world_id)?;
                let event = events
                    .last()
                    .ok_or_else(|| anyhow::anyhow!("Link observer has no events"))?;
                if !matches!(event.kind, EventKind::Destroyed) {
                    bail!("Link World is unavailable without a destruction event");
                }
                Ok(json!({
                    "mode": "destroyed",
                    "observer_event_count": events.len(),
                    "observer_head": event,
                }))
            }
        }
    }

    fn receipt(
        &self,
        operation: SecurityOperation,
        operation_id: &str,
        reconciled: bool,
        detail: Value,
    ) -> Value {
        json!({
            "schema_version": PORT_SCHEMA_VERSION,
            "project": "link",
            "operation": operation,
            "operation_id": operation_id,
            "world_id": self.manifest.world_id(),
            "manifest_revision": self.manifest.manifest_revision(),
            "reconciled": reconciled,
            "detail": detail,
        })
    }

    fn active_inspection(&self) -> Result<WorldInspection> {
        self.controller.inspect(&self.manifest.world_id())
    }

    fn operation_directory(&self) -> PathBuf {
        self.paths.operation_root.join(self.manifest.world_id())
    }

    fn operation_path(&self, operation_id: &str) -> PathBuf {
        self.operation_directory()
            .join(format!("{}.json", operation_token(operation_id)))
    }

    fn read_journal(&self, operation_id: &str) -> Result<Option<OperationJournal>> {
        let path = self.operation_path(operation_id);
        if !path.exists() {
            return Ok(None);
        }
        let metadata = fs::symlink_metadata(&path)?;
        if !metadata.file_type().is_file() || metadata.len() > MAX_OPERATION_BYTES {
            bail!("Link operation journal is not a bounded regular file");
        }
        let mut bytes = Vec::with_capacity(metadata.len() as usize);
        File::open(&path)?
            .take(MAX_OPERATION_BYTES)
            .read_to_end(&mut bytes)?;
        let journal: OperationJournal = serde_json::from_slice(&bytes)?;
        if journal.schema_version != PORT_SCHEMA_VERSION || journal.operation_id != operation_id {
            bail!("Link operation journal identity or schema mismatch");
        }
        Ok(Some(journal))
    }

    fn write_journal(&self, journal: &OperationJournal) -> Result<()> {
        let directory = self.operation_directory();
        fs::create_dir_all(&directory)?;
        set_private_directory(&directory)?;
        let path = self.operation_path(&journal.operation_id);
        let temporary = directory.join(format!(
            ".{}.{}.tmp",
            operation_token(&journal.operation_id),
            std::process::id()
        ));
        let mut file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&temporary)?;
        set_private_file(&file)?;
        serde_json::to_writer(&mut file, journal)?;
        file.write_all(b"\n")?;
        file.sync_all()?;
        fs::rename(&temporary, &path)?;
        File::open(&directory)?.sync_all()?;
        Ok(())
    }
}

fn validate_additional_roots(paths: &SecurityPortPaths) -> Result<()> {
    let roots = [
        absolute(&paths.authority_root)?,
        absolute(&paths.observer_root)?,
        absolute(&paths.actor_root)?,
        absolute(&paths.operation_root)?,
        absolute(&paths.reconstruction_root)?,
    ];
    for (index, root) in roots.iter().enumerate() {
        if root.parent().is_none() {
            bail!("Security Port roots must not be filesystem roots");
        }
        if let Ok(metadata) = fs::symlink_metadata(root)
            && metadata.file_type().is_symlink()
        {
            bail!("Security Port roots must not be symbolic links");
        }
        for other in roots.iter().skip(index + 1) {
            if root == other || root.starts_with(other) || other.starts_with(root) {
                bail!("Security Port roots must be independent paths");
            }
        }
    }
    Ok(())
}

fn validate_operation_id(value: &str) -> Result<()> {
    if value.is_empty()
        || value.len() > 128
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || b"._:-".contains(&byte))
    {
        bail!("invalid Security operation ID");
    }
    Ok(())
}

fn operation_token(operation_id: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(b"ordivon-link/security-port-operation/v1\0");
    hasher.update(operation_id.as_bytes());
    hasher
        .finalize()
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn absolute(path: &Path) -> Result<PathBuf> {
    if path.is_absolute() {
        Ok(path.to_path_buf())
    } else {
        Ok(std::env::current_dir()?.join(path))
    }
}

fn read_json_value(path: &Path) -> Result<Value> {
    let metadata = fs::symlink_metadata(path)?;
    if !metadata.file_type().is_file() || metadata.len() > MAX_OPERATION_BYTES {
        bail!("JSON evidence path is not a bounded regular file");
    }
    Ok(serde_json::from_slice(&fs::read(path)?)?)
}

fn bounded(value: &str) -> String {
    value.chars().take(2048).collect()
}

#[cfg(unix)]
fn set_private_directory(path: &Path) -> Result<()> {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(0o700))?;
    Ok(())
}

#[cfg(not(unix))]
fn set_private_directory(_path: &Path) -> Result<()> {
    Ok(())
}

#[cfg(unix)]
fn set_private_file(file: &File) -> Result<()> {
    use std::os::unix::fs::PermissionsExt;
    file.set_permissions(fs::Permissions::from_mode(0o600))?;
    Ok(())
}

#[cfg(not(unix))]
fn set_private_file(_file: &File) -> Result<()> {
    Ok(())
}
