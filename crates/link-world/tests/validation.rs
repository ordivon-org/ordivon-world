mod common;

use std::fs::{self, File};

use link_world::{
    CommunicationIdentity, Controller, IdentityKind, LinkState, Mutation, NodeService,
    ServiceProtocol,
};
use tempfile::TempDir;

use common::fixture_manifest;

#[test]
fn identity_is_equal_across_toml_json_and_all_collection_orders() {
    let manifest = fixture_manifest();
    let json = serde_json::to_string(&manifest).unwrap();
    let mut reordered: link_world::NetworkWorldManifest = serde_json::from_str(&json).unwrap();
    reordered.nodes.reverse();
    for node in &mut reordered.nodes {
        node.services.reverse();
    }
    reordered.links.reverse();
    reordered.subnets.reverse();
    reordered.trust_zones.reverse();
    reordered.communication_identities.reverse();
    reordered.routes.reverse();
    reordered.external_boundaries.reverse();
    reordered.initial_mutations.reverse();

    manifest.validate().unwrap();
    reordered.validate().unwrap();
    assert_eq!(manifest.world_id(), reordered.world_id());
    assert_eq!(manifest.manifest_revision(), reordered.manifest_revision());
}

#[test]
fn validation_rejects_noncanonical_networks_zero_ports_and_unicode_ids() {
    let mut manifest = fixture_manifest();
    manifest.subnets[0].cidr = "10.77.2.1/24".into();
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest.subnets[0].cidr = "2001:0db8::/32".into();
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest.nodes[0].services[0].fixture_address = Some("127.0.0.1:0".parse().unwrap());
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest.nodes[0].id = "databasé".into();
    assert!(manifest.validate().is_err());
}

#[test]
fn validation_rejects_global_duplicate_services_and_conflicting_initial_state() {
    let mut manifest = fixture_manifest();
    let duplicate = manifest.nodes[0].services[0].clone();
    manifest.nodes[1].services.push(duplicate);
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest.initial_mutations.push(Mutation::SetLinkState {
        link_id: "gateway-worker".into(),
        state: LinkState::Up,
    });
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest.nodes[0].services = (0..257)
        .map(|index| NodeService {
            id: format!("service-{index}"),
            protocol: ServiceProtocol::Tcp,
            fixture_address: None,
        })
        .collect();
    manifest.communication_identities.clear();
    assert!(manifest.validate().is_err());
}

#[test]
fn service_identity_must_bind_a_service_on_its_declared_node() {
    let mut manifest = fixture_manifest();
    manifest.communication_identities[0].service = Some("worker-rpc".into());
    assert!(manifest.validate().is_err());

    let mut manifest = fixture_manifest();
    manifest
        .communication_identities
        .push(CommunicationIdentity {
            id: "invalid-node-identity".into(),
            node: "gateway".into(),
            kind: IdentityKind::Node,
            service: Some("gateway-http".into()),
        });
    assert!(manifest.validate().is_err());
}

#[test]
fn manifest_loader_rejects_unknown_fields_and_oversized_input() {
    let temp = TempDir::new().unwrap();
    let unknown = temp.path().join("unknown.json");
    let input = serde_json::to_string(&fixture_manifest()).unwrap();
    fs::write(&unknown, input.replacen("{", "{\"unknown\":true,", 1)).unwrap();
    assert!(Controller::load_manifest(&unknown).is_err());

    let oversized = temp.path().join("oversized.toml");
    let file = File::create(&oversized).unwrap();
    file.set_len(1024 * 1024 + 1).unwrap();
    assert!(Controller::load_manifest(&oversized).is_err());
}

#[test]
fn root_paths_reject_nesting_parent_traversal_and_symlinks() {
    let temp = TempDir::new().unwrap();
    assert!(
        Controller::new(
            temp.path().join("root"),
            temp.path().join("root/observer"),
            temp.path().join("actor"),
        )
        .is_err()
    );
    assert!(
        Controller::new(
            temp.path().join("../authority"),
            temp.path().join("observer"),
            temp.path().join("actor"),
        )
        .is_err()
    );

    #[cfg(unix)]
    {
        use std::os::unix::fs::symlink;
        let target = temp.path().join("target");
        fs::create_dir(&target).unwrap();
        let symlink_path = temp.path().join("symlink");
        symlink(&target, &symlink_path).unwrap();
        assert!(
            Controller::new(
                symlink_path,
                temp.path().join("observer"),
                temp.path().join("actor"),
            )
            .is_err()
        );
    }
}

#[cfg(unix)]
#[test]
fn persisted_manifest_symlink_is_rejected() {
    use std::os::unix::fs::symlink;

    let temp = TempDir::new().unwrap();
    let controller = common::controller(temp.path());
    let manifest = fixture_manifest();
    let world_id = manifest.world_id();
    controller.create(&manifest).unwrap();

    let manifest_path = temp
        .path()
        .join("authority")
        .join(&world_id)
        .join("manifest.json");
    fs::remove_file(&manifest_path).unwrap();
    let outside = temp.path().join("outside.json");
    fs::write(&outside, serde_json::to_vec(&manifest).unwrap()).unwrap();
    symlink(outside, manifest_path).unwrap();
    assert!(controller.inspect(&world_id).is_err());
}
