use std::fmt;

use chrono::{DateTime, NaiveDate, Utc};
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

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum StudyRole {
    Baseline,
    Candidate,
    Comparator,
    Platform,
    Reference,
}

impl fmt::Display for StudyRole {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Baseline => "baseline",
            Self::Candidate => "candidate",
            Self::Comparator => "comparator",
            Self::Platform => "platform",
            Self::Reference => "reference",
        })
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum SourceStatus {
    OpenSource,
    SpecificationOnly,
}

impl fmt::Display for SourceStatus {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::OpenSource => "open_source",
            Self::SpecificationOnly => "specification_only",
        })
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum TransportLayer {
    IpTunnel,
    StreamProxy,
    DatagramProxy,
    MultiprotocolPlatform,
    Specification,
}

impl fmt::Display for TransportLayer {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::IpTunnel => "ip_tunnel",
            Self::StreamProxy => "stream_proxy",
            Self::DatagramProxy => "datagram_proxy",
            Self::MultiprotocolPlatform => "multiprotocol_platform",
            Self::Specification => "specification",
        })
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum TransportCarrier {
    Tcp,
    Udp,
    Quic,
    Tls,
    Http2,
    Http3,
}

impl fmt::Display for TransportCarrier {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Tcp => "tcp",
            Self::Udp => "udp",
            Self::Quic => "quic",
            Self::Tls => "tls",
            Self::Http2 => "http2",
            Self::Http3 => "http3",
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TransportCatalog {
    pub schema_version: u32,
    pub inspected_at: NaiveDate,
    pub transports: Vec<TransportProfile>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TransportProfile {
    pub id: String,
    pub family: String,
    pub implementation: String,
    pub role: StudyRole,
    pub source_url: String,
    pub source_revision: String,
    pub license: String,
    pub source_status: SourceStatus,
    pub language: String,
    pub layers: Vec<TransportLayer>,
    pub carriers: Vec<TransportCarrier>,
    pub primary_security: String,
    pub camouflage: String,
    pub strengths: Vec<String>,
    pub limitations: Vec<String>,
    pub code_paths: Vec<String>,
}

impl TransportCatalog {
    pub fn validate(&self) -> Result<(), ValidationError> {
        if self.schema_version != 1 {
            return Err(ValidationError::UnsupportedTransportCatalogSchema(
                self.schema_version,
            ));
        }
        if self.transports.is_empty() {
            return Err(ValidationError::EmptyTransportCatalog);
        }

        let mut ids = std::collections::BTreeSet::new();
        for transport in &self.transports {
            transport.validate()?;
            if !ids.insert(transport.id.as_str()) {
                return Err(ValidationError::DuplicateTransport(transport.id.clone()));
            }
        }
        Ok(())
    }
}

impl TransportProfile {
    pub fn validate(&self) -> Result<(), ValidationError> {
        if self.id.trim().is_empty() {
            return Err(ValidationError::EmptyTransportId);
        }
        if !self.source_url.starts_with("https://") {
            return Err(ValidationError::InvalidTransportSourceUrl(self.id.clone()));
        }
        if self.source_revision.len() != 40
            || !self
                .source_revision
                .bytes()
                .all(|byte| byte.is_ascii_hexdigit())
        {
            return Err(ValidationError::InvalidTransportRevision(self.id.clone()));
        }
        if self.layers.is_empty() || self.carriers.is_empty() {
            return Err(ValidationError::MissingTransportShape(self.id.clone()));
        }
        if self.strengths.is_empty() || self.limitations.is_empty() || self.code_paths.is_empty() {
            return Err(ValidationError::IncompleteTransportStudy(self.id.clone()));
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
    #[error("unsupported transport catalog schema version {0}")]
    UnsupportedTransportCatalogSchema(u32),
    #[error("transport catalog is empty")]
    EmptyTransportCatalog,
    #[error("transport id is empty")]
    EmptyTransportId,
    #[error("transport {0} source URL must use https")]
    InvalidTransportSourceUrl(String),
    #[error("transport {0} source revision must be a 40-character hexadecimal commit")]
    InvalidTransportRevision(String),
    #[error("transport {0} must declare at least one layer and carrier")]
    MissingTransportShape(String),
    #[error("transport {0} study must include strengths, limitations, and code paths")]
    IncompleteTransportStudy(String),
    #[error("duplicate transport id {0}")]
    DuplicateTransport(String),
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
