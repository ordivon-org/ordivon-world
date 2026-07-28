use std::path::PathBuf;

use anyhow::Result;
use clap::Parser;
use link_world::ActorSurface;

#[derive(Debug, Parser)]
#[command(
    name = "link-world-actor",
    version,
    about = "Read-only Ordivon Link Network World v1 actor surface"
)]
struct Cli {
    #[arg(long, default_value = "artifacts/world-actors")]
    actor_root: PathBuf,
    world_id: String,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let view = ActorSurface::open(cli.actor_root, cli.world_id)?.inspect()?;
    println!("{}", serde_json::to_string_pretty(&view)?);
    Ok(())
}
