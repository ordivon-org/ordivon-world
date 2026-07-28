use std::path::Path;

use link_world::{Controller, NetworkWorldManifest};

pub fn fixture_manifest() -> NetworkWorldManifest {
    toml::from_str(include_str!(
        "../../../../config/worlds/disconnected-three-service.toml"
    ))
    .expect("fixture manifest")
}

#[allow(dead_code)]
pub fn controller(root: &Path) -> Controller {
    Controller::new(
        root.join("authority"),
        root.join("observer"),
        root.join("actor"),
    )
    .expect("controller")
}
