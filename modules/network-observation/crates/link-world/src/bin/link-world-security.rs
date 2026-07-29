use std::path::PathBuf;

use anyhow::Result;
use clap::{Parser, Subcommand};
use link_world::{SecurityOperation, SecurityPort, SecurityPortPaths};
use serde::Serialize;

#[derive(Debug, Parser)]
#[command(
    name = "link-world-security",
    version,
    about = "Ordivon Link component-owned Security lifecycle port v0"
)]
struct Cli {
    #[arg(long)]
    manifest: PathBuf,
    #[arg(long)]
    authority_root: PathBuf,
    #[arg(long)]
    observer_root: PathBuf,
    #[arg(long)]
    actor_root: PathBuf,
    #[arg(long)]
    operation_root: PathBuf,
    #[arg(long)]
    reconstruction_root: PathBuf,
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Snapshot,
    Execute {
        operation: SecurityOperation,
        operation_id: String,
    },
    Reconcile {
        operation: SecurityOperation,
        operation_id: String,
    },
    Residual,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let port = SecurityPort::open(SecurityPortPaths {
        manifest: cli.manifest,
        authority_root: cli.authority_root,
        observer_root: cli.observer_root,
        actor_root: cli.actor_root,
        operation_root: cli.operation_root,
        reconstruction_root: cli.reconstruction_root,
    })?;
    match cli.command {
        Command::Snapshot => print_json(&port.snapshot())?,
        Command::Execute {
            operation,
            operation_id,
        } => {
            let fault = std::env::var("ORDIVON_LINK_SECURITY_FAULT_AFTER_EFFECT")
                .is_ok_and(|value| value == operation.as_str());
            print_json(&port.execute_with_fault(operation, &operation_id, fault)?)?;
        }
        Command::Reconcile {
            operation,
            operation_id,
        } => print_json(&port.reconcile(operation, &operation_id)?)?,
        Command::Residual => print_json(&serde_json::json!({
            "schema_version": 1,
            "project": "link",
            "checks": port.residual_checks(),
        }))?,
    }
    Ok(())
}

fn print_json(value: &impl Serialize) -> Result<()> {
    println!("{}", serde_json::to_string(value)?);
    Ok(())
}
