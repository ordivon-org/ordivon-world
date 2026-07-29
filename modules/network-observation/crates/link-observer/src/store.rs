use std::fs;
use std::path::Path;
use std::sync::Mutex;
use std::time::Duration;

use anyhow::{Context, Result};
use chrono::{DateTime, Utc};
use rusqlite::{Connection, params};

use crate::model::{HealthState, LinkEvent, LinkSnapshot, ServiceState};

pub struct Store {
    connection: Mutex<Connection>,
}

impl Store {
    pub fn open(path: &Path) -> Result<Self> {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)
                .with_context(|| format!("failed to create {}", parent.display()))?;
        }
        let connection =
            Connection::open(path).with_context(|| format!("failed to open {}", path.display()))?;
        Self::from_connection(connection)
    }

    #[cfg(test)]
    pub fn open_in_memory() -> Result<Self> {
        Self::from_connection(Connection::open_in_memory()?)
    }

    fn from_connection(connection: Connection) -> Result<Self> {
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.execute_batch(
            r#"
            PRAGMA journal_mode = WAL;
            PRAGMA synchronous = NORMAL;
            PRAGMA foreign_keys = ON;
            PRAGMA trusted_schema = OFF;

            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            INSERT OR IGNORE INTO metadata(key, value) VALUES ('schema_version', '1');

            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observed_at TEXT NOT NULL,
                health TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS service_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL REFERENCES snapshots(id) ON DELETE CASCADE,
                observed_at TEXT NOT NULL,
                service_id TEXT NOT NULL,
                state TEXT NOT NULL,
                latency_ms REAL,
                failure_class TEXT
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observed_at TEXT NOT NULL,
                kind TEXT NOT NULL,
                severity TEXT NOT NULL,
                summary TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_snapshots_observed_at
                ON snapshots(observed_at DESC);
            CREATE INDEX IF NOT EXISTS idx_service_checks_observed_at
                ON service_checks(observed_at DESC, service_id);
            CREATE INDEX IF NOT EXISTS idx_events_observed_at
                ON events(observed_at DESC);
            "#,
        )?;
        let schema_version: String = connection.query_row(
            "SELECT value FROM metadata WHERE key = 'schema_version'",
            [],
            |row| row.get(0),
        )?;
        if schema_version != "1" {
            return Err(anyhow::anyhow!("unsupported Edge database schema"));
        }
        Ok(Self {
            connection: Mutex::new(connection),
        })
    }

    pub fn record_snapshot(
        &self,
        snapshot: &LinkSnapshot,
        previous: Option<&LinkSnapshot>,
    ) -> Result<()> {
        let payload = serde_json::to_string(snapshot)?;
        let mut connection = self
            .connection
            .lock()
            .map_err(|_| anyhow::anyhow!("edge store mutex poisoned"))?;
        let transaction = connection.transaction()?;
        transaction.execute(
            "INSERT INTO snapshots(observed_at, health, payload_json) VALUES (?1, ?2, ?3)",
            params![
                snapshot.observed_at.to_rfc3339(),
                health_name(snapshot.health),
                payload
            ],
        )?;
        let snapshot_id = transaction.last_insert_rowid();
        for service in &snapshot.services {
            transaction.execute(
                r#"INSERT INTO service_checks(
                    snapshot_id, observed_at, service_id, state, latency_ms, failure_class
                ) VALUES (?1, ?2, ?3, ?4, ?5, ?6)"#,
                params![
                    snapshot_id,
                    snapshot.observed_at.to_rfc3339(),
                    service.id,
                    service_state_name(service.state),
                    service.latency_ms,
                    service.failure_class,
                ],
            )?;
        }
        for event in derive_events(previous, snapshot) {
            transaction.execute(
                "INSERT INTO events(observed_at, kind, severity, summary) VALUES (?1, ?2, ?3, ?4)",
                params![
                    event.observed_at.to_rfc3339(),
                    event.kind,
                    event.severity,
                    event.summary,
                ],
            )?;
        }
        transaction.execute(
            "DELETE FROM snapshots WHERE id NOT IN (SELECT id FROM snapshots ORDER BY id DESC LIMIT 25000)",
            [],
        )?;
        transaction.execute(
            "DELETE FROM events WHERE id NOT IN (SELECT id FROM events ORDER BY id DESC LIMIT 5000)",
            [],
        )?;
        transaction.commit()?;
        Ok(())
    }

    pub fn latest_snapshot(&self) -> Result<Option<LinkSnapshot>> {
        let connection = self
            .connection
            .lock()
            .map_err(|_| anyhow::anyhow!("edge store mutex poisoned"))?;
        let mut statement =
            connection.prepare("SELECT payload_json FROM snapshots ORDER BY id DESC LIMIT 16")?;
        let payloads = statement.query_map([], |row| row.get::<_, String>(0))?;
        for payload in payloads {
            if let Ok(snapshot) = serde_json::from_str::<LinkSnapshot>(&payload?) {
                return Ok(Some(snapshot));
            }
        }
        Ok(None)
    }

    pub fn recent_events(&self, limit: usize) -> Result<Vec<LinkEvent>> {
        let limit = limit.clamp(1, 200) as i64;
        let connection = self
            .connection
            .lock()
            .map_err(|_| anyhow::anyhow!("edge store mutex poisoned"))?;
        let mut statement = connection.prepare(
            "SELECT id, observed_at, kind, severity, summary FROM events ORDER BY id DESC LIMIT ?1",
        )?;
        let rows = statement.query_map([limit], |row| {
            let observed_at: String = row.get(1)?;
            Ok(LinkEvent {
                id: row.get(0)?,
                observed_at: DateTime::parse_from_rfc3339(&observed_at)
                    .map(|value| value.with_timezone(&Utc))
                    .map_err(|error| {
                        rusqlite::Error::FromSqlConversionFailure(
                            1,
                            rusqlite::types::Type::Text,
                            Box::new(error),
                        )
                    })?,
                kind: row.get(2)?,
                severity: row.get(3)?,
                summary: row.get(4)?,
            })
        })?;
        rows.collect::<Result<Vec<_>, _>>().map_err(Into::into)
    }
}

fn derive_events(previous: Option<&LinkSnapshot>, current: &LinkSnapshot) -> Vec<LinkEvent> {
    let mut events = Vec::new();
    let mut push = |kind: &str, severity: &str, summary: String| {
        events.push(LinkEvent {
            id: 0,
            observed_at: current.observed_at,
            kind: kind.to_owned(),
            severity: severity.to_owned(),
            summary,
        });
    };

    let Some(previous) = previous else {
        push(
            "runtime_initialized",
            "info",
            "Ordivon Edge observer initialized".to_owned(),
        );
        return events;
    };

    if previous.health != current.health {
        push(
            "health_changed",
            severity_for_health(current.health),
            format!(
                "Overall health changed from {} to {}",
                health_name(previous.health),
                health_name(current.health)
            ),
        );
    }
    if previous.path_state != current.path_state {
        push(
            "path_changed",
            severity_for_health(current.health),
            format!(
                "Path state changed from {} to {}",
                serde_name(previous.path_state),
                serde_name(current.path_state)
            ),
        );
    }
    if previous.provider.connected != current.provider.connected {
        push(
            "provider_changed",
            if current.provider.connected {
                "info"
            } else {
                "warning"
            },
            if current.provider.connected {
                "Surfshark tunnel became connected".to_owned()
            } else {
                "Surfshark tunnel became disconnected".to_owned()
            },
        );
    }
    for service in &current.services {
        if let Some(old) = previous.services.iter().find(|old| old.id == service.id)
            && old.state != service.state
        {
            push(
                "service_changed",
                if service.state == ServiceState::Failed {
                    "error"
                } else if service.state == ServiceState::Degraded {
                    "warning"
                } else {
                    "info"
                },
                format!(
                    "Service {} changed from {} to {}",
                    service.id,
                    service_state_name(old.state),
                    service_state_name(service.state)
                ),
            );
        }
    }
    events
}

fn severity_for_health(health: HealthState) -> &'static str {
    match health {
        HealthState::Healthy => "info",
        HealthState::Degraded | HealthState::Unknown => "warning",
        HealthState::Failed => "error",
    }
}

fn health_name(value: HealthState) -> &'static str {
    match value {
        HealthState::Healthy => "healthy",
        HealthState::Degraded => "degraded",
        HealthState::Failed => "failed",
        HealthState::Unknown => "unknown",
    }
}

fn service_state_name(value: ServiceState) -> &'static str {
    match value {
        ServiceState::Healthy => "healthy",
        ServiceState::Degraded => "degraded",
        ServiceState::Failed => "failed",
    }
}

fn serde_name<T: serde::Serialize>(value: T) -> String {
    serde_json::to_value(value)
        .ok()
        .and_then(|value| value.as_str().map(ToOwned::to_owned))
        .unwrap_or_else(|| "unknown".to_owned())
}

#[cfg(test)]
mod tests {
    use chrono::Utc;

    use super::*;
    use crate::model::{
        DnsSnapshot, Ipv6Risk, LocalRuntimeSnapshot, PathState, PrivacyStatus, ProviderSnapshot,
        RouteSnapshot, ServiceCheck,
    };

    fn snapshot(health: HealthState, connected: bool) -> LinkSnapshot {
        LinkSnapshot {
            schema_version: 1,
            observed_at: Utc::now(),
            health,
            path_state: if connected {
                PathState::Tunneled
            } else {
                PathState::Direct
            },
            provider: ProviderSnapshot {
                name: "surfshark".to_owned(),
                detected: true,
                connected,
                protocol: connected.then(|| "wireguard".to_owned()),
            },
            route: RouteSnapshot {
                effective_interface_class: if connected { "tunnel" } else { "physical" }.to_owned(),
                ipv4_tunnel_route: connected,
                mtu: Some(1380),
                ipv6_default_route: true,
                ipv6_tunnel_route: false,
                ipv6_risk: Ipv6Risk::LatentPhysicalDefault,
            },
            dns: DnsSnapshot {
                mode: "wsl_dns_tunneling".to_owned(),
                resolver_count: 1,
            },
            local_runtime: LocalRuntimeSnapshot {
                cloudflare_tunnel_running: Some(true),
                ordivon_mcp_running: Some(true),
            },
            services: vec![ServiceCheck {
                id: "github-web".to_owned(),
                state: ServiceState::Healthy,
                latency_ms: Some(200.0),
                failure_class: None,
            }],
            reasons: Vec::new(),
            privacy: PrivacyStatus {
                sensitive_fields_redacted: true,
                network_binding: "loopback_only".to_owned(),
                raw_command_output_retained: false,
            },
        }
    }

    #[test]
    fn stores_sanitized_snapshots_and_events() {
        let store = Store::open_in_memory().expect("store");
        let first = snapshot(HealthState::Healthy, true);
        store.record_snapshot(&first, None).expect("first");
        let second = snapshot(HealthState::Degraded, false);
        store
            .record_snapshot(&second, Some(&first))
            .expect("second");
        let events = store.recent_events(20).expect("events");
        assert!(events.iter().any(|event| event.kind == "health_changed"));
        assert!(events.iter().any(|event| event.kind == "provider_changed"));
        assert_eq!(
            store.latest_snapshot().expect("latest"),
            Some(second.clone())
        );
        store
            .connection
            .lock()
            .expect("lock")
            .execute(
                "INSERT INTO snapshots(observed_at, health, payload_json) VALUES (?1, ?2, ?3)",
                params![Utc::now().to_rfc3339(), "failed", "{not-json"],
            )
            .expect("corrupt row");
        assert_eq!(store.latest_snapshot().expect("fallback"), Some(second));
    }

    #[test]
    fn concurrent_reads_and_writes_remain_consistent() {
        use std::sync::Arc;
        use std::thread;

        let store = Arc::new(Store::open_in_memory().expect("store"));
        let mut workers = Vec::new();
        for worker in 0..4 {
            let store = Arc::clone(&store);
            workers.push(thread::spawn(move || {
                for index in 0..50 {
                    let mut value = snapshot(HealthState::Healthy, true);
                    value.observed_at =
                        Utc::now() + chrono::Duration::milliseconds(i64::from(worker * 50 + index));
                    store.record_snapshot(&value, None).expect("write");
                }
            }));
        }
        for _ in 0..4 {
            let store = Arc::clone(&store);
            workers.push(thread::spawn(move || {
                for _ in 0..100 {
                    let _ = store.recent_events(20).expect("read events");
                    let _ = store.latest_snapshot().expect("read snapshot");
                }
            }));
        }
        for worker in workers {
            worker.join().expect("worker");
        }
        assert!(store.latest_snapshot().expect("latest").is_some());
        assert_eq!(store.recent_events(200).expect("events").len(), 200);
    }

    #[test]
    fn busy_timeout_allows_a_short_external_writer_lock() {
        use std::sync::Arc;
        use std::thread;
        use std::time::{Duration, Instant};

        let directory = tempfile::tempdir().expect("tempdir");
        let path = directory.path().join("edge.db");
        let store = Arc::new(Store::open(&path).expect("store"));
        let blocker = Connection::open(&path).expect("blocker");
        blocker
            .execute_batch("PRAGMA journal_mode = WAL; BEGIN IMMEDIATE;")
            .expect("begin lock");

        let writer_store = Arc::clone(&store);
        let started = Instant::now();
        let writer = thread::spawn(move || {
            writer_store
                .record_snapshot(&snapshot(HealthState::Healthy, true), None)
                .expect("write after lock")
        });
        thread::sleep(Duration::from_millis(200));
        blocker.execute_batch("COMMIT;").expect("release lock");
        writer.join().expect("writer");
        assert!(started.elapsed() >= Duration::from_millis(150));
        assert!(store.latest_snapshot().expect("latest").is_some());
    }

    #[test]
    fn rejects_unknown_database_schema() {
        let connection = Connection::open_in_memory().expect("connection");
        connection
            .execute_batch(
                "CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                 INSERT INTO metadata(key, value) VALUES ('schema_version', '999');",
            )
            .expect("metadata");
        let error = match Store::from_connection(connection) {
            Ok(_) => panic!("schema must fail"),
            Err(error) => error,
        };
        assert!(
            error
                .to_string()
                .contains("unsupported Edge database schema")
        );
    }

    #[test]
    fn snapshot_json_has_no_identity_fields() {
        let value = serde_json::to_value(snapshot(HealthState::Healthy, true)).expect("json");
        let rendered = value.to_string();
        for forbidden in [
            "public_ip",
            "remote_ip",
            "hostname",
            "username",
            "mac_address",
            "local_address",
        ] {
            assert!(
                !rendered.contains(forbidden),
                "unexpected field {forbidden}"
            );
        }
    }
}
