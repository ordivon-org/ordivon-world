use std::fs;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::time::Duration;

use anyhow::Result;
use chrono::Utc;
use link_model::{FailureClass, ProbeKind, ProbeProtocol};
use link_probe::{ProbeOptions, load_registry, run_probe};
use serde::Deserialize;
use tokio::process::Command;
use tokio::task::JoinSet;
use tokio::time::timeout;

use crate::model::{
    DnsSnapshot, HealthState, Ipv6Risk, LinkSnapshot, LocalRuntimeSnapshot, PathState,
    PrivacyStatus, ProviderSnapshot, RouteSnapshot, ServiceCheck, ServiceState,
};

const POWERSHELL: &str = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe";
const PUBLIC_ROUTE_TARGET: &str = "1.1.1.1";
const DEGRADED_SERVICE_LATENCY_MS: f64 = 8_000.0;
const MAX_WEB_TARGETS: usize = 32;

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

    pub async fn collect(&self) -> Result<LinkSnapshot> {
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
        let (ipv6_default_route, ipv6_tunnel_route, ipv6_risk) = classify_ipv6_route(
            ipv6_routes.as_deref(),
            effective_device.as_deref(),
            ipv4_tunnel_route,
        );

        let dns = observe_dns(Path::new("/etc/resolv.conf"));
        let local_runtime = LocalRuntimeSnapshot {
            cloudflare_tunnel_running: self.process_active("cloudflared").await,
            ordivon_mcp_running: self.systemd_active("ordivon-mcp.service").await,
        };
        let (services, service_error) = self.collect_services().await;

        let path_state =
            derive_path_state(&provider, effective_device.is_some(), ipv4_tunnel_route);
        let (mut health, mut reasons) = derive_health(path_state, &services);
        match ipv6_risk {
            Ipv6Risk::LatentPhysicalDefault => {
                ensure_degraded(&mut health);
                reasons.push("ipv6_physical_default_without_tunnel_route".to_owned());
            }
            Ipv6Risk::Unknown => {
                ensure_degraded(&mut health);
                reasons.push("ipv6_route_observation_unavailable".to_owned());
            }
            Ipv6Risk::NoneObserved | Ipv6Risk::TunnelCovered => {}
        }
        if let Some(error) = service_error {
            ensure_degraded(&mut health);
            reasons.push(error);
        }
        if services.is_empty() {
            ensure_degraded(&mut health);
            reasons.push("no_service_checks_available".to_owned());
        }
        reasons.sort();
        reasons.dedup();

        Ok(LinkSnapshot {
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
  $_.Name -match 'Surfshark' -or $_.InterfaceDescription -match 'Surfshark'
})
[pscustomobject]@{
  detected = ($services.Count -gt 0 -or $adapters.Count -gt 0)
  service_running = (@($services | Where-Object { $_.Status -eq 'Running' }).Count -gt 0)
  surfshark_adapter_up = (@($adapters | Where-Object { $_.Status -eq 'Up' }).Count -gt 0)
  wireguard_adapter_up = (@($adapters | Where-Object {
    $_.Status -eq 'Up' -and ($_.Name -match 'WireGuard' -or $_.InterfaceDescription -match 'WireGuard')
  }).Count -gt 0)
  openvpn_adapter_up = (@($adapters | Where-Object {
    $_.Status -eq 'Up' -and (
      $_.Name -match 'OpenVPN|TAP|Data Channel' -or
      $_.InterfaceDescription -match 'OpenVPN|TAP|Data Channel'
    )
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
        provider_snapshot(status)
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
        let targets: Vec<_> = registry
            .targets
            .into_iter()
            .filter(|target| target.enabled && target.protocols.contains(&ProbeProtocol::HttpTls))
            .collect();
        if targets.is_empty() {
            return (Vec::new(), Some("no_enabled_http_tls_targets".to_owned()));
        }
        if targets.len() > MAX_WEB_TARGETS {
            return (Vec::new(), Some("too_many_web_targets".to_owned()));
        }

        let mut tasks = JoinSet::new();
        for target in targets {
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
        let mut command = Command::new(program);
        command.args(args).kill_on_drop(true);
        let output = timeout(self.command_timeout, command.output())
            .await
            .ok()?
            .ok()?;
        if !output.status.success() {
            return None;
        }
        String::from_utf8(output.stdout).ok()
    }

    async fn process_active(&self, process: &str) -> Option<bool> {
        let mut command = Command::new("pgrep");
        command
            .args(["-x", process])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .kill_on_drop(true);
        timeout(self.command_timeout, command.status())
            .await
            .ok()?
            .ok()
            .map(|status| status.success())
    }

    async fn systemd_active(&self, unit: &str) -> Option<bool> {
        let mut command = Command::new("systemctl");
        command
            .args(["is-active", "--quiet", unit])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .kill_on_drop(true);
        timeout(self.command_timeout, command.status())
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
    surfshark_adapter_up: bool,
    wireguard_adapter_up: bool,
    openvpn_adapter_up: bool,
}

fn provider_snapshot(status: WindowsSurfsharkStatus) -> ProviderSnapshot {
    let protocol = if status.wireguard_adapter_up {
        Some("wireguard".to_owned())
    } else if status.openvpn_adapter_up {
        Some("openvpn".to_owned())
    } else if status.surfshark_adapter_up {
        Some("unknown".to_owned())
    } else {
        None
    };
    ProviderSnapshot {
        name: "surfshark".to_owned(),
        detected: status.detected,
        connected: status.service_running && status.surfshark_adapter_up,
        protocol,
    }
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

fn classify_ipv6_route(
    route_output: Option<&str>,
    effective_ipv4_device: Option<&str>,
    ipv4_tunnel_route: bool,
) -> (bool, bool, Ipv6Risk) {
    let Some(route_output) = route_output else {
        return (false, false, Ipv6Risk::Unknown);
    };
    let ipv6_default_device = parse_default_route_device(route_output);
    let ipv6_default_route = ipv6_default_device.is_some();
    let ipv6_tunnel_route = ipv6_default_device
        .as_deref()
        .zip(effective_ipv4_device)
        .is_some_and(|(ipv6, ipv4)| ipv6 == ipv4 && ipv4_tunnel_route);
    let risk = match (ipv6_default_route, ipv6_tunnel_route) {
        (false, _) => Ipv6Risk::NoneObserved,
        (true, true) => Ipv6Risk::TunnelCovered,
        (true, false) => Ipv6Risk::LatentPhysicalDefault,
    };
    (ipv6_default_route, ipv6_tunnel_route, risk)
}

fn ensure_degraded(health: &mut HealthState) {
    if *health == HealthState::Healthy {
        *health = HealthState::Degraded;
    }
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

fn service_check(result: link_model::ProbeResult) -> ServiceCheck {
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
    fn unavailable_ipv6_observation_is_not_reported_as_no_route() {
        assert_eq!(
            classify_ipv6_route(None, Some("eth3"), true),
            (false, false, Ipv6Risk::Unknown)
        );
        assert_eq!(
            classify_ipv6_route(Some(""), Some("eth3"), true),
            (false, false, Ipv6Risk::NoneObserved)
        );
    }

    #[tokio::test]
    async fn command_timeout_kills_the_child_process() {
        use std::fs;
        use std::time::Duration;

        let directory = tempfile::tempdir().expect("tempdir");
        let pid_path = directory.path().join("child.pid");
        let command = format!("echo $$ > '{}'; exec sleep 30", pid_path.display());
        let mut observer = SystemObserver::new(directory.path().join("targets.toml"));
        observer.command_timeout = Duration::from_millis(100);
        assert!(
            observer
                .command_output("/usr/bin/sh", &["-c", &command])
                .await
                .is_none()
        );
        tokio::time::sleep(Duration::from_millis(150)).await;
        let pid = fs::read_to_string(&pid_path).expect("pid");
        let status = std::process::Command::new("kill")
            .args(["-0", pid.trim()])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .status()
            .expect("kill check");
        assert!(!status.success(), "timed-out child still exists");
    }

    #[test]
    fn unrelated_wireguard_cannot_make_surfshark_connected() {
        let provider = provider_snapshot(WindowsSurfsharkStatus {
            detected: true,
            service_running: true,
            surfshark_adapter_up: false,
            wireguard_adapter_up: true,
            openvpn_adapter_up: false,
        });
        assert!(!provider.connected);
    }

    #[test]
    fn surfshark_protocol_classification_is_fail_closed() {
        let wireguard = provider_snapshot(WindowsSurfsharkStatus {
            detected: true,
            service_running: true,
            surfshark_adapter_up: true,
            wireguard_adapter_up: true,
            openvpn_adapter_up: false,
        });
        assert!(wireguard.connected);
        assert_eq!(wireguard.protocol.as_deref(), Some("wireguard"));

        let openvpn = provider_snapshot(WindowsSurfsharkStatus {
            detected: true,
            service_running: true,
            surfshark_adapter_up: true,
            wireguard_adapter_up: false,
            openvpn_adapter_up: true,
        });
        assert_eq!(openvpn.protocol.as_deref(), Some("openvpn"));

        let unknown = provider_snapshot(WindowsSurfsharkStatus {
            detected: true,
            service_running: true,
            surfshark_adapter_up: true,
            wireguard_adapter_up: false,
            openvpn_adapter_up: false,
        });
        assert!(unknown.connected);
        assert_eq!(unknown.protocol.as_deref(), Some("unknown"));
    }

    #[test]
    fn path_state_matrix_does_not_infer_a_tunnel() {
        let connected = ProviderSnapshot {
            name: "surfshark".to_owned(),
            detected: true,
            connected: true,
            protocol: Some("wireguard".to_owned()),
        };
        let disconnected = ProviderSnapshot {
            connected: false,
            protocol: None,
            ..connected.clone()
        };
        let unknown = ProviderSnapshot {
            detected: false,
            ..disconnected.clone()
        };
        assert_eq!(
            derive_path_state(&connected, false, false),
            PathState::Failed
        );
        assert_eq!(
            derive_path_state(&connected, true, false),
            PathState::Degraded
        );
        assert_eq!(
            derive_path_state(&connected, true, true),
            PathState::Tunneled
        );
        assert_eq!(
            derive_path_state(&disconnected, true, false),
            PathState::Direct
        );
        assert_eq!(derive_path_state(&unknown, true, false), PathState::Unknown);
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
