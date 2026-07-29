mod common;

use std::fs;
use std::net::{SocketAddr, TcpListener as StdTcpListener};
use std::time::Duration;

use link_world::{
    ActorSurface, EgressResult, EventKind, LinkState, Mutation, ObserverLog, WorldPhase,
    serve_loopback_fixture,
};
use tempfile::TempDir;
use tokio::io::AsyncReadExt;
use tokio::net::TcpStream;

use common::{controller, fixture_manifest};

const FIXTURE_WORLD_ID: &str =
    "nw1-3ac94003a99380f5600b3db185e5db3044f4fc4ccd5f5da1bba6cf4d5bbdae89";

#[test]
fn lifecycle_is_idempotent_where_safe_and_observer_outlives_destroy() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    assert_eq!(world_id, FIXTURE_WORLD_ID);

    let created = controller.create(&manifest).unwrap();
    assert_eq!(created.state.runtime_revision, 0);
    assert!(created.actor_projection_current);
    assert_eq!(
        created.state.links["gateway-worker"].state,
        LinkState::Partitioned
    );
    assert_eq!(controller.create(&manifest).unwrap(), created);
    assert_eq!(controller.events(&world_id).unwrap().len(), 1);

    let actor = ActorSurface::open(temp.path().join("actor"), &world_id)
        .unwrap()
        .inspect()
        .unwrap();
    assert_eq!(actor.runtime_revision, 0);
    let actor_json = serde_json::to_string(&actor).unwrap();
    assert!(!actor_json.contains("observer"));
    assert!(!actor_json.contains("egress_evidence"));
    assert!(
        !temp
            .path()
            .join("actor")
            .join(&world_id)
            .join("manifest.json")
            .exists()
    );

    let state = controller
        .mutate(
            &world_id,
            Mutation::SetServiceReachability {
                service_id: "worker-rpc".into(),
                reachable: false,
            },
        )
        .unwrap();
    assert_eq!(state.runtime_revision, 1);
    let repeated = controller
        .mutate(
            &world_id,
            Mutation::SetServiceReachability {
                service_id: "worker-rpc".into(),
                reachable: false,
            },
        )
        .unwrap();
    assert_eq!(repeated.runtime_revision, 1);

    controller
        .mutate(
            &world_id,
            Mutation::SetLinkState {
                link_id: "gateway-worker".into(),
                state: LinkState::Up,
            },
        )
        .unwrap();
    controller
        .mutate(
            &world_id,
            Mutation::RotateIdentity {
                identity_id: "worker-identity".into(),
            },
        )
        .unwrap();
    controller
        .observe_egress(
            &world_id,
            "public-internet",
            EgressResult::Indeterminate,
            "fixture",
            "not_measured_by_local_fixture",
        )
        .unwrap();

    let frozen = controller.freeze(&world_id).unwrap();
    assert_eq!(frozen.phase, WorldPhase::Frozen);
    assert_eq!(
        controller.freeze(&world_id).unwrap().runtime_revision,
        frozen.runtime_revision
    );
    assert!(
        controller
            .mutate(
                &world_id,
                Mutation::SetRouteState {
                    route_id: "gateway-to-worker".into(),
                    enabled: false,
                },
            )
            .is_err()
    );

    let reset = controller.reset(&world_id).unwrap();
    assert_eq!(reset.phase, WorldPhase::Active);
    assert!(reset.services["worker-rpc"].reachable);
    assert_eq!(reset.identities["worker-identity"].generation, 1);
    assert_eq!(reset.links["gateway-worker"].state, LinkState::Partitioned);
    assert!(reset.egress_evidence.is_empty());
    assert_eq!(reset.runtime_revision, 6);

    let inspection = controller.inspect(&world_id).unwrap();
    assert_eq!(inspection.observer_event_count, 7);
    let destroyed = controller.destroy(&world_id).unwrap();
    assert!(matches!(destroyed.kind, EventKind::Destroyed));
    assert_eq!(destroyed.runtime_revision, 7);
    assert!(!temp.path().join("authority").join(&world_id).exists());
    assert!(
        ActorSurface::open(temp.path().join("actor"), &world_id)
            .unwrap()
            .inspect()
            .is_err()
    );

    let repeated_destroy = controller.destroy(&world_id).unwrap();
    assert_eq!(repeated_destroy, destroyed);
    assert_eq!(controller.events(&world_id).unwrap().len(), 8);
    assert!(controller.create(&manifest).is_err());
    assert!(!temp.path().join("authority").join(&world_id).exists());
}

#[test]
fn event_replay_repairs_a_missing_actor_projection() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();
    controller
        .mutate(
            &world_id,
            Mutation::SetRouteState {
                route_id: "gateway-to-worker".into(),
                enabled: false,
            },
        )
        .unwrap();

    let actor_directory = temp.path().join("actor").join(&world_id);
    fs::remove_dir_all(&actor_directory).unwrap();
    assert!(
        ActorSurface::open(temp.path().join("actor"), &world_id)
            .unwrap()
            .inspect()
            .is_err()
    );

    let inspection = controller.inspect(&world_id).unwrap();
    assert!(inspection.actor_projection_current);
    let actor = controller
        .actor_surface(&world_id)
        .unwrap()
        .inspect()
        .unwrap();
    assert_eq!(actor.runtime_revision, 1);
    assert!(!actor.routes["gateway-to-worker"].enabled);
}

#[test]
fn create_recovers_a_durable_manifest_without_a_creation_event() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest().normalized();
    let world_id = manifest.world_id();
    let authority = temp.path().join("authority");
    fs::create_dir(&authority).unwrap();
    let world = authority.join(&world_id);
    fs::create_dir(&world).unwrap();
    set_directory_private(&authority);
    set_directory_private(&world);
    fs::write(
        world.join("manifest.json"),
        serde_json::to_vec_pretty(&manifest).unwrap(),
    )
    .unwrap();

    let inspection = controller.create(&manifest).unwrap();
    assert_eq!(inspection.state.runtime_revision, 0);
    assert_eq!(inspection.observer_event_count, 1);
}

#[test]
fn observer_detects_rewrite_unknown_fields_and_unexpected_entries() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let observer = ObserverLog::new(temp.path().join("observer"));
    let events_directory = observer.events_directory(&world_id).unwrap();
    let first_event = events_directory.join("00000000000000000000.json");
    make_owner_writable(&first_event);
    let encoded = fs::read_to_string(&first_event).unwrap();
    let with_unknown = encoded.replacen("{", "{\"unexpected\":true,", 1);
    fs::write(&first_event, with_unknown).unwrap();

    let error = controller.events(&world_id).unwrap_err().to_string();
    assert!(error.contains("unknown field"), "{error}");
    assert!(
        controller
            .mutate(
                &world_id,
                Mutation::SetServiceReachability {
                    service_id: "worker-rpc".into(),
                    reachable: false,
                },
            )
            .is_err()
    );

    fs::write(events_directory.join("junk"), b"not an event").unwrap();
    assert!(observer.read_verified(&world_id).is_err());
}

#[test]
fn actor_and_authority_roots_have_distinct_permissions_and_content() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let authority_world = temp.path().join("authority").join(&world_id);
    let actor_world = temp.path().join("actor").join(&world_id);
    assert!(authority_world.join("manifest.json").is_file());
    assert!(actor_world.join("projection.json").is_file());
    assert!(!actor_world.join("events").exists());

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        assert_eq!(
            fs::metadata(temp.path().join("authority"))
                .unwrap()
                .permissions()
                .mode()
                & 0o777,
            0o700
        );
        assert_eq!(
            fs::metadata(temp.path().join("observer"))
                .unwrap()
                .permissions()
                .mode()
                & 0o777,
            0o700
        );
        assert_eq!(
            fs::metadata(actor_world.join("projection.json"))
                .unwrap()
                .permissions()
                .mode()
                & 0o777,
            0o444
        );
    }
}

#[tokio::test]
async fn loopback_fixture_withdraws_restores_and_reduces_connection_events() {
    let Some((reservations, addresses)) = reserve_loopback_addresses(3) else {
        eprintln!("loopback sockets are prohibited by this test sandbox; skipping");
        return;
    };
    drop(reservations);

    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let mut manifest = fixture_manifest();
    for (service, address) in manifest
        .nodes
        .iter_mut()
        .flat_map(|node| &mut node.services)
        .zip(addresses.iter().copied())
    {
        service.fixture_address = Some(address);
    }
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let fixture_controller = controller.clone();
    let fixture_world = world_id.clone();
    let fixture = tokio::spawn(async move {
        serve_loopback_fixture(fixture_controller, fixture_world, Duration::from_millis(10)).await
    });

    let first = wait_for_response(addresses[1]).await;
    assert!(first.contains("\"service_id\":\"worker-rpc\""));
    let _ = wait_for_response(addresses[1]).await;
    let connection_events = || {
        controller
            .events(&world_id)
            .unwrap()
            .iter()
            .filter(|event| {
                matches!(
                    &event.kind,
                    EventKind::ServiceConnectionObserved { service_id, .. }
                        if service_id == "worker-rpc"
                )
            })
            .count()
    };
    assert_eq!(connection_events(), 1);

    controller
        .mutate(
            &world_id,
            Mutation::SetServiceReachability {
                service_id: "worker-rpc".into(),
                reachable: false,
            },
        )
        .unwrap();
    wait_for_refusal(addresses[1]).await;
    controller
        .mutate(
            &world_id,
            Mutation::SetServiceReachability {
                service_id: "worker-rpc".into(),
                reachable: true,
            },
        )
        .unwrap();
    let restored = wait_for_response(addresses[1]).await;
    assert!(restored.contains("\"runtime_revision\":2"));
    assert_eq!(connection_events(), 2);

    fixture.abort();
    let _ = fixture.await;
}

fn reserve_loopback_addresses(count: usize) -> Option<(Vec<StdTcpListener>, Vec<SocketAddr>)> {
    let mut reservations = Vec::new();
    for _ in 0..count {
        match StdTcpListener::bind("127.0.0.1:0") {
            Ok(listener) => reservations.push(listener),
            Err(error) if error.kind() == std::io::ErrorKind::PermissionDenied => return None,
            Err(error) => panic!("failed to reserve loopback fixture port: {error}"),
        }
    }
    let addresses = reservations
        .iter()
        .map(|listener| listener.local_addr().unwrap())
        .collect();
    Some((reservations, addresses))
}

async fn wait_for_response(address: SocketAddr) -> String {
    for _ in 0..200 {
        if let Ok(mut stream) = TcpStream::connect(address).await {
            let mut response = String::new();
            if stream.read_to_string(&mut response).await.is_ok() && !response.is_empty() {
                return response;
            }
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
    panic!("fixture did not serve {address}");
}

async fn wait_for_refusal(address: SocketAddr) {
    for _ in 0..200 {
        if TcpStream::connect(address).await.is_err() {
            return;
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
    panic!("fixture did not withdraw {address}");
}

#[cfg(unix)]
fn make_owner_writable(path: &std::path::Path) {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(0o600)).unwrap();
}

#[cfg(unix)]
fn set_directory_private(path: &std::path::Path) {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(0o700)).unwrap();
}

#[cfg(not(unix))]
fn make_owner_writable(path: &std::path::Path) {
    let mut permissions = fs::metadata(path).unwrap().permissions();
    permissions.set_readonly(false);
    fs::set_permissions(path, permissions).unwrap();
}

#[cfg(not(unix))]
fn set_directory_private(_path: &std::path::Path) {}
