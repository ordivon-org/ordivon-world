use std::collections::BTreeMap;

use anyhow::Result;
use edge_model::{ProbeProtocol, ProbeResult};
use serde::Serialize;

#[derive(Debug, Clone, Serialize, PartialEq)]
pub struct ProbeSummary {
    pub network: String,
    pub route: String,
    pub protocol: ProbeProtocol,
    pub target: String,
    pub samples: usize,
    pub successes: usize,
    pub success_rate: f64,
    pub p50_total_ms: Option<f64>,
    pub p95_total_ms: Option<f64>,
}

pub fn summarize(results: &[ProbeResult]) -> Vec<ProbeSummary> {
    type Key = (String, String, ProbeProtocol, String);
    let mut groups: BTreeMap<Key, Vec<&ProbeResult>> = BTreeMap::new();
    for result in results {
        groups
            .entry((
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
        .map(|((network, route, protocol, target), samples)| {
            let successes = samples.iter().filter(|sample| sample.success).count();
            let mut totals: Vec<f64> = samples
                .iter()
                .filter(|sample| sample.success)
                .filter_map(|sample| sample.total_ms)
                .collect();
            totals.sort_by(f64::total_cmp);
            ProbeSummary {
                network,
                route,
                protocol,
                target,
                samples: samples.len(),
                successes,
                success_rate: successes as f64 / samples.len() as f64,
                p50_total_ms: percentile(&totals, 0.50),
                p95_total_ms: percentile(&totals, 0.95),
            }
        })
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
        "# Ordivon Edge probe report\n\n| Network | Route | Protocol | Target | Samples | Success | P50 total | P95 total |\n|---|---|---|---|---:|---:|---:|---:|\n",
    );
    for summary in summaries {
        let p50 = format_ms(summary.p50_total_ms);
        let p95 = format_ms(summary.p95_total_ms);
        output.push_str(&format!(
            "| {} | {} | {} | {} | {} | {:.1}% | {} | {} |\n",
            summary.network,
            summary.route,
            summary.protocol,
            summary.target,
            summary.samples,
            summary.success_rate * 100.0,
            p50,
            p95
        ));
    }
    output
}

fn format_ms(value: Option<f64>) -> String {
    value.map_or_else(|| "—".to_owned(), |value| format!("{value:.1} ms"))
}

#[cfg(test)]
mod tests {
    use chrono::Utc;
    use edge_model::FailureClass;

    use super::*;

    fn result(success: bool, total_ms: Option<f64>) -> ProbeResult {
        ProbeResult {
            schema_version: 1,
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
            http_status: success.then_some(200),
            remote_ip: None,
            success,
            failure_class: (!success).then_some(FailureClass::Timeout),
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
    fn summary_counts_failures_but_times_successes_only() {
        let summaries = summarize(&[result(true, Some(10.0)), result(false, None)]);
        assert_eq!(summaries.len(), 1);
        assert_eq!(summaries[0].samples, 2);
        assert_eq!(summaries[0].successes, 1);
        assert_eq!(summaries[0].success_rate, 0.5);
        assert_eq!(summaries[0].p50_total_ms, Some(10.0));
    }
}
