use std::fs;
use std::path::PathBuf;
use std::thread;
use std::time::{Duration, Instant};

use anyhow::{Context, Result, bail};
use chrono::Utc;
use clap::{Args, Parser, Subcommand, ValueEnum};
use link_model::{ProbeKind, ProbeProtocol};
use link_probe::{
    ProbeOptions, append_results, load_registry, load_transport_catalog, read_results, run_probe,
    summaries_json, summaries_markdown, summarize, transport_catalog_markdown, write_text,
};

#[derive(Debug, Parser)]
#[command(
    name = "link-probe",
    version,
    about = "Ordivon Edge network observation harness"
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Measure DNS, transport, TLS/QUIC, TTFB, and completion.
    Run(RunArgs),
    /// Download a declared object and record bytes and throughput.
    Transfer(TransferArgs),
    /// Hold one response-body connection until the requested deadline.
    Lifetime(LifetimeArgs),
    /// Aggregate one or more NDJSON collections as JSON.
    Compare(InputOutputArgs),
    /// Render one or more NDJSON collections as Markdown.
    Report(InputOutputArgs),
    /// Validate and render the pinned transport source catalog.
    Catalog(CatalogArgs),
}

#[derive(Debug, Args)]
struct CollectionControls {
    #[arg(long)]
    network: String,
    #[arg(long)]
    route: String,
    #[arg(long, value_enum, default_value_t = ProtocolSelection::All)]
    protocol: ProtocolSelection,
    #[arg(long, default_value_t = 1)]
    repeat: u32,
    /// Start-to-start cadence between collection rounds.
    #[arg(long, default_value_t = 0)]
    interval_seconds: u64,
    #[arg(long)]
    collection_id: Option<String>,
    #[arg(long)]
    no_env_proxy: bool,
    #[arg(long, env = "ORDIVON_LINK_CURL_BIN", default_value = "curl")]
    curl_bin: String,
    #[arg(long)]
    truncate_output: bool,
    #[arg(long)]
    output: PathBuf,
}

#[derive(Debug, Args)]
struct RunArgs {
    #[arg(long, default_value = "config/targets/default.toml")]
    targets: PathBuf,
    #[command(flatten)]
    controls: CollectionControls,
    #[arg(long, default_value_t = 15)]
    timeout_seconds: u64,
}

#[derive(Debug, Args)]
struct TransferArgs {
    #[arg(long, default_value = "config/targets/transfer.toml")]
    targets: PathBuf,
    #[command(flatten)]
    controls: CollectionControls,
    #[arg(long, default_value_t = 60)]
    timeout_seconds: u64,
}

#[derive(Debug, Args)]
struct LifetimeArgs {
    #[arg(long, default_value = "config/targets/transfer.toml")]
    targets: PathBuf,
    #[command(flatten)]
    controls: CollectionControls,
    #[arg(long, default_value_t = 15)]
    duration_seconds: u64,
    #[arg(long, default_value_t = 65_536)]
    rate_limit_bytes_per_second: u64,
}

#[derive(Debug, Args)]
struct InputOutputArgs {
    #[arg(long)]
    input: PathBuf,
    #[arg(long)]
    output: Option<PathBuf>,
}

#[derive(Debug, Args)]
struct CatalogArgs {
    #[arg(long, default_value = "config/transports/protocols.toml")]
    input: PathBuf,
    #[arg(long)]
    output: Option<PathBuf>,
}

#[derive(Debug, Clone, Copy, ValueEnum)]
enum ProtocolSelection {
    All,
    HttpTls,
    Quic,
}

impl ProtocolSelection {
    fn includes(self, protocol: ProbeProtocol) -> bool {
        match self {
            Self::All => true,
            Self::HttpTls => protocol == ProbeProtocol::HttpTls,
            Self::Quic => protocol == ProbeProtocol::Quic,
        }
    }
}

struct CollectionRequest {
    targets: PathBuf,
    controls: CollectionControls,
    probe_kind: ProbeKind,
    timeout: Duration,
    requested_duration: Option<Duration>,
    rate_limit_bytes_per_second: Option<u64>,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Command::Run(args) => execute_collection(CollectionRequest {
            targets: args.targets,
            controls: args.controls,
            probe_kind: ProbeKind::Reachability,
            timeout: checked_duration("--timeout-seconds", args.timeout_seconds)?,
            requested_duration: None,
            rate_limit_bytes_per_second: None,
        }),
        Command::Transfer(args) => execute_collection(CollectionRequest {
            targets: args.targets,
            controls: args.controls,
            probe_kind: ProbeKind::Transfer,
            timeout: checked_duration("--timeout-seconds", args.timeout_seconds)?,
            requested_duration: None,
            rate_limit_bytes_per_second: None,
        }),
        Command::Lifetime(args) => {
            if args.rate_limit_bytes_per_second == 0 {
                bail!("--rate-limit-bytes-per-second must be at least 1");
            }
            let duration = checked_duration("--duration-seconds", args.duration_seconds)?;
            execute_collection(CollectionRequest {
                targets: args.targets,
                controls: args.controls,
                probe_kind: ProbeKind::ConnectionLifetime,
                timeout: duration,
                requested_duration: Some(duration),
                rate_limit_bytes_per_second: Some(args.rate_limit_bytes_per_second),
            })
        }
        Command::Compare(args) => compare(args),
        Command::Report(args) => report(args),
        Command::Catalog(args) => catalog(args),
    }
}

fn checked_duration(flag: &str, seconds: u64) -> Result<Duration> {
    if seconds == 0 {
        bail!("{flag} must be at least 1");
    }
    Ok(Duration::from_secs(seconds))
}

fn execute_collection(request: CollectionRequest) -> Result<()> {
    if request.controls.repeat == 0 {
        bail!("--repeat must be at least 1");
    }

    let registry = load_registry(&request.targets)?;
    if request.controls.truncate_output && request.controls.output.exists() {
        fs::remove_file(&request.controls.output).with_context(|| {
            format!(
                "failed to truncate existing output {}",
                request.controls.output.display()
            )
        })?;
    }

    let collection_id = request.controls.collection_id.unwrap_or_else(|| {
        format!(
            "{}-{}",
            request.probe_kind,
            Utc::now().format("%Y%m%dT%H%M%S%.3fZ")
        )
    });
    let cadence = Duration::from_secs(request.controls.interval_seconds);
    let mut total_results = 0usize;

    for round in 1..=request.controls.repeat {
        let round_started = Instant::now();
        let options = ProbeOptions {
            network: request.controls.network.clone(),
            route: request.controls.route.clone(),
            timeout: request.timeout,
            no_env_proxy: request.controls.no_env_proxy,
            curl_bin: request.controls.curl_bin.clone(),
            probe_kind: request.probe_kind,
            collection_id: collection_id.clone(),
            sample_index: round,
            requested_duration: request.requested_duration,
            rate_limit_bytes_per_second: request.rate_limit_bytes_per_second,
        };
        let mut round_results = Vec::new();

        for target in registry.targets.iter().filter(|target| target.enabled) {
            for &protocol in &target.protocols {
                if request.controls.protocol.includes(protocol) {
                    let result = run_probe(target, protocol, &options);
                    println!("{}", serde_json::to_string(&result)?);
                    round_results.push(result);
                }
            }
        }

        if round_results.is_empty() {
            bail!("no enabled targets matched the selected protocol");
        }
        append_results(&request.controls.output, &round_results).with_context(|| {
            format!(
                "failed to append results to {}",
                request.controls.output.display()
            )
        })?;
        total_results += round_results.len();

        if round < request.controls.repeat && !cadence.is_zero() {
            thread::sleep(cadence.saturating_sub(round_started.elapsed()));
        }
    }

    if total_results == 0 {
        bail!("collection produced no results");
    }
    Ok(())
}

fn compare(args: InputOutputArgs) -> Result<()> {
    let results = read_results(&args.input)?;
    let content = summaries_json(&summarize(&results))?;
    emit(content, args.output)
}

fn report(args: InputOutputArgs) -> Result<()> {
    let results = read_results(&args.input)?;
    let content = summaries_markdown(&summarize(&results));
    emit(content, args.output)
}

fn catalog(args: CatalogArgs) -> Result<()> {
    let catalog = load_transport_catalog(&args.input)?;
    emit(transport_catalog_markdown(&catalog), args.output)
}

fn emit(content: String, output: Option<PathBuf>) -> Result<()> {
    if let Some(path) = output {
        write_text(&path, &content)?;
    } else {
        println!("{content}");
    }
    Ok(())
}
