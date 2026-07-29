mod common;

use std::sync::{Arc, Barrier};

use link_world::{LinkState, Mutation};
use tempfile::TempDir;

use common::{controller, fixture_manifest};

#[test]
fn concurrent_distinct_mutations_serialize_without_lost_updates() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let barrier = Arc::new(Barrier::new(3));
    let service_controller = controller.clone();
    let service_world = world_id.clone();
    let service_barrier = barrier.clone();
    let service = std::thread::spawn(move || {
        service_barrier.wait();
        service_controller.mutate(
            &service_world,
            Mutation::SetServiceReachability {
                service_id: "worker-rpc".into(),
                reachable: false,
            },
        )
    });
    let link_controller = controller.clone();
    let link_world = world_id.clone();
    let link_barrier = barrier.clone();
    let link = std::thread::spawn(move || {
        link_barrier.wait();
        link_controller.mutate(
            &link_world,
            Mutation::SetLinkState {
                link_id: "gateway-worker".into(),
                state: LinkState::Up,
            },
        )
    });
    barrier.wait();
    service.join().unwrap().unwrap();
    link.join().unwrap().unwrap();

    let state = controller.inspect(&world_id).unwrap().state;
    assert_eq!(state.runtime_revision, 2);
    assert!(!state.services["worker-rpc"].reachable);
    assert_eq!(state.links["gateway-worker"].state, LinkState::Up);
}

#[test]
fn concurrent_identical_set_mutations_emit_one_transition() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let barrier = Arc::new(Barrier::new(3));
    let mut handles = Vec::new();
    for _ in 0..2 {
        let controller = controller.clone();
        let world_id = world_id.clone();
        let barrier = barrier.clone();
        handles.push(std::thread::spawn(move || {
            barrier.wait();
            controller.mutate(
                &world_id,
                Mutation::SetServiceReachability {
                    service_id: "worker-rpc".into(),
                    reachable: false,
                },
            )
        }));
    }
    barrier.wait();
    for handle in handles {
        handle.join().unwrap().unwrap();
    }

    let inspection = controller.inspect(&world_id).unwrap();
    assert_eq!(inspection.state.runtime_revision, 1);
    assert_eq!(inspection.observer_event_count, 2);
}

#[test]
fn concurrent_identity_rotations_are_both_preserved() {
    let temp = TempDir::new().unwrap();
    let controller = controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let barrier = Arc::new(Barrier::new(3));
    let mut handles = Vec::new();
    for _ in 0..2 {
        let controller = controller.clone();
        let world_id = world_id.clone();
        let barrier = barrier.clone();
        handles.push(std::thread::spawn(move || {
            barrier.wait();
            controller.mutate(
                &world_id,
                Mutation::RotateIdentity {
                    identity_id: "worker-identity".into(),
                },
            )
        }));
    }
    barrier.wait();
    for handle in handles {
        handle.join().unwrap().unwrap();
    }

    let inspection = controller.inspect(&world_id).unwrap();
    assert_eq!(inspection.state.runtime_revision, 2);
    assert_eq!(inspection.state.identities["worker-identity"].generation, 3);
}
