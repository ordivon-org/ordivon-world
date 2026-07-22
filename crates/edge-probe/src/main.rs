use std::path::PathBuf;
use std::time::Duration;

use anyhow::{Context, Result, bail};
use clap::{Args, Parser, Subcommand, ValueEnum};
use edge_model::ProbeProtocol;
use edge_probe::{
    ProbeOptions, append_results, load_registry, read_results, run_probe, summaries_json,
    summaries_markdown, summarize, write_text,
};

#[derive(Debug, Parser)]
#[command(
    name = "edge-probe",
    version,
    about = "Ordivon Edge network observation harness"
)]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Run(RunArgs),
    Compare(InputOutputArgs),
    Report(InputOutputArgs),
}

#[derive(Debug, Args)]
struct RunArgs {
    #[arg(long, default_value = "config/targets/default.toml")]
    targets: PathBuf,
    #[arg(long)]
    network: String,
    #[arg(long)]
    route: String,
    #[arg(long, value_enum, default_value_t = ProtocolSelection::All)]
    protocol: ProtocolSelection,
    #[arg(long, default_value_t = 1)]
    repeat: u32,
    #[arg(long, default_value_t = 15)]
    timeout_seconds: u64,
    #[arg(long)]
    no_env_proxy: bool,
    #[arg(long, env = "ORDIVON_EDGE_CURL_BIN", default_value = "curl")]
    curl_bin: String,
    #[arg(long)]
    output: PathBuf,
}

#[derive(Debug, Args)]
struct InputOutputArgs {
    #[arg(long)]
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

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Command::Run(args) => run(args),
        Command::Compare(args) => compare(args),
        Command::Report(args) => report(args),
    }
}

fn run(args: RunArgs) -> Result<()> {
    if args.repeat == 0 {
        bail!("--repeat must be at least 1");
    }
    if args.timeout_seconds == 0 {
        bail!("--timeout-seconds must be at least 1");
    }

    let registry = load_registry(&args.targets)?;
    let options = ProbeOptions {
        network: args.network,
        route: args.route,
        timeout: Duration::from_secs(args.timeout_seconds),
        no_env_proxy: args.no_env_proxy,
        curl_bin: args.curl_bin,
    };

    let mut results = Vec::new();
    for _ in 0..args.repeat {
        for target in registry.targets.iter().filter(|target| target.enabled) {
            for &protocol in &target.protocols {
                if args.protocol.includes(protocol) {
                    let result = run_probe(target, protocol, &options);
                    println!("{}", serde_json::to_string(&result)?);
                    results.push(result);
                }
            }
        }
    }

    if results.is_empty() {
        bail!("no enabled targets matched the selected protocol");
    }
    append_results(&args.output, &results)
        .with_context(|| format!("failed to append results to {}", args.output.display()))?;
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

fn emit(content: String, output: Option<PathBuf>) -> Result<()> {
    if let Some(path) = output {
        write_text(&path, &content)?;
    } else {
        println!("{content}");
    }
    Ok(())
}
