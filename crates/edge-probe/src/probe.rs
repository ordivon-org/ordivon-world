use std::fs;
use std::path::Path;
use std::process::Command;
use std::time::Duration;

use anyhow::{Context, Result};
use chrono::Utc;
use edge_model::{
    FailureClass, ProbeKind, ProbeProtocol, ProbeResult, ProbeTermination, TargetConfig,
    TargetRegistry,
};
use serde_json::Value;

const CURL_WRITE_OUT: &str = "%{json}";
const USER_AGENT: &str = "ordivon-edge-probe/0.1";

#[derive(Debug, Clone)]
pub struct ProbeOptions {
    pub network: String,
    pub route: String,
    pub timeout: Duration,
    pub no_env_proxy: bool,
    pub curl_bin: String,
    pub probe_kind: ProbeKind,
    pub collection_id: String,
    pub sample_index: u32,
    pub requested_duration: Option<Duration>,
    pub rate_limit_bytes_per_second: Option<u64>,
}

#[derive(Debug, Clone, Copy)]
struct ProbeFacts {
    exit_code: Option<i32>,
    protocol: ProbeProtocol,
    http_status: Option<u16>,
    total_ms: Option<f64>,
    requested_duration_ms: Option<u64>,
    bytes_downloaded: Option<u64>,
    connection_count: Option<u32>,
}

impl ProbeFacts {
    fn status_ok(self) -> bool {
        self.http_status
            .is_some_and(|status| (100..=599).contains(&status))
    }

    fn reached_duration(self) -> bool {
        self.total_ms
            .zip(self.requested_duration_ms)
            .is_some_and(|(observed, requested)| observed >= requested as f64 * 0.95)
    }
}

pub fn load_registry(path: &Path) -> Result<TargetRegistry> {
    let raw = fs::read_to_string(path)
        .with_context(|| format!("failed to read target registry {}", path.display()))?;
    let registry: TargetRegistry = toml::from_str(&raw)
        .with_context(|| format!("failed to parse target registry {}", path.display()))?;
    registry.validate().context("invalid target registry")?;
    Ok(registry)
}

pub fn run_probe(
    target: &TargetConfig,
    protocol: ProbeProtocol,
    options: &ProbeOptions,
) -> ProbeResult {
    let started_at = Utc::now();
    let timeout_seconds = options.timeout.as_secs().max(1).to_string();
    let connect_timeout_seconds = options.timeout.as_secs().clamp(1, 10).to_string();

    let mut command = Command::new(&options.curl_bin);
    command.args([
        "--disable",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--max-time",
        &timeout_seconds,
        "--connect-timeout",
        &connect_timeout_seconds,
        "--user-agent",
        USER_AGENT,
        "--write-out",
        CURL_WRITE_OUT,
    ]);

    if options.probe_kind == ProbeKind::Reachability {
        command.arg("--head");
    }

    if options.no_env_proxy {
        command.args(["--noproxy", "*"]);
    }

    if let Some(rate_limit) = options.rate_limit_bytes_per_second {
        command.args(["--limit-rate", &rate_limit.to_string()]);
    }

    match protocol {
        ProbeProtocol::HttpTls => {
            command.arg("--http1.1");
        }
        ProbeProtocol::Quic => {
            command.arg("--http3-only");
        }
    }

    command.arg(&target.url);

    let output = match command.output() {
        Ok(output) => output,
        Err(error) => {
            return tool_failure(target, protocol, options, started_at, error.to_string());
        }
    };

    let exit_code = output.status.code();
    let parsed = serde_json::from_slice::<Value>(&output.stdout).ok();
    let http_status = parsed.as_ref().and_then(extract_status);
    let total_ms = parsed
        .as_ref()
        .and_then(|value| time_ms(value, "time_total"));
    let bytes_downloaded = parsed
        .as_ref()
        .and_then(|value| integer_field(value, "size_download"));
    let connection_count = parsed
        .as_ref()
        .and_then(|value| integer_field(value, "num_connects"))
        .and_then(|value| u32::try_from(value).ok());
    let requested_duration_ms = options.requested_duration.map(duration_ms);
    let facts = ProbeFacts {
        exit_code,
        protocol,
        http_status,
        total_ms,
        requested_duration_ms,
        bytes_downloaded,
        connection_count,
    };
    let success = probe_succeeded(options.probe_kind, facts);
    let stderr = String::from_utf8_lossy(&output.stderr).trim().to_owned();
    let termination = if success {
        if options.probe_kind == ProbeKind::ConnectionLifetime && exit_code == Some(28) {
            ProbeTermination::DeadlineReached
        } else {
            ProbeTermination::Completed
        }
    } else {
        ProbeTermination::Failed
    };
    let failure_class = (!success).then(|| classify_probe_failure(options.probe_kind, facts));

    ProbeResult {
        schema_version: 1,
        probe_kind: options.probe_kind,
        collection_id: Some(options.collection_id.clone()),
        sample_index: Some(options.sample_index),
        target: target.id.clone(),
        url: target.url.clone(),
        network: options.network.clone(),
        route: options.route.clone(),
        protocol,
        started_at,
        dns_ms: parsed
            .as_ref()
            .and_then(|value| time_ms(value, "time_namelookup")),
        connect_ms: parsed.as_ref().and_then(connect_phase_ms),
        tls_ms: parsed.as_ref().and_then(tls_phase_ms),
        ttfb_ms: parsed
            .as_ref()
            .and_then(|value| time_ms(value, "time_starttransfer")),
        total_ms,
        requested_duration_ms,
        bytes_downloaded,
        speed_download_bps: parsed
            .as_ref()
            .and_then(|value| number_field(value, "speed_download")),
        connection_count,
        http_version: parsed
            .as_ref()
            .and_then(|value| string_field(value, "http_version")),
        http_status,
        remote_ip: parsed
            .as_ref()
            .and_then(|value| string_field(value, "remote_ip")),
        success,
        failure_class,
        termination: Some(termination),
        tool_exit_code: exit_code,
        error: if success || stderr.is_empty() {
            None
        } else {
            Some(stderr)
        },
    }
}

fn tool_failure(
    target: &TargetConfig,
    protocol: ProbeProtocol,
    options: &ProbeOptions,
    started_at: chrono::DateTime<Utc>,
    error: String,
) -> ProbeResult {
    ProbeResult {
        schema_version: 1,
        probe_kind: options.probe_kind,
        collection_id: Some(options.collection_id.clone()),
        sample_index: Some(options.sample_index),
        target: target.id.clone(),
        url: target.url.clone(),
        network: options.network.clone(),
        route: options.route.clone(),
        protocol,
        started_at,
        dns_ms: None,
        connect_ms: None,
        tls_ms: None,
        ttfb_ms: None,
        total_ms: None,
        requested_duration_ms: options.requested_duration.map(duration_ms),
        bytes_downloaded: None,
        speed_download_bps: None,
        connection_count: None,
        http_version: None,
        http_status: None,
        remote_ip: None,
        success: false,
        failure_class: Some(FailureClass::Tool),
        termination: Some(ProbeTermination::Failed),
        tool_exit_code: None,
        error: Some(error),
    }
}

fn duration_ms(duration: Duration) -> u64 {
    u64::try_from(duration.as_millis()).unwrap_or(u64::MAX)
}

fn probe_succeeded(probe_kind: ProbeKind, facts: ProbeFacts) -> bool {
    match probe_kind {
        ProbeKind::Reachability => facts.exit_code == Some(0) && facts.status_ok(),
        ProbeKind::Transfer => {
            facts.exit_code == Some(0)
                && facts.status_ok()
                && facts.bytes_downloaded.is_some_and(|bytes| bytes > 0)
        }
        ProbeKind::ConnectionLifetime => {
            matches!(facts.exit_code, Some(0 | 28))
                && facts.status_ok()
                && facts.reached_duration()
                && facts.bytes_downloaded.is_some_and(|bytes| bytes > 0)
                && facts.connection_count == Some(1)
        }
    }
}

fn classify_probe_failure(probe_kind: ProbeKind, facts: ProbeFacts) -> FailureClass {
    match probe_kind {
        ProbeKind::Transfer
            if facts.exit_code == Some(0)
                && facts.status_ok()
                && facts.bytes_downloaded.is_none_or(|bytes| bytes == 0) =>
        {
            FailureClass::Transfer
        }
        ProbeKind::ConnectionLifetime
            if facts.status_ok()
                && (facts.connection_count != Some(1) || !facts.reached_duration()) =>
        {
            FailureClass::ConnectionLifetime
        }
        _ => classify_failure(facts.exit_code, facts.protocol, facts.http_status),
    }
}

fn extract_status(value: &Value) -> Option<u16> {
    value
        .get("response_code")
        .or_else(|| value.get("http_code"))
        .and_then(Value::as_u64)
        .and_then(|status| u16::try_from(status).ok())
}

fn number_field(value: &Value, key: &str) -> Option<f64> {
    value.get(key).and_then(Value::as_f64)
}

fn integer_field(value: &Value, key: &str) -> Option<u64> {
    value.get(key).and_then(|number| {
        number
            .as_u64()
            .or_else(|| number.as_f64().map(|value| value as u64))
    })
}

fn string_field(value: &Value, key: &str) -> Option<String> {
    value
        .get(key)
        .and_then(Value::as_str)
        .filter(|text| !text.is_empty())
        .map(ToOwned::to_owned)
}

fn seconds(value: &Value, key: &str) -> Option<f64> {
    number_field(value, key)
}

fn time_ms(value: &Value, key: &str) -> Option<f64> {
    seconds(value, key).map(|seconds| seconds * 1000.0)
}

fn phase_ms(value: &Value, end: &str, start: &str) -> Option<f64> {
    let end = seconds(value, end)?;
    let start = seconds(value, start)?;
    Some(((end - start).max(0.0)) * 1000.0)
}

fn connect_phase_ms(value: &Value) -> Option<f64> {
    phase_ms(value, "time_connect", "time_namelookup")
}

fn tls_phase_ms(value: &Value) -> Option<f64> {
    phase_ms(value, "time_appconnect", "time_connect")
}

pub fn classify_failure(
    exit_code: Option<i32>,
    protocol: ProbeProtocol,
    http_status: Option<u16>,
) -> FailureClass {
    match exit_code {
        Some(5 | 6) => FailureClass::Dns,
        Some(7) => match protocol {
            ProbeProtocol::HttpTls => FailureClass::TcpConnect,
            ProbeProtocol::Quic => FailureClass::QuicHandshake,
        },
        Some(28) => FailureClass::Timeout,
        Some(35 | 51 | 53 | 58 | 59 | 60 | 64 | 66 | 77 | 80 | 82 | 83 | 90 | 91) => match protocol
        {
            ProbeProtocol::HttpTls => FailureClass::TlsHandshake,
            ProbeProtocol::Quic => FailureClass::QuicHandshake,
        },
        Some(16 | 22 | 33 | 47 | 52 | 56 | 61 | 92) => FailureClass::Http,
        Some(95 | 96) => FailureClass::QuicHandshake,
        Some(_) if http_status.is_none() => match protocol {
            ProbeProtocol::HttpTls => FailureClass::Unknown,
            ProbeProtocol::Quic => FailureClass::QuicHandshake,
        },
        Some(_) => FailureClass::Http,
        None => FailureClass::Tool,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn failure_classification_distinguishes_quic() {
        assert_eq!(
            classify_failure(Some(35), ProbeProtocol::Quic, None),
            FailureClass::QuicHandshake
        );
        assert_eq!(
            classify_failure(Some(35), ProbeProtocol::HttpTls, None),
            FailureClass::TlsHandshake
        );
        assert_eq!(
            classify_failure(Some(7), ProbeProtocol::Quic, None),
            FailureClass::QuicHandshake
        );
    }

    fn lifetime_facts(connection_count: u32) -> ProbeFacts {
        ProbeFacts {
            exit_code: Some(28),
            protocol: ProbeProtocol::HttpTls,
            http_status: Some(200),
            total_ms: Some(5_001.0),
            requested_duration_ms: Some(5_000),
            bytes_downloaded: Some(320_000),
            connection_count: Some(connection_count),
        }
    }

    #[test]
    fn lifetime_deadline_is_expected_success() {
        assert!(probe_succeeded(
            ProbeKind::ConnectionLifetime,
            lifetime_facts(1),
        ));
    }

    #[test]
    fn lifetime_requires_one_continuous_connection() {
        assert!(!probe_succeeded(
            ProbeKind::ConnectionLifetime,
            lifetime_facts(2),
        ));
    }
}
