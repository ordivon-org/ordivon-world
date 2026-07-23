use std::fmt;

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(
    Debug, Clone, Copy, Default, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord,
)]
#[serde(rename_all = "snake_case")]
pub enum ProbeKind {
    #[default]
    Reachability,
    Transfer,
    ConnectionLifetime,
}

impl fmt::Display for ProbeKind {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Reachability => formatter.write_str("reachability"),
            Self::Transfer => formatter.write_str("transfer"),
            Self::ConnectionLifetime => formatter.write_str("connection_lifetime"),
        }
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ProbeTermination {
    Completed,
    DeadlineReached,
    Failed,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum ProbeProtocol {
    HttpTls,
    Quic,
}

impl fmt::Display for ProbeProtocol {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::HttpTls => formatter.write_str("http_tls"),
            Self::Quic => formatter.write_str("quic"),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Device {
    pub id: String,
    pub label: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Edge {
    pub id: String,
    pub provider: String,
    pub region: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Target {
    pub id: String,
    pub url: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Transport {
    pub id: String,
    pub implementation: String,
    pub protocol: ProbeProtocol,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct RouteDecision {
    pub device_id: String,
    pub target_id: String,
    pub selected_route: String,
    pub selected_transport: String,
    pub reason: String,
    pub decided_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum FailureClass {
    Configuration,
    Dns,
    TcpConnect,
    TlsHandshake,
    QuicHandshake,
    Http,
    Transfer,
    ConnectionLifetime,
    Timeout,
    Tool,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ProbeResult {
    pub schema_version: u32,
    #[serde(default)]
    pub probe_kind: ProbeKind,
    #[serde(default)]
    pub collection_id: Option<String>,
    #[serde(default)]
    pub sample_index: Option<u32>,
    pub target: String,
    pub url: String,
    pub network: String,
    pub route: String,
    pub protocol: ProbeProtocol,
    pub started_at: DateTime<Utc>,
    pub dns_ms: Option<f64>,
    pub connect_ms: Option<f64>,
    pub tls_ms: Option<f64>,
    pub ttfb_ms: Option<f64>,
    pub total_ms: Option<f64>,
    #[serde(default)]
    pub requested_duration_ms: Option<u64>,
    #[serde(default)]
    pub bytes_downloaded: Option<u64>,
    #[serde(default)]
    pub speed_download_bps: Option<f64>,
    #[serde(default)]
    pub connection_count: Option<u32>,
    #[serde(default)]
    pub http_version: Option<String>,
    pub http_status: Option<u16>,
    pub remote_ip: Option<String>,
    pub success: bool,
    pub failure_class: Option<FailureClass>,
    #[serde(default)]
    pub termination: Option<ProbeTermination>,
    pub tool_exit_code: Option<i32>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TargetRegistry {
    pub schema_version: u32,
    pub targets: Vec<TargetConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TargetConfig {
    pub id: String,
    pub url: String,
    #[serde(default = "default_enabled")]
    pub enabled: bool,
    pub protocols: Vec<ProbeProtocol>,
}

const MAX_TARGETS: usize = 64;
const MAX_TARGET_ID_BYTES: usize = 64;
const MAX_TARGET_URL_BYTES: usize = 2048;

const fn default_enabled() -> bool {
    true
}

impl TargetRegistry {
    pub fn validate(&self) -> Result<(), ValidationError> {
        if self.schema_version != 1 {
            return Err(ValidationError::UnsupportedSchema(self.schema_version));
        }
        if self.targets.is_empty() {
            return Err(ValidationError::EmptyRegistry);
        }
        if self.targets.len() > MAX_TARGETS {
            return Err(ValidationError::TooManyTargets {
                count: self.targets.len(),
                maximum: MAX_TARGETS,
            });
        }

        let mut ids = std::collections::BTreeSet::new();
        for target in &self.targets {
            target.validate()?;
            if !ids.insert(target.id.as_str()) {
                return Err(ValidationError::DuplicateTarget(target.id.clone()));
            }
        }
        Ok(())
    }
}

impl TargetConfig {
    pub fn validate(&self) -> Result<(), ValidationError> {
        if self.id.trim().is_empty() {
            return Err(ValidationError::EmptyTargetId);
        }
        if self.id.len() > MAX_TARGET_ID_BYTES {
            return Err(ValidationError::TargetIdTooLong(self.id.clone()));
        }
        let mut characters = self.id.chars();
        let valid_first = characters
            .next()
            .is_some_and(|character| character.is_ascii_lowercase());
        let valid_rest = characters.all(|character| {
            character.is_ascii_lowercase()
                || character.is_ascii_digit()
                || matches!(character, '-' | '_')
        });
        if !valid_first || !valid_rest {
            return Err(ValidationError::UnsafeTargetId(self.id.clone()));
        }
        if self.url.len() > MAX_TARGET_URL_BYTES {
            return Err(ValidationError::TargetUrlTooLong(self.id.clone()));
        }
        if self.url.chars().any(char::is_whitespace) {
            return Err(ValidationError::UnsafeTargetUrl(self.id.clone()));
        }
        if !self.url.starts_with("https://") {
            return Err(ValidationError::NonHttpsUrl(self.id.clone()));
        }
        if self.protocols.is_empty() {
            return Err(ValidationError::NoProtocols(self.id.clone()));
        }
        Ok(())
    }
}

#[derive(Debug, Error, PartialEq, Eq)]
pub enum ValidationError {
    #[error("unsupported target registry schema version {0}")]
    UnsupportedSchema(u32),
    #[error("target registry is empty")]
    EmptyRegistry,
    #[error("target registry has {count} targets; maximum is {maximum}")]
    TooManyTargets { count: usize, maximum: usize },
    #[error("target id is empty")]
    EmptyTargetId,
    #[error("target id is too long: {0}")]
    TargetIdTooLong(String),
    #[error(
        "target id must start with a lowercase letter and contain only lowercase letters, digits, '-' or '_': {0}"
    )]
    UnsafeTargetId(String),
    #[error("target URL is too long for {0}")]
    TargetUrlTooLong(String),
    #[error("target URL contains whitespace for {0}")]
    UnsafeTargetUrl(String),
    #[error("target {0} does not use https")]
    NonHttpsUrl(String),
    #[error("target {0} has no protocols")]
    NoProtocols(String),
    #[error("duplicate target id {0}")]
    DuplicateTarget(String),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn registry_rejects_duplicate_ids() {
        let registry = TargetRegistry {
            schema_version: 1,
            targets: vec![
                TargetConfig {
                    id: "github".into(),
                    url: "https://github.com/".into(),
                    enabled: true,
                    protocols: vec![ProbeProtocol::HttpTls],
                },
                TargetConfig {
                    id: "github".into(),
                    url: "https://api.github.com/".into(),
                    enabled: true,
                    protocols: vec![ProbeProtocol::Quic],
                },
            ],
        };

        assert_eq!(
            registry.validate(),
            Err(ValidationError::DuplicateTarget("github".into()))
        );
    }

    #[test]
    fn target_requires_https() {
        let target = TargetConfig {
            id: "example".into(),
            url: "http://example.com".into(),
            enabled: true,
            protocols: vec![ProbeProtocol::HttpTls],
        };

        assert_eq!(
            target.validate(),
            Err(ValidationError::NonHttpsUrl("example".into()))
        );
    }

    #[test]
    fn target_id_is_a_bounded_public_label() {
        for id in ["192.168.1.1", "UserName", "private name", "-leading"] {
            let target = TargetConfig {
                id: id.into(),
                url: "https://example.com/".into(),
                enabled: true,
                protocols: vec![ProbeProtocol::HttpTls],
            };
            assert!(matches!(
                target.validate(),
                Err(ValidationError::UnsafeTargetId(_))
            ));
        }
        let valid = TargetConfig {
            id: "openai-api_1".into(),
            url: "https://example.com/".into(),
            enabled: true,
            protocols: vec![ProbeProtocol::HttpTls],
        };
        assert_eq!(valid.validate(), Ok(()));
    }

    #[test]
    fn registry_rejects_unbounded_target_count() {
        let targets = (0..=MAX_TARGETS)
            .map(|index| TargetConfig {
                id: format!("target-{index}"),
                url: "https://example.com/".into(),
                enabled: true,
                protocols: vec![ProbeProtocol::HttpTls],
            })
            .collect();
        let registry = TargetRegistry {
            schema_version: 1,
            targets,
        };
        assert!(matches!(
            registry.validate(),
            Err(ValidationError::TooManyTargets { .. })
        ));
    }

    #[test]
    fn old_probe_result_defaults_to_reachability() {
        let raw = r#"{
          "schema_version":1,
          "target":"example",
          "url":"https://example.com/",
          "network":"test",
          "route":"direct-process",
          "protocol":"http_tls",
          "started_at":"2026-07-23T00:00:00Z",
          "dns_ms":1.0,
          "connect_ms":2.0,
          "tls_ms":3.0,
          "ttfb_ms":4.0,
          "total_ms":5.0,
          "http_status":200,
          "remote_ip":null,
          "success":true,
          "failure_class":null,
          "tool_exit_code":0,
          "error":null
        }"#;

        let result: ProbeResult = serde_json::from_str(raw).expect("deserialize old result");
        assert_eq!(result.probe_kind, ProbeKind::Reachability);
        assert_eq!(result.bytes_downloaded, None);
    }
}
