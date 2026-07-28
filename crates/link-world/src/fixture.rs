use std::net::SocketAddr;
use std::time::Duration;

use anyhow::{Result, bail};
use serde::Serialize;
use tokio::io::AsyncWriteExt;
use tokio::net::{TcpListener, TcpStream};
use tokio::task::JoinSet;
use tokio::time::sleep;

use crate::controller::Controller;
use crate::model::{NodeService, WORLD_SCHEMA_VERSION};

#[derive(Serialize)]
struct FixtureResponse<'a> {
    schema_version: u32,
    world_id: &'a str,
    service_id: &'a str,
    runtime_revision: u64,
}

pub async fn serve_loopback_fixture(
    controller: Controller,
    world_id: String,
    poll_interval: Duration,
) -> Result<()> {
    if poll_interval < Duration::from_millis(5) || poll_interval > Duration::from_secs(10) {
        bail!("fixture poll interval must be between 5 milliseconds and 10 seconds");
    }
    let (manifest, _, _) = controller.load_active(&world_id)?;
    let services: Vec<NodeService> = manifest
        .nodes
        .into_iter()
        .flat_map(|node| node.services)
        .filter(|service| service.fixture_address.is_some())
        .collect();
    if services.is_empty() {
        bail!("world has no loopback fixture addresses");
    }

    let mut tasks = JoinSet::new();
    for service in services {
        let controller = controller.clone();
        let world_id = world_id.clone();
        tasks.spawn(
            async move { serve_service(controller, world_id, service, poll_interval).await },
        );
    }

    while let Some(result) = tasks.join_next().await {
        result??;
    }
    Ok(())
}

async fn serve_service(
    controller: Controller,
    world_id: String,
    service: NodeService,
    poll_interval: Duration,
) -> Result<()> {
    let address = service
        .fixture_address
        .expect("fixture service has an address");
    let mut listener: Option<TcpListener> = None;
    let mut last_observed_revision = None;

    loop {
        let (_, state, _) = controller.load_active(&world_id)?;
        let reachable = state
            .services
            .get(&service.id)
            .is_some_and(|runtime| runtime.reachable);

        if !reachable {
            listener = None;
            sleep(poll_interval).await;
            continue;
        }
        if listener.is_none() {
            listener = Some(bind_loopback(address).await?);
        }

        let accept = listener.as_ref().expect("listener is bound").accept();
        match tokio::time::timeout(poll_interval, accept).await {
            Ok(Ok((stream, _))) => {
                if last_observed_revision != Some(state.runtime_revision) {
                    controller.observe_service_connection(
                        &world_id,
                        &service.id,
                        state.runtime_revision,
                    )?;
                    last_observed_revision = Some(state.runtime_revision);
                }
                write_response(stream, &world_id, &service.id, state.runtime_revision).await?;
            }
            Ok(Err(error)) => return Err(error.into()),
            Err(_) => {}
        }
    }
}

async fn bind_loopback(address: SocketAddr) -> Result<TcpListener> {
    if !address.ip().is_loopback() {
        bail!("fixture refused non-loopback address {address}");
    }
    Ok(TcpListener::bind(address).await?)
}

async fn write_response(
    mut stream: TcpStream,
    world_id: &str,
    service_id: &str,
    runtime_revision: u64,
) -> Result<()> {
    let response = FixtureResponse {
        schema_version: WORLD_SCHEMA_VERSION,
        world_id,
        service_id,
        runtime_revision,
    };
    let mut encoded = serde_json::to_vec(&response)?;
    encoded.push(b'\n');
    stream.write_all(&encoded).await?;
    stream.shutdown().await?;
    Ok(())
}
