use std::collections::BTreeMap;

use anyhow::Result;
use edge_model::{ProbeKind, ProbeProtocol, ProbeResult};
use serde::Serialize;

#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct ProbeSummary {
    pub probe_kind: ProbeKind,
    pub network: String,
    pub route: String,
    pub protocol: ProbeProtocol,
    pub target: String,
    pub samples: usize,
    pub successes: usize,
    pub success_rate: f64,
    pub p50_total_ms: Option<f64>,
    pub p95_total_ms: Option<f64>,
    pub p50_bytes_downloaded: Option<f64>,
    pub p50_speed_download_bps: Option<f64>,
}

pub fn summarize(results: &[ProbeResult]) -> Vec<ProbeSummary> {
    type Key = (ProbeKind, String, String, ProbeProtocol, String);
    let mut groups: BTreeMap<Key, Vec<&ProbeResult>> = BTreeMap::new();
    for result in results {
        groups
            .entry((
                result.probe_kind,
                result.network.clone(),
                result.route.clone(),
                result.protocol,
                result.target.clone(),
            ))
            .or_default()
            .push(result);
    }

    groups
        .into_iter()
        .map(
            |((probe_kind, network, route, protocol, target), samples)| {
                let successes = samples.iter().filter(|sample| sample.success).count();
                let mut totals = successful_values(&samples, |sample| sample.total_ms);
                let mut bytes = if probe_kind == ProbeKind::Reachability {
                    Vec::new()
                } else {
                    successful_values(&samples, |sample| {
                        sample.bytes_downloaded.map(|value| value as f64)
                    })
                };
                let mut speeds = if probe_kind == ProbeKind::Reachability {
                    Vec::new()
                } else {
                    successful_values(&samples, |sample| sample.speed_download_bps)
                };
                totals.sort_by(f64::total_cmp);
                bytes.sort_by(f64::total_cmp);
                speeds.sort_by(f64::total_cmp);

                ProbeSummary {
                    probe_kind,
                    network,
                    route,
                    protocol,
                    target,
                    samples: samples.len(),
                    successes,
                    success_rate: successes as f64 / samples.len() as f64,
                    p50_total_ms: percentile(&totals, 0.50),
                    p95_total_ms: percentile(&totals, 0.95),
                    p50_bytes_downloaded: percentile(&bytes, 0.50),
                    p50_speed_download_bps: percentile(&speeds, 0.50),
                }
            },
        )
        .collect()
}

fn successful_values(
    samples: &[&ProbeResult],
    value: impl Fn(&ProbeResult) -> Option<f64>,
) -> Vec<f64> {
    samples
        .iter()
        .filter(|sample| sample.success)
        .filter_map(|sample| value(sample))
        .collect()
}

pub fn percentile(sorted_values: &[f64], percentile: f64) -> Option<f64> {
    if sorted_values.is_empty() {
        return None;
    }
    let rank = (percentile * sorted_values.len() as f64).ceil() as usize;
    Some(sorted_values[rank.saturating_sub(1).min(sorted_values.len() - 1)])
}

pub fn summaries_json(summaries: &[ProbeSummary]) -> Result<String> {
    Ok(serde_json::to_string_pretty(summaries)?)
}

pub fn summaries_markdown(summaries: &[ProbeSummary]) -> String {
    let mut output = String::from(
        "# Ordivon Edge probe report\n\n| Kind | Network | Route | Protocol | Target | Samples | Success | P50 total | P95 total | P50 bytes | P50 speed |\n|---|---|---|---|---|---:|---:|---:|---:|---:|---:|\n",
    );
    for summary in summaries {
        output.push_str(&format!(
            "| {} | {} | {} | {} | {} | {} | {:.1}% | {} | {} | {} | {} |\n",
            summary.probe_kind,
            summary.network,
            summary.route,
            summary.protocol,
            summary.target,
            summary.samples,
            summary.success_rate * 100.0,
            format_ms(summary.p50_total_ms),
            format_ms(summary.p95_total_ms),
            format_bytes(summary.p50_bytes_downloaded),
            format_speed(summary.p50_speed_download_bps),
        ));
    }
    output
}

fn format_ms(value: Option<f64>) -> String {
    value.map_or_else(|| "—".to_owned(), |value| format!("{value:.1} ms"))
}

fn format_bytes(value: Option<f64>) -> String {
    value.map_or_else(
        || "—".to_owned(),
        |value| {
            if value >= 1024.0 * 1024.0 {
                format!("{:.2} MiB", value / 1024.0 / 1024.0)
            } else if value >= 1024.0 {
                format!("{:.1} KiB", value / 1024.0)
            } else {
                format!("{value:.0} B")
            }
        },
    )
}

fn format_speed(value: Option<f64>) -> String {
    value.map_or_else(
        || "—".to_owned(),
        |value| {
            if value >= 1024.0 * 1024.0 {
                format!("{:.2} MiB/s", value / 1024.0 / 1024.0)
            } else if value >= 1024.0 {
                format!("{:.1} KiB/s", value / 1024.0)
            } else {
                format!("{value:.0} B/s")
            }
        },
    )
}

#[cfg(test)]
mod tests {
    use chrono::Utc;
    use edge_model::{FailureClass, ProbeTermination};

    use super::*;

    fn result(kind: ProbeKind, success: bool, total_ms: Option<f64>) -> ProbeResult {
        ProbeResult {
            schema_version: 1,
            probe_kind: kind,
            collection_id: Some("test-collection".into()),
            sample_index: Some(1),
            target: "github".into(),
            url: "https://github.com/".into(),
            network: "test".into(),
            route: "direct-process".into(),
            protocol: ProbeProtocol::HttpTls,
            started_at: Utc::now(),
            dns_ms: Some(1.0),
            connect_ms: Some(2.0),
            tls_ms: Some(3.0),
            ttfb_ms: total_ms,
            total_ms,
            requested_duration_ms: None,
            bytes_downloaded: success.then_some(1024),
            speed_download_bps: success.then_some(512.0),
            connection_count: success.then_some(1),
            http_version: success.then(|| "1.1".into()),
            http_status: success.then_some(200),
            remote_ip: None,
            success,
            failure_class: (!success).then_some(FailureClass::Timeout),
            termination: Some(if success {
                ProbeTermination::Completed
            } else {
                ProbeTermination::Failed
            }),
            tool_exit_code: Some(if success { 0 } else { 28 }),
            error: None,
        }
    }

    #[test]
    fn percentile_uses_nearest_rank() {
        let values = [10.0, 20.0, 30.0, 40.0];
        assert_eq!(percentile(&values, 0.50), Some(20.0));
        assert_eq!(percentile(&values, 0.95), Some(40.0));
    }

    #[test]
    fn summary_counts_failures_but_metrics_successes_only() {
        let summaries = summarize(&[
            result(ProbeKind::Transfer, true, Some(10.0)),
            result(ProbeKind::Transfer, false, None),
        ]);
        assert_eq!(summaries.len(), 1);
        assert_eq!(summaries[0].samples, 2);
        assert_eq!(summaries[0].successes, 1);
        assert_eq!(summaries[0].success_rate, 0.5);
        assert_eq!(summaries[0].p50_total_ms, Some(10.0));
        assert_eq!(summaries[0].p50_bytes_downloaded, Some(1024.0));
    }

    #[test]
    fn summary_separates_probe_kinds() {
        let summaries = summarize(&[
            result(ProbeKind::Reachability, true, Some(10.0)),
            result(ProbeKind::Transfer, true, Some(20.0)),
        ]);
        assert_eq!(summaries.len(), 2);
    }
}
