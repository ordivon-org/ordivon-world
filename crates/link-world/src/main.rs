use std::net::IpAddr;
use std::path::PathBuf;
use std::time::Duration;

use anyhow::Result;
use clap::{Parser, Subcommand};
use link_world::{Controller, EgressResult, LinkState, Mutation, serve_loopback_fixture};
use serde::Serialize;

#[derive(Debug, Parser)]
#[command(
    name = "link-world",
    version,
    about = "Ordivon Link Network World v1 controller"
)]
struct Cli {
    #[arg(long, default_value = "artifacts/worlds")]
    authority_root: PathBuf,
    #[arg(long, default_value = "artifacts/world-observer")]
    observer_root: PathBuf,
    #[arg(long, default_value = "artifacts/world-actors")]
    actor_root: PathBuf,
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Validate {
        manifest: PathBuf,
    },
    Create {
        manifest: PathBuf,
    },
    Inspect {
        world_id: String,
    },
    Events {
        world_id: String,
    },
    Freeze {
        world_id: String,
    },
    Reset {
        world_id: String,
    },
    Destroy {
        world_id: String,
    },
    Mutate {
        world_id: String,
        #[command(subcommand)]
        mutation: MutationCommand,
    },
    RecordEgress {
        world_id: String,
        #[arg(long)]
        boundary: String,
        #[arg(long)]
        result: EgressResultArg,
        #[arg(long)]
        method: String,
        #[arg(long)]
        detail: String,
    },
    Fixture {
        world_id: String,
        #[arg(
            long,
            default_value_t = 25,
            value_parser = clap::value_parser!(u64).range(5..=10_000)
        )]
        poll_ms: u64,
    },
}

#[derive(Debug, Subcommand)]
enum MutationCommand {
    Service {
        service_id: String,
        #[arg(long, action = clap::ArgAction::Set)]
        reachable: bool,
    },
    Link {
        link_id: String,
        #[arg(long, action = clap::ArgAction::Set)]
        partitioned: bool,
    },
    Impairment {
        link_id: String,
        #[arg(long)]
        latency_ms: u32,
        #[arg(long)]
        loss_basis_points: u16,
    },
    Route {
        route_id: String,
        #[arg(long, action = clap::ArgAction::Set)]
        enabled: bool,
    },
    Dns {
        identity_id: String,
        #[arg(long)]
        address: Option<IpAddr>,
        #[arg(long, conflicts_with = "address")]
        clear: bool,
    },
    RotateIdentity {
        identity_id: String,
    },
    RevokeIdentity {
        identity_id: String,
        #[arg(long, default_value_t = true, action = clap::ArgAction::Set)]
        revoked: bool,
    },
}

#[derive(Debug, Clone, Copy, clap::ValueEnum)]
enum EgressResultArg {
    Reachable,
    Unreachable,
    Indeterminate,
}

#[derive(Serialize)]
struct ValidationOutput {
    schema_version: u32,
    world_id: String,
    manifest_revision: String,
    valid: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();
    let controller = Controller::new(cli.authority_root, cli.observer_root, cli.actor_root)?;
    match cli.command {
        Command::Validate { manifest } => {
            let manifest = Controller::load_manifest(&manifest)?;
            Controller::validate_manifest(&manifest)?;
            print_json(&ValidationOutput {
                schema_version: 1,
                world_id: manifest.world_id(),
                manifest_revision: manifest.manifest_revision(),
                valid: true,
            })?;
        }
        Command::Create { manifest } => {
            let manifest = Controller::load_manifest(&manifest)?;
            print_json(&controller.create(&manifest)?)?;
        }
        Command::Inspect { world_id } => print_json(&controller.inspect(&world_id)?)?,
        Command::Events { world_id } => print_json(&controller.events(&world_id)?)?,
        Command::Freeze { world_id } => print_json(&controller.freeze(&world_id)?)?,
        Command::Reset { world_id } => print_json(&controller.reset(&world_id)?)?,
        Command::Destroy { world_id } => print_json(&controller.destroy(&world_id)?)?,
        Command::Mutate { world_id, mutation } => {
            print_json(&controller.mutate(&world_id, mutation.into())?)?;
        }
        Command::RecordEgress {
            world_id,
            boundary,
            result,
            method,
            detail,
        } => {
            print_json(&controller.observe_egress(
                &world_id,
                &boundary,
                result.into(),
                &method,
                &detail,
            )?)?;
        }
        Command::Fixture { world_id, poll_ms } => {
            serve_loopback_fixture(controller, world_id, Duration::from_millis(poll_ms)).await?;
        }
    }
    Ok(())
}

impl From<MutationCommand> for Mutation {
    fn from(command: MutationCommand) -> Self {
        match command {
            MutationCommand::Service {
                service_id,
                reachable,
            } => Self::SetServiceReachability {
                service_id,
                reachable,
            },
            MutationCommand::Link {
                link_id,
                partitioned,
            } => Self::SetLinkState {
                link_id,
                state: if partitioned {
                    LinkState::Partitioned
                } else {
                    LinkState::Up
                },
            },
            MutationCommand::Impairment {
                link_id,
                latency_ms,
                loss_basis_points,
            } => Self::SetImpairment {
                link_id,
                latency_ms,
                loss_basis_points,
            },
            MutationCommand::Route { route_id, enabled } => {
                Self::SetRouteState { route_id, enabled }
            }
            MutationCommand::Dns {
                identity_id,
                address,
                clear: _,
            } => Self::SetDnsOverride {
                identity_id,
                address,
            },
            MutationCommand::RotateIdentity { identity_id } => Self::RotateIdentity { identity_id },
            MutationCommand::RevokeIdentity {
                identity_id,
                revoked,
            } => Self::RevokeIdentity {
                identity_id,
                revoked,
            },
        }
    }
}

impl From<EgressResultArg> for EgressResult {
    fn from(value: EgressResultArg) -> Self {
        match value {
            EgressResultArg::Reachable => Self::Reachable,
            EgressResultArg::Unreachable => Self::Unreachable,
            EgressResultArg::Indeterminate => Self::Indeterminate,
        }
    }
}

fn print_json(value: &impl Serialize) -> Result<()> {
    println!("{}", serde_json::to_string_pretty(value)?);
    Ok(())
}
