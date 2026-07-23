use std::fs;
use std::path::{Path, PathBuf};
use std::time::Duration;

use anyhow::Result;
use chrono::Utc;
use edge_model::{FailureClass, ProbeKind, ProbeProtocol};
use edge_probe::{ProbeOptions, load_registry, run_probe};
use serde::Deserialize;
use tokio::process::Command;
use tokio::task::JoinSet;
use tokio::time::timeout;

use crate::model::{
    DnsSnapshot, EdgeSnapshot, HealthState, Ipv6Risk, LocalRuntimeSnapshot, PathState,
    PrivacyStatus, ProviderSnapshot, RouteSnapshot, ServiceCheck, ServiceState,
};

const POWERSHELL: &str = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe";
const PUBLIC_ROUTE_TARGET: &str = "1.1.1.1";
const DEGRADED_SERVICE_LATENCY_MS: f64 = 8_000.0;

#[derive(Debug, Clone)]
pub struct SystemObserver {
    targets_path: PathBuf,
    curl_bin: String,
    command_timeout: Duration,
    probe_timeout: Duration,
}

impl SystemObserver {
    pub fn new(targets_path: impl Into<PathBuf>) -> Self {
        Self {
            targets_path: targets_path.into(),
            curl_bin: "curl".to_owned(),
            command_timeout: Duration::from_secs(5),
            probe_timeout: Duration::from_secs(10),
        }
    }

    pub fn with_curl_bin(mut self, curl_bin: impl Into<String>) -> Self {
        self.curl_bin = curl_bin.into();
        self
    }

    pub async fn collect(&self) -> Result<EdgeSnapshot> {
        let provider = self.observe_surfshark().await;
        let route_get = self
            .command_output("ip", &["route", "get", PUBLIC_ROUTE_TARGET])
            .await;
        let route_table = self.command_output("ip", &["route", "show"]).await;
        let effective_device = route_get.as_deref().and_then(parse_route_device);
        let has_split_tunnel = effective_device
            .as_deref()
            .is_some_and(|device| has_ipv4_split_tunnel(route_table.as_deref(), device));
        let ipv4_tunnel_route = provider.connected && has_split_tunnel;
        let interface_class = match (&effective_device, ipv4_tunnel_route) {
            (Some(_), true) => "tunnel",
            (Some(_), false) => "physical",
            (None, _) => "unknown",
        }
        .to_owned();

        let mtu = if let Some(device) = effective_device.as_deref() {
            self.command_output("ip", &["-o", "link", "show", "dev", device])
                .await
                .as_deref()
                .and_then(parse_mtu)
        } else {
            None
        };

        let ipv6_routes = self
            .command_output("ip", &["-6", "route", "show", "default"])
            .await;
        let ipv6_default_device = ipv6_routes.as_deref().and_then(parse_default_route_device);
        let ipv6_default_route = ipv6_default_device.is_some();
        let ipv6_tunnel_route = ipv6_default_device
            .as_deref()
            .zip(effective_device.as_deref())
            .is_some_and(|(ipv6, ipv4)| ipv6 == ipv4 && ipv4_tunnel_route);
        let ipv6_risk = match (ipv6_default_route, ipv6_tunnel_route) {
            (false, _) => Ipv6Risk::NoneObserved,
            (true, true) => Ipv6Risk::TunnelCovered,
            (true, false) => Ipv6Risk::LatentPhysicalDefault,
        };

        let dns = observe_dns(Path::new("/etc/resolv.conf"));
        let local_runtime = LocalRuntimeSnapshot {
            cloudflare_tunnel_running: self.process_active("cloudflared").await,
            ordivon_mcp_running: self.systemd_active("ordivon-mcp.service").await,
        };
        let (services, service_error) = self.collect_services().await;

        let path_state =
            derive_path_state(&provider, effective_device.is_some(), ipv4_tunnel_route);
        let (health, mut reasons) = derive_health(path_state, &services);
        if ipv6_risk == Ipv6Risk::LatentPhysicalDefault {
            reasons.push("ipv6_physical_default_without_tunnel_route".to_owned());
        }
        if let Some(error) = service_error {
            reasons.push(error);
        }
        reasons.sort();
        reasons.dedup();

        Ok(EdgeSnapshot {
            schema_version: 1,
            observed_at: Utc::now(),
            health,
            path_state,
            provider,
            route: RouteSnapshot {
                effective_interface_class: interface_class,
                ipv4_tunnel_route,
                mtu,
                ipv6_default_route,
                ipv6_tunnel_route,
                ipv6_risk,
            },
            dns,
            local_runtime,
            services,
            reasons,
            privacy: PrivacyStatus {
                sensitive_fields_redacted: true,
                network_binding: "loopback_only".to_owned(),
                raw_command_output_retained: false,
            },
        })
    }

    async fn observe_surfshark(&self) -> ProviderSnapshot {
        if !Path::new(POWERSHELL).exists() {
            return unknown_provider();
        }
        let script = r#"
$services = @(Get-Service -ErrorAction SilentlyContinue | Where-Object {
  $_.Name -match 'Surfshark' -or $_.DisplayName -match 'Surfshark'
})
$adapters = @(Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object {
  $_.Name -match 'Surfshark|WireGuard|OpenVPN' -or
  $_.InterfaceDescription -match 'Surfshark|WireGuard|OpenVPN'
})
[pscustomobject]@{
  detected = ($services.Count -gt 0 -or $adapters.Count -gt 0)
  service_running = (@($services | Where-Object { $_.Status -eq 'Running' }).Count -gt 0)
  wireguard_adapter_up = (@($adapters | Where-Object {
    $_.Status -eq 'Up' -and ($_.Name -match 'WireGuard' -or $_.InterfaceDescription -match 'WireGuard')
  }).Count -gt 0)
  openvpn_adapter_up = (@($adapters | Where-Object {
    $_.Status -eq 'Up' -and ($_.Name -match 'OpenVPN' -or $_.InterfaceDescription -match 'OpenVPN')
  }).Count -gt 0)
} | ConvertTo-Json -Compress
"#;
        let Some(raw) = self
            .command_output(
                POWERSHELL,
                &["-NoProfile", "-NonInteractive", "-Command", script],
            )
            .await
        else {
            return unknown_provider();
        };
        let Ok(status) = serde_json::from_str::<WindowsSurfsharkStatus>(raw.trim()) else {
            return unknown_provider();
        };
        let protocol = if status.wireguard_adapter_up {
            Some("wireguard".to_owned())
        } else if status.openvpn_adapter_up {
            Some("openvpn".to_owned())
        } else {
            None
        };
        ProviderSnapshot {
            name: "surfshark".to_owned(),
            detected: status.detected,
            connected: status.service_running
                && (status.wireguard_adapter_up || status.openvpn_adapter_up),
            protocol,
        }
    }

    async fn collect_services(&self) -> (Vec<ServiceCheck>, Option<String>) {
        let registry = match load_registry(&self.targets_path) {
            Ok(registry) => registry,
            Err(_) => return (Vec::new(), Some("service_registry_unavailable".to_owned())),
        };
        let collection_id = format!("edge-web-{}", Utc::now().format("%Y%m%dT%H%M%SZ"));
        let options = ProbeOptions {
            network: "wsl-current".to_owned(),
            route: "host-current".to_owned(),
            timeout: self.probe_timeout,
            no_env_proxy: true,
            curl_bin: self.curl_bin.clone(),
            probe_kind: ProbeKind::Reachability,
            collection_id,
            sample_index: 1,
            requested_duration: None,
            rate_limit_bytes_per_second: None,
        };
        let mut tasks = JoinSet::new();
        for target in registry.targets.into_iter().filter(|target| target.enabled) {
            if !target.protocols.contains(&ProbeProtocol::HttpTls) {
                continue;
            }
            let options = options.clone();
            tasks.spawn_blocking(move || run_probe(&target, ProbeProtocol::HttpTls, &options));
        }

        let mut checks = Vec::new();
        while let Some(result) = tasks.join_next().await {
            match result {
                Ok(result) => checks.push(service_check(result)),
                Err(_) => checks.push(ServiceCheck {
                    id: "probe-worker".to_owned(),
                    state: ServiceState::Failed,
                    latency_ms: None,
                    failure_class: Some("tool".to_owned()),
                }),
            }
        }
        checks.sort_by(|left, right| left.id.cmp(&right.id));
        (checks, None)
    }

    async fn command_output(&self, program: &str, args: &[&str]) -> Option<String> {
        let child = Command::new(program).args(args).output();
        let output = timeout(self.command_timeout, child).await.ok()?.ok()?;
        if !output.status.success() {
            return None;
        }
        String::from_utf8(output.stdout).ok()
    }

    async fn process_active(&self, process: &str) -> Option<bool> {
        let status = Command::new("pgrep").args(["-x", process]).status();
        timeout(self.command_timeout, status)
            .await
            .ok()?
            .ok()
            .map(|status| status.success())
    }

    async fn systemd_active(&self, unit: &str) -> Option<bool> {
        let status = Command::new("systemctl")
            .args(["is-active", "--quiet", unit])
            .status();
        timeout(self.command_timeout, status)
            .await
            .ok()?
            .ok()
            .map(|status| status.success())
    }
}

#[derive(Debug, Deserialize)]
struct WindowsSurfsharkStatus {
    detected: bool,
    service_running: bool,
    wireguard_adapter_up: bool,
    openvpn_adapter_up: bool,
}

fn unknown_provider() -> ProviderSnapshot {
    ProviderSnapshot {
        name: "surfshark".to_owned(),
        detected: false,
        connected: false,
        protocol: None,
    }
}

fn observe_dns(path: &Path) -> DnsSnapshot {
    let raw = fs::read_to_string(path).unwrap_or_default();
    let resolvers: Vec<&str> = raw
        .lines()
        .filter_map(|line| line.strip_prefix("nameserver "))
        .map(str::trim)
        .filter(|value| !value.is_empty())
        .collect();
    let mode = if resolvers.contains(&"10.255.255.254") {
        "wsl_dns_tunneling"
    } else if resolvers
        .iter()
        .all(|resolver| resolver.starts_with("127."))
        && !resolvers.is_empty()
    {
        "local_resolver"
    } else if resolvers.is_empty() {
        "unknown"
    } else {
        "custom_resolver"
    };
    DnsSnapshot {
        mode: mode.to_owned(),
        resolver_count: resolvers.len(),
    }
}

fn parse_route_device(output: &str) -> Option<String> {
    let mut fields = output.split_whitespace();
    while let Some(field) = fields.next() {
        if field == "dev" {
            return fields.next().map(ToOwned::to_owned);
        }
    }
    None
}

fn parse_default_route_device(output: &str) -> Option<String> {
    output
        .lines()
        .find(|line| line.split_whitespace().next() == Some("default"))
        .and_then(parse_route_device)
}

fn has_ipv4_split_tunnel(route_table: Option<&str>, device: &str) -> bool {
    let Some(route_table) = route_table else {
        return false;
    };
    let first = route_table.lines().any(|line| {
        line.starts_with("0.0.0.0/1 ") && parse_route_device(line).as_deref() == Some(device)
    });
    let second = route_table.lines().any(|line| {
        line.starts_with("128.0.0.0/1 ") && parse_route_device(line).as_deref() == Some(device)
    });
    first && second
}

fn parse_mtu(output: &str) -> Option<u32> {
    let mut fields = output.split_whitespace();
    while let Some(field) = fields.next() {
        if field == "mtu" {
            return fields.next()?.parse().ok();
        }
    }
    None
}

fn derive_path_state(
    provider: &ProviderSnapshot,
    route_present: bool,
    ipv4_tunnel_route: bool,
) -> PathState {
    match (
        provider.detected,
        provider.connected,
        route_present,
        ipv4_tunnel_route,
    ) {
        (_, _, false, _) => PathState::Failed,
        (_, true, true, true) => PathState::Tunneled,
        (_, true, true, false) => PathState::Degraded,
        (true, false, true, _) => PathState::Direct,
        (false, false, true, _) => PathState::Unknown,
    }
}

fn derive_health(path_state: PathState, services: &[ServiceCheck]) -> (HealthState, Vec<String>) {
    let mut reasons = Vec::new();
    let failed = services
        .iter()
        .filter(|service| service.state == ServiceState::Failed)
        .count();
    let degraded = services
        .iter()
        .filter(|service| service.state == ServiceState::Degraded)
        .count();

    let health = match path_state {
        PathState::Failed => {
            reasons.push("no_public_route".to_owned());
            HealthState::Failed
        }
        PathState::Degraded => {
            reasons.push("provider_connected_without_verified_tunnel_route".to_owned());
            HealthState::Degraded
        }
        PathState::Direct => {
            reasons.push("surfshark_not_connected".to_owned());
            HealthState::Degraded
        }
        PathState::Unknown => {
            reasons.push("provider_state_unknown".to_owned());
            HealthState::Unknown
        }
        PathState::Tunneled if !services.is_empty() && failed * 2 >= services.len() => {
            reasons.push("multiple_critical_services_failed".to_owned());
            HealthState::Failed
        }
        PathState::Tunneled if failed > 0 || degraded > 0 => {
            reasons.push("one_or_more_services_degraded".to_owned());
            HealthState::Degraded
        }
        PathState::Tunneled => HealthState::Healthy,
    };
    (health, reasons)
}

fn service_check(result: edge_model::ProbeResult) -> ServiceCheck {
    let state = if !result.success {
        ServiceState::Failed
    } else if result
        .total_ms
        .is_some_and(|latency| latency >= DEGRADED_SERVICE_LATENCY_MS)
    {
        ServiceState::Degraded
    } else {
        ServiceState::Healthy
    };
    ServiceCheck {
        id: result.target,
        state,
        latency_ms: result.total_ms,
        failure_class: result.failure_class.and_then(failure_class_name),
    }
}

fn failure_class_name(class: FailureClass) -> Option<String> {
    serde_json::to_value(class)
        .ok()?
        .as_str()
        .map(ToOwned::to_owned)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_route_and_mtu_without_retaining_addresses() {
        assert_eq!(
            parse_route_device("1.1.1.1 dev eth3 src 10.14.0.2 uid 0"),
            Some("eth3".to_owned())
        );
        assert_eq!(
            parse_mtu("20: eth3: <UP> mtu 1380 qdisc mq state UP"),
            Some(1380)
        );
    }

    #[test]
    fn split_tunnel_requires_both_halves_on_same_device() {
        let routes = "0.0.0.0/1 dev eth3 metric 5\n128.0.0.0/1 dev eth3 metric 5\ndefault via 192.168.0.1 dev eth0";
        assert!(has_ipv4_split_tunnel(Some(routes), "eth3"));
        assert!(!has_ipv4_split_tunnel(Some(routes), "eth0"));
    }

    #[test]
    fn direct_path_is_degraded_when_surfshark_is_detected() {
        let provider = ProviderSnapshot {
            name: "surfshark".to_owned(),
            detected: true,
            connected: false,
            protocol: None,
        };
        assert_eq!(derive_path_state(&provider, true, false), PathState::Direct);
        assert_eq!(
            derive_health(PathState::Direct, &[]).0,
            HealthState::Degraded
        );
    }
}
