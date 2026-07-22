use std::fmt;

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use thiserror::Error;

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
    Timeout,
    Tool,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ProbeResult {
    pub schema_version: u32,
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
    pub http_status: Option<u16>,
    pub remote_ip: Option<String>,
    pub success: bool,
    pub failure_class: Option<FailureClass>,
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
    #[error("target id is empty")]
    EmptyTargetId,
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
}
