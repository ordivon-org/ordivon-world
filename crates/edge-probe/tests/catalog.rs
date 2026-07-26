use std::path::PathBuf;

use edge_probe::{load_transport_catalog, transport_catalog_markdown};

#[test]
fn committed_transport_catalog_is_valid_and_renderable() {
    let path =
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../config/transports/protocols.toml");
    let catalog = load_transport_catalog(&path).expect("load committed transport catalog");

    assert!(catalog.transports.len() >= 8);
    let markdown = transport_catalog_markdown(&catalog);
    assert!(markdown.contains("xray-vless-reality"));
    assert!(markdown.contains("hysteria2"));
    assert!(markdown.contains("sing-box"));
}
