use std::fs;
use std::path::Path;
use std::process::Command;
use std::time::Duration;

use anyhow::{Context, Result};
use chrono::Utc;
use edge_model::{FailureClass, ProbeProtocol, ProbeResult, TargetConfig, TargetRegistry};
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

    if options.no_env_proxy {
        command.args(["--noproxy", "*"]);
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
            return ProbeResult {
                schema_version: 1,
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
                http_status: None,
                remote_ip: None,
                success: false,
                failure_class: Some(FailureClass::Tool),
                tool_exit_code: None,
                error: Some(error.to_string()),
            };
        }
    };

    let exit_code = output.status.code();
    let parsed = serde_json::from_slice::<Value>(&output.stdout).ok();
    let http_status = parsed.as_ref().and_then(extract_status);
    let success =
        output.status.success() && http_status.is_some_and(|status| (100..=599).contains(&status));
    let stderr = String::from_utf8_lossy(&output.stderr).trim().to_owned();

    ProbeResult {
        schema_version: 1,
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
        total_ms: parsed
            .as_ref()
            .and_then(|value| time_ms(value, "time_total")),
        http_status,
        remote_ip: parsed
            .as_ref()
            .and_then(|value| string_field(value, "remote_ip")),
        success,
        failure_class: (!success).then(|| classify_failure(exit_code, protocol, http_status)),
        tool_exit_code: exit_code,
        error: if stderr.is_empty() {
            None
        } else {
            Some(stderr)
        },
    }
}

fn extract_status(value: &Value) -> Option<u16> {
    value
        .get("response_code")
        .or_else(|| value.get("http_code"))
        .and_then(Value::as_u64)
        .and_then(|status| u16::try_from(status).ok())
}

fn string_field(value: &Value, key: &str) -> Option<String> {
    value
        .get(key)
        .and_then(Value::as_str)
        .filter(|text| !text.is_empty())
        .map(ToOwned::to_owned)
}

fn seconds(value: &Value, key: &str) -> Option<f64> {
    value.get(key).and_then(Value::as_f64)
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
}
