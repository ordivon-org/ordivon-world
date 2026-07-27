use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum HealthState {
    Healthy,
    Degraded,
    Failed,
    Unknown,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum PathState {
    Unknown,
    Direct,
    Tunneled,
    Degraded,
    Failed,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ServiceState {
    Healthy,
    Degraded,
    Failed,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Ipv6Risk {
    NoneObserved,
    LatentPhysicalDefault,
    TunnelCovered,
    Unknown,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ProviderSnapshot {
    pub name: String,
    pub detected: bool,
    pub connected: bool,
    pub protocol: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct RouteSnapshot {
    pub effective_interface_class: String,
    pub ipv4_tunnel_route: bool,
    pub mtu: Option<u32>,
    pub ipv6_default_route: bool,
    pub ipv6_tunnel_route: bool,
    pub ipv6_risk: Ipv6Risk,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct DnsSnapshot {
    pub mode: String,
    pub resolver_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct LocalRuntimeSnapshot {
    pub cloudflare_tunnel_running: Option<bool>,
    pub ordivon_mcp_running: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct ServiceCheck {
    pub id: String,
    pub state: ServiceState,
    pub latency_ms: Option<f64>,
    pub failure_class: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct PrivacyStatus {
    pub sensitive_fields_redacted: bool,
    pub network_binding: String,
    pub raw_command_output_retained: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct EdgeSnapshot {
    pub schema_version: u32,
    pub observed_at: DateTime<Utc>,
    pub health: HealthState,
    pub path_state: PathState,
    pub provider: ProviderSnapshot,
    pub route: RouteSnapshot,
    pub dns: DnsSnapshot,
    pub local_runtime: LocalRuntimeSnapshot,
    pub services: Vec<ServiceCheck>,
    pub reasons: Vec<String>,
    pub privacy: PrivacyStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct EdgeEvent {
    pub id: i64,
    pub observed_at: DateTime<Utc>,
    pub kind: String,
    pub severity: String,
    pub summary: String,
}
