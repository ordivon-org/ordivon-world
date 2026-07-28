use std::fs;
use std::net::{SocketAddr, TcpListener};

use link_world::{
    Controller, NetworkWorldManifest, SecurityOperation, SecurityPort, SecurityPortPaths,
};
use tempfile::TempDir;

fn manifest_with_free_ports() -> NetworkWorldManifest {
    let mut manifest: NetworkWorldManifest = toml::from_str(include_str!(
        "../../../config/worlds/disconnected-three-service.toml"
    ))
    .unwrap();
    let listeners: Vec<TcpListener> = (0..3)
        .map(|_| TcpListener::bind("127.0.0.1:0").unwrap())
        .collect();
    let addresses: Vec<SocketAddr> = listeners
        .iter()
        .map(|listener| listener.local_addr().unwrap())
        .collect();
    for (service, address) in manifest
        .nodes
        .iter_mut()
        .flat_map(|node| &mut node.services)
        .zip(addresses)
    {
        service.fixture_address = Some(address);
    }
    drop(listeners);
    manifest
}

fn port_fixture() -> (TempDir, SecurityPort, NetworkWorldManifest) {
    let temporary = tempfile::tempdir().unwrap();
    let manifest = manifest_with_free_ports();
    let manifest_path = temporary.path().join("world.toml");
    fs::write(&manifest_path, toml::to_string_pretty(&manifest).unwrap()).unwrap();
    let port = SecurityPort::open(SecurityPortPaths {
        manifest: manifest_path,
        authority_root: temporary.path().join("authority"),
        observer_root: temporary.path().join("observer"),
        actor_root: temporary.path().join("actor"),
        operation_root: temporary.path().join("operations"),
        reconstruction_root: temporary.path().join("reconstruction"),
    })
    .unwrap();
    (temporary, port, manifest)
}

#[test]
fn component_port_preserves_binding_and_reconstructs_in_fresh_roots() {
    let (_temporary, port, manifest) = port_fixture();
    let snapshot = port.snapshot();
    assert_eq!(snapshot.native_id, manifest.world_id());
    assert_eq!(snapshot.revision, manifest.manifest_revision());
    assert_eq!(snapshot.root_digest, manifest.manifest_revision());

    port.execute(SecurityOperation::Prepare, "prepare-1")
        .unwrap();
    port.execute(SecurityOperation::Start, "start-1").unwrap();
    port.execute(SecurityOperation::Freeze, "freeze-1").unwrap();
    port.execute(SecurityOperation::Destroy, "destroy-1")
        .unwrap();

    let reconstructed = port
        .execute(SecurityOperation::Reconstruct, "reconstruct-1")
        .unwrap();
    assert_eq!(
        reconstructed["detail"]["snapshot"],
        serde_json::to_value(&snapshot).unwrap()
    );
    assert_eq!(reconstructed["detail"]["fresh_root_removed"], true);
    assert!(
        port.execute(SecurityOperation::Verify, "verify-1").unwrap()["detail"]["mode"]
            == "destroyed"
    );
}

#[test]
fn lost_reset_response_is_proved_by_observer_without_redispatch() {
    let (_temporary, port, manifest) = port_fixture();
    port.execute(SecurityOperation::Prepare, "prepare-1")
        .unwrap();
    let error = port
        .execute_with_fault(SecurityOperation::Reset, "reset-ambiguous", true)
        .unwrap_err()
        .to_string();
    assert!(error.contains("response loss"));

    let reconciled = port
        .reconcile(SecurityOperation::Reset, "reset-ambiguous")
        .unwrap();
    assert_eq!(reconciled["reconciled"], true);
    assert_eq!(
        Controller::new(
            _temporary.path().join("authority"),
            _temporary.path().join("observer"),
            _temporary.path().join("actor")
        )
        .unwrap()
        .inspect(&manifest.world_id())
        .unwrap()
        .state
        .runtime_revision,
        1
    );

    let replay = port
        .execute(SecurityOperation::Reset, "reset-ambiguous")
        .unwrap();
    assert_eq!(replay, reconciled);
    assert_eq!(
        Controller::new(
            _temporary.path().join("authority"),
            _temporary.path().join("observer"),
            _temporary.path().join("actor")
        )
        .unwrap()
        .inspect(&manifest.world_id())
        .unwrap()
        .state
        .runtime_revision,
        1
    );
}

#[test]
fn destruction_residuals_distinguish_retained_evidence_from_live_effects() {
    let (_temporary, port, _manifest) = port_fixture();
    port.execute(SecurityOperation::Prepare, "prepare-1")
        .unwrap();
    port.execute(SecurityOperation::Destroy, "destroy-1")
        .unwrap();
    let checks = port.residual_checks();
    assert!(
        checks
            .iter()
            .any(|check| { check.subject_id.ends_with(":authority") && check.status == "clean" })
    );
    assert!(checks.iter().any(|check| {
        check.subject_id.ends_with(":observer") && check.status == "expected_retained"
    }));
    assert!(checks.iter().any(|check| {
        check.subject_id.ends_with(":actor-projection") && check.status == "expected_retained"
    }));
    assert!(
        checks
            .iter()
            .filter(|check| check.subject_id.contains(":fixture:"))
            .all(|check| check.status == "clean")
    );
    assert!(
        !checks
            .iter()
            .any(|check| check.status == "unexpected_residual")
    );
}
