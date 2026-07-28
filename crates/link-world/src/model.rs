use std::collections::{BTreeMap, BTreeSet};
use std::net::{IpAddr, SocketAddr};

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

pub const WORLD_SCHEMA_VERSION: u32 = 1;
const MAX_ITEMS: usize = 256;
const MAX_ID_BYTES: usize = 64;
const MAX_TEXT_BYTES: usize = 256;
const IDENTITY_DOMAIN: &[u8] = b"ordivon-link/network-world-manifest/v1\0";

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct NetworkWorldManifest {
    pub schema_version: u32,
    pub name: String,
    pub nodes: Vec<Node>,
    pub links: Vec<Link>,
    pub subnets: Vec<Subnet>,
    pub trust_zones: Vec<TrustZone>,
    pub communication_identities: Vec<CommunicationIdentity>,
    pub routes: Vec<Route>,
    pub external_boundaries: Vec<ExternalBoundary>,
    #[serde(default)]
    pub initial_mutations: Vec<Mutation>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Node {
    pub id: String,
    pub subnet: String,
    #[serde(default)]
    pub services: Vec<NodeService>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct NodeService {
    pub id: String,
    pub protocol: ServiceProtocol,
    #[serde(default)]
    pub fixture_address: Option<SocketAddr>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum ServiceProtocol {
    Tcp,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Link {
    pub id: String,
    pub node_a: String,
    pub node_b: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Subnet {
    pub id: String,
    pub cidr: String,
    pub trust_zone: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct TrustZone {
    pub id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CommunicationIdentity {
    pub id: String,
    pub node: String,
    pub kind: IdentityKind,
    #[serde(default)]
    pub service: Option<String>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum IdentityKind {
    Service,
    Node,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Route {
    pub id: String,
    pub source_subnet: String,
    pub destination: String,
    #[serde(default)]
    pub via_node: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ExternalBoundary {
    pub id: String,
    pub destination: String,
    pub policy: BoundaryPolicy,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum BoundaryPolicy {
    DeclaredDeny,
    DeclaredAllow,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Mutation {
    SetServiceReachability {
        service_id: String,
        reachable: bool,
    },
    SetLinkState {
        link_id: String,
        state: LinkState,
    },
    SetImpairment {
        link_id: String,
        latency_ms: u32,
        loss_basis_points: u16,
    },
    SetRouteState {
        route_id: String,
        enabled: bool,
    },
    SetDnsOverride {
        identity_id: String,
        address: Option<IpAddr>,
    },
    RotateIdentity {
        identity_id: String,
    },
    RevokeIdentity {
        identity_id: String,
        revoked: bool,
    },
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum LinkState {
    Up,
    Partitioned,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum WorldPhase {
    Active,
    Frozen,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct WorldState {
    pub schema_version: u32,
    pub world_id: String,
    pub manifest_revision: String,
    pub runtime_revision: u64,
    pub phase: WorldPhase,
    pub effect_semantics: EffectSemantics,
    pub links: BTreeMap<String, LinkRuntime>,
    pub services: BTreeMap<String, ServiceRuntime>,
    pub routes: BTreeMap<String, RouteRuntime>,
    pub identities: BTreeMap<String, IdentityRuntime>,
    pub dns_overrides: BTreeMap<String, Option<IpAddr>>,
    pub egress_evidence: Vec<EgressEvidence>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct EffectSemantics {
    pub service_reachability: EffectMode,
    pub link_state: EffectMode,
    pub latency_loss: EffectMode,
    pub routes: EffectMode,
    pub dns: EffectMode,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum EffectMode {
    ModeledOnly,
    OptInLoopbackFixture,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct LinkRuntime {
    pub state: LinkState,
    pub impairment: Impairment,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct Impairment {
    pub latency_ms: u32,
    pub loss_basis_points: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ServiceRuntime {
    pub reachable: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct RouteRuntime {
    pub enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct IdentityRuntime {
    pub generation: u64,
    pub revoked: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct EgressEvidence {
    pub boundary_id: String,
    pub result: EgressResult,
    pub method: String,
    pub detail: String,
    pub observed_at_revision: u64,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum EgressResult {
    Reachable,
    Unreachable,
    Indeterminate,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct ActorView {
    pub schema_version: u32,
    pub world_id: String,
    pub runtime_revision: u64,
    pub phase: WorldPhase,
    pub effect_semantics: EffectSemantics,
    pub links: BTreeMap<String, LinkRuntime>,
    pub services: BTreeMap<String, ServiceRuntime>,
    pub routes: BTreeMap<String, RouteRuntime>,
    pub identities: BTreeMap<String, IdentityRuntime>,
    pub dns_overrides: BTreeMap<String, Option<IpAddr>>,
}

#[derive(Debug, Error, PartialEq, Eq)]
pub enum ManifestError {
    #[error("unsupported world schema version {0}")]
    UnsupportedSchema(u32),
    #[error("{collection} must contain between 1 and {MAX_ITEMS} items")]
    InvalidCollectionSize { collection: &'static str },
    #[error("unsafe or empty {kind} id `{id}`")]
    UnsafeId { kind: &'static str, id: String },
    #[error("duplicate {kind} id `{id}`")]
    DuplicateId { kind: &'static str, id: String },
    #[error("{kind} `{id}` references missing {target_kind} `{target}`")]
    MissingReference {
        kind: &'static str,
        id: String,
        target_kind: &'static str,
        target: String,
    },
    #[error("link `{0}` must connect two distinct nodes")]
    SelfLink(String),
    #[error("service `{0}` must have a loopback fixture address")]
    NonLoopbackFixture(String),
    #[error("service `{0}` fixture port must not be zero")]
    ZeroFixturePort(String),
    #[error("service fixture address `{0}` is used more than once")]
    DuplicateFixtureAddress(SocketAddr),
    #[error("{kind} text is empty, oversized, or contains control characters")]
    InvalidText { kind: &'static str },
    #[error("{kind} `{id}` has invalid network prefix `{cidr}`")]
    InvalidNetworkPrefix {
        kind: &'static str,
        id: String,
        cidr: String,
    },
    #[error("impairment loss must not exceed 10000 basis points")]
    InvalidLoss,
    #[error("identity `{identity}` kind and service reference disagree")]
    InvalidIdentityBinding { identity: String },
    #[error("route `{route}` next hop `{node}` is not on source subnet `{subnet}`")]
    InvalidRouteNextHop {
        route: String,
        node: String,
        subnet: String,
    },
    #[error("initial mutations conflict for `{0}`")]
    ConflictingInitialMutation(String),
    #[error("initial mutation is invalid: {0}")]
    InvalidInitialMutation(String),
}

impl NetworkWorldManifest {
    pub fn validate(&self) -> Result<(), ManifestError> {
        if self.schema_version != WORLD_SCHEMA_VERSION {
            return Err(ManifestError::UnsupportedSchema(self.schema_version));
        }
        validate_id("world", &self.name)?;
        validate_nonempty_size("nodes", self.nodes.len())?;
        validate_nonempty_size("subnets", self.subnets.len())?;
        validate_nonempty_size("trust_zones", self.trust_zones.len())?;
        validate_max_size("links", self.links.len())?;
        validate_max_size(
            "communication_identities",
            self.communication_identities.len(),
        )?;
        validate_max_size("routes", self.routes.len())?;
        validate_max_size("external_boundaries", self.external_boundaries.len())?;
        validate_max_size("initial_mutations", self.initial_mutations.len())?;

        let zones = collect_ids("trust_zone", self.trust_zones.iter().map(|item| &item.id))?;
        let subnets = collect_ids("subnet", self.subnets.iter().map(|item| &item.id))?;
        let nodes = collect_ids("node", self.nodes.iter().map(|item| &item.id))?;
        let _links = collect_ids("link", self.links.iter().map(|item| &item.id))?;
        let _identities = collect_ids(
            "identity",
            self.communication_identities.iter().map(|item| &item.id),
        )?;
        let _routes = collect_ids("route", self.routes.iter().map(|item| &item.id))?;
        let _boundaries = collect_ids(
            "external_boundary",
            self.external_boundaries.iter().map(|item| &item.id),
        )?;

        let mut subnet_prefixes = BTreeSet::new();
        for subnet in &self.subnets {
            validate_cidr("subnet", &subnet.id, &subnet.cidr)?;
            if !subnet_prefixes.insert(&subnet.cidr) {
                return Err(ManifestError::DuplicateId {
                    kind: "subnet prefix",
                    id: subnet.cidr.clone(),
                });
            }
            require_reference(
                "subnet",
                &subnet.id,
                "trust_zone",
                &subnet.trust_zone,
                &zones,
            )?;
        }

        let mut services = BTreeSet::new();
        let mut service_nodes = BTreeMap::new();
        let mut addresses = BTreeSet::new();
        let node_subnets: BTreeMap<&str, &str> = self
            .nodes
            .iter()
            .map(|node| (node.id.as_str(), node.subnet.as_str()))
            .collect();
        for node in &self.nodes {
            require_reference("node", &node.id, "subnet", &node.subnet, &subnets)?;
            validate_max_size("node services", node.services.len())?;
            for service in &node.services {
                validate_id("service", &service.id)?;
                if !services.insert(service.id.as_str()) {
                    return Err(ManifestError::DuplicateId {
                        kind: "service",
                        id: service.id.clone(),
                    });
                }
                service_nodes.insert(service.id.as_str(), node.id.as_str());
                if let Some(address) = service.fixture_address {
                    if !address.ip().is_loopback() {
                        return Err(ManifestError::NonLoopbackFixture(service.id.clone()));
                    }
                    if address.port() == 0 {
                        return Err(ManifestError::ZeroFixturePort(service.id.clone()));
                    }
                    if !addresses.insert(address) {
                        return Err(ManifestError::DuplicateFixtureAddress(address));
                    }
                }
            }
        }
        if services.len() > MAX_ITEMS {
            return Err(ManifestError::InvalidCollectionSize {
                collection: "services",
            });
        }

        for link in &self.links {
            if link.node_a == link.node_b {
                return Err(ManifestError::SelfLink(link.id.clone()));
            }
            require_reference("link", &link.id, "node", &link.node_a, &nodes)?;
            require_reference("link", &link.id, "node", &link.node_b, &nodes)?;
        }

        for identity in &self.communication_identities {
            require_reference("identity", &identity.id, "node", &identity.node, &nodes)?;
            let valid_binding = match (identity.kind, identity.service.as_deref()) {
                (IdentityKind::Node, None) => true,
                (IdentityKind::Service, Some(service)) => {
                    service_nodes.get(service).copied() == Some(identity.node.as_str())
                }
                _ => false,
            };
            if !valid_binding {
                return Err(ManifestError::InvalidIdentityBinding {
                    identity: identity.id.clone(),
                });
            }
        }

        for route in &self.routes {
            validate_cidr("route", &route.id, &route.destination)?;
            require_reference("route", &route.id, "subnet", &route.source_subnet, &subnets)?;
            if let Some(via_node) = &route.via_node {
                require_reference("route", &route.id, "node", via_node, &nodes)?;
                if node_subnets.get(via_node.as_str()).copied()
                    != Some(route.source_subnet.as_str())
                {
                    return Err(ManifestError::InvalidRouteNextHop {
                        route: route.id.clone(),
                        node: via_node.clone(),
                        subnet: route.source_subnet.clone(),
                    });
                }
            }
        }

        for boundary in &self.external_boundaries {
            validate_cidr("external_boundary", &boundary.id, &boundary.destination)?;
        }

        let baseline = WorldState::base(self);
        let mut initial_slots = BTreeSet::new();
        for mutation in &self.initial_mutations {
            baseline
                .check_mutation(mutation)
                .map_err(ManifestError::InvalidInitialMutation)?;
            let slot = mutation.initial_slot();
            if !initial_slots.insert(slot.clone()) {
                return Err(ManifestError::ConflictingInitialMutation(slot));
            }
        }

        Ok(())
    }

    pub fn normalized(&self) -> Self {
        let mut manifest = self.clone();
        manifest.nodes.sort_by(|left, right| left.id.cmp(&right.id));
        for node in &mut manifest.nodes {
            node.services.sort_by(|left, right| left.id.cmp(&right.id));
        }
        manifest.links.sort_by(|left, right| left.id.cmp(&right.id));
        manifest
            .subnets
            .sort_by(|left, right| left.id.cmp(&right.id));
        manifest
            .trust_zones
            .sort_by(|left, right| left.id.cmp(&right.id));
        manifest
            .communication_identities
            .sort_by(|left, right| left.id.cmp(&right.id));
        manifest
            .routes
            .sort_by(|left, right| left.id.cmp(&right.id));
        manifest
            .external_boundaries
            .sort_by(|left, right| left.id.cmp(&right.id));
        manifest.initial_mutations.sort_by_key(canonical_json);
        manifest
    }

    pub fn manifest_revision(&self) -> String {
        format!("sha256:{}", manifest_digest(&self.normalized()))
    }

    pub fn world_id(&self) -> String {
        format!("nw1-{}", manifest_digest(&self.normalized()))
    }

    pub fn service(&self, service_id: &str) -> Option<&NodeService> {
        self.nodes
            .iter()
            .flat_map(|node| &node.services)
            .find(|service| service.id == service_id)
    }
}

impl WorldState {
    fn base(manifest: &NetworkWorldManifest) -> Self {
        Self {
            schema_version: WORLD_SCHEMA_VERSION,
            world_id: manifest.world_id(),
            manifest_revision: manifest.manifest_revision(),
            runtime_revision: 0,
            phase: WorldPhase::Active,
            effect_semantics: EffectSemantics {
                service_reachability: EffectMode::OptInLoopbackFixture,
                link_state: EffectMode::ModeledOnly,
                latency_loss: EffectMode::ModeledOnly,
                routes: EffectMode::ModeledOnly,
                dns: EffectMode::ModeledOnly,
            },
            links: manifest
                .links
                .iter()
                .map(|link| {
                    (
                        link.id.clone(),
                        LinkRuntime {
                            state: LinkState::Up,
                            impairment: Impairment::default(),
                        },
                    )
                })
                .collect(),
            services: manifest
                .nodes
                .iter()
                .flat_map(|node| &node.services)
                .map(|service| (service.id.clone(), ServiceRuntime { reachable: true }))
                .collect(),
            routes: manifest
                .routes
                .iter()
                .map(|route| (route.id.clone(), RouteRuntime { enabled: true }))
                .collect(),
            identities: manifest
                .communication_identities
                .iter()
                .map(|identity| {
                    (
                        identity.id.clone(),
                        IdentityRuntime {
                            generation: 1,
                            revoked: false,
                        },
                    )
                })
                .collect(),
            dns_overrides: manifest
                .communication_identities
                .iter()
                .map(|identity| (identity.id.clone(), None))
                .collect(),
            egress_evidence: Vec::new(),
        }
    }

    pub(crate) fn baseline(manifest: &NetworkWorldManifest) -> Result<Self, String> {
        let mut state = Self::base(manifest);
        for mutation in &manifest.initial_mutations {
            state.apply_mutation(mutation)?;
        }
        state.runtime_revision = 0;
        Ok(state)
    }

    pub fn actor_view(&self) -> ActorView {
        ActorView {
            schema_version: WORLD_SCHEMA_VERSION,
            world_id: self.world_id.clone(),
            runtime_revision: self.runtime_revision,
            phase: self.phase,
            effect_semantics: self.effect_semantics.clone(),
            links: self.links.clone(),
            services: self.services.clone(),
            routes: self.routes.clone(),
            identities: self.identities.clone(),
            dns_overrides: self.dns_overrides.clone(),
        }
    }

    pub fn check_mutation(&self, mutation: &Mutation) -> Result<(), String> {
        match mutation {
            Mutation::SetServiceReachability { service_id, .. } => {
                require_runtime("service", service_id, &self.services)
            }
            Mutation::SetLinkState { link_id, .. } => require_runtime("link", link_id, &self.links),
            Mutation::SetImpairment {
                link_id,
                loss_basis_points,
                ..
            } => {
                require_runtime("link", link_id, &self.links)?;
                if *loss_basis_points > 10_000 {
                    return Err(ManifestError::InvalidLoss.to_string());
                }
                Ok(())
            }
            Mutation::SetRouteState { route_id, .. } => {
                require_runtime("route", route_id, &self.routes)
            }
            Mutation::SetDnsOverride { identity_id, .. }
            | Mutation::RotateIdentity { identity_id }
            | Mutation::RevokeIdentity { identity_id, .. } => {
                require_runtime("identity", identity_id, &self.identities)
            }
        }
    }

    pub fn apply_mutation(&mut self, mutation: &Mutation) -> Result<(), String> {
        self.check_mutation(mutation)?;
        match mutation {
            Mutation::SetServiceReachability {
                service_id,
                reachable,
            } => {
                self.services
                    .get_mut(service_id)
                    .ok_or_else(|| format!("unknown service `{service_id}`"))?
                    .reachable = *reachable;
            }
            Mutation::SetLinkState { link_id, state } => {
                self.links
                    .get_mut(link_id)
                    .ok_or_else(|| format!("unknown link `{link_id}`"))?
                    .state = *state;
            }
            Mutation::SetImpairment {
                link_id,
                latency_ms,
                loss_basis_points,
            } => {
                self.links
                    .get_mut(link_id)
                    .ok_or_else(|| format!("unknown link `{link_id}`"))?
                    .impairment = Impairment {
                    latency_ms: *latency_ms,
                    loss_basis_points: *loss_basis_points,
                };
            }
            Mutation::SetRouteState { route_id, enabled } => {
                self.routes
                    .get_mut(route_id)
                    .ok_or_else(|| format!("unknown route `{route_id}`"))?
                    .enabled = *enabled;
            }
            Mutation::SetDnsOverride {
                identity_id,
                address,
            } => {
                *self
                    .dns_overrides
                    .get_mut(identity_id)
                    .ok_or_else(|| format!("unknown identity `{identity_id}`"))? = *address;
            }
            Mutation::RotateIdentity { identity_id } => {
                let identity = self
                    .identities
                    .get_mut(identity_id)
                    .ok_or_else(|| format!("unknown identity `{identity_id}`"))?;
                identity.generation = identity
                    .generation
                    .checked_add(1)
                    .ok_or_else(|| format!("identity `{identity_id}` generation overflow"))?;
                identity.revoked = false;
            }
            Mutation::RevokeIdentity {
                identity_id,
                revoked,
            } => {
                self.identities
                    .get_mut(identity_id)
                    .ok_or_else(|| format!("unknown identity `{identity_id}`"))?
                    .revoked = *revoked;
            }
        }
        Ok(())
    }

    pub fn mutation_changes(&self, mutation: &Mutation) -> Result<bool, String> {
        self.check_mutation(mutation)?;
        Ok(match mutation {
            Mutation::SetServiceReachability {
                service_id,
                reachable,
            } => self.services[service_id].reachable != *reachable,
            Mutation::SetLinkState { link_id, state } => self.links[link_id].state != *state,
            Mutation::SetImpairment {
                link_id,
                latency_ms,
                loss_basis_points,
            } => {
                self.links[link_id].impairment
                    != (Impairment {
                        latency_ms: *latency_ms,
                        loss_basis_points: *loss_basis_points,
                    })
            }
            Mutation::SetRouteState { route_id, enabled } => {
                self.routes[route_id].enabled != *enabled
            }
            Mutation::SetDnsOverride {
                identity_id,
                address,
            } => self.dns_overrides[identity_id] != *address,
            Mutation::RotateIdentity { .. } => true,
            Mutation::RevokeIdentity {
                identity_id,
                revoked,
            } => self.identities[identity_id].revoked != *revoked,
        })
    }
}

impl Mutation {
    fn initial_slot(&self) -> String {
        match self {
            Self::SetServiceReachability { service_id, .. } => format!("service:{service_id}"),
            Self::SetLinkState { link_id, .. } => format!("link-state:{link_id}"),
            Self::SetImpairment { link_id, .. } => format!("impairment:{link_id}"),
            Self::SetRouteState { route_id, .. } => format!("route:{route_id}"),
            Self::SetDnsOverride { identity_id, .. } => format!("dns:{identity_id}"),
            Self::RotateIdentity { identity_id } | Self::RevokeIdentity { identity_id, .. } => {
                format!("identity:{identity_id}")
            }
        }
    }
}

fn validate_nonempty_size(collection: &'static str, size: usize) -> Result<(), ManifestError> {
    if size == 0 || size > MAX_ITEMS {
        return Err(ManifestError::InvalidCollectionSize { collection });
    }
    Ok(())
}

fn validate_max_size(collection: &'static str, size: usize) -> Result<(), ManifestError> {
    if size > MAX_ITEMS {
        return Err(ManifestError::InvalidCollectionSize { collection });
    }
    Ok(())
}

fn validate_id(kind: &'static str, id: &str) -> Result<(), ManifestError> {
    let mut chars = id.chars();
    let valid = id.len() <= MAX_ID_BYTES
        && chars
            .next()
            .is_some_and(|character| character.is_ascii_lowercase())
        && chars.all(|character| {
            character.is_ascii_lowercase()
                || character.is_ascii_digit()
                || matches!(character, '-' | '_')
        });
    if !valid {
        return Err(ManifestError::UnsafeId {
            kind,
            id: id.to_owned(),
        });
    }
    Ok(())
}

fn validate_text(kind: &'static str, text: &str) -> Result<(), ManifestError> {
    if text.is_empty() || text.len() > MAX_TEXT_BYTES || text.chars().any(char::is_control) {
        return Err(ManifestError::InvalidText { kind });
    }
    Ok(())
}

fn validate_cidr(kind: &'static str, id: &str, cidr: &str) -> Result<(), ManifestError> {
    validate_text("network prefix", cidr)?;
    let invalid = || ManifestError::InvalidNetworkPrefix {
        kind,
        id: id.to_owned(),
        cidr: cidr.to_owned(),
    };
    let (address, prefix) = cidr.split_once('/').ok_or_else(invalid)?;
    let address: IpAddr = address.parse().map_err(|_| invalid())?;
    let prefix: u8 = prefix.parse().map_err(|_| invalid())?;
    let maximum = if address.is_ipv4() { 32 } else { 128 };
    if prefix > maximum
        || cidr != format!("{address}/{prefix}")
        || !is_network_address(address, prefix)
    {
        return Err(invalid());
    }
    Ok(())
}

fn is_network_address(address: IpAddr, prefix: u8) -> bool {
    match address {
        IpAddr::V4(address) => {
            let bits = u32::from(address);
            let host_mask = if prefix == 32 { 0 } else { u32::MAX >> prefix };
            bits & host_mask == 0
        }
        IpAddr::V6(address) => {
            let bits = u128::from(address);
            let host_mask = if prefix == 128 {
                0
            } else {
                u128::MAX >> prefix
            };
            bits & host_mask == 0
        }
    }
}

fn collect_ids<'a>(
    kind: &'static str,
    ids: impl Iterator<Item = &'a String>,
) -> Result<BTreeSet<&'a str>, ManifestError> {
    let mut collected = BTreeSet::new();
    for id in ids {
        validate_id(kind, id)?;
        if !collected.insert(id.as_str()) {
            return Err(ManifestError::DuplicateId {
                kind,
                id: id.clone(),
            });
        }
    }
    Ok(collected)
}

fn require_reference(
    kind: &'static str,
    id: &str,
    target_kind: &'static str,
    target: &str,
    values: &BTreeSet<&str>,
) -> Result<(), ManifestError> {
    if !values.contains(target) {
        return Err(ManifestError::MissingReference {
            kind,
            id: id.to_owned(),
            target_kind,
            target: target.to_owned(),
        });
    }
    Ok(())
}

fn require_runtime<T>(kind: &str, id: &str, values: &BTreeMap<String, T>) -> Result<(), String> {
    if values.contains_key(id) {
        Ok(())
    } else {
        Err(format!("unknown {kind} `{id}`"))
    }
}

fn canonical_json<T: Serialize>(value: &T) -> Vec<u8> {
    serde_json::to_vec(value).expect("serializable world value")
}

fn manifest_digest(manifest: &NetworkWorldManifest) -> String {
    let mut hasher = Sha256::new();
    hasher.update(IDENTITY_DOMAIN);
    hasher.update(canonical_json(manifest));
    hasher
        .finalize()
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn manifest() -> NetworkWorldManifest {
        NetworkWorldManifest {
            schema_version: 1,
            name: "deterministic-world".into(),
            nodes: vec![
                Node {
                    id: "beta".into(),
                    subnet: "range".into(),
                    services: vec![],
                },
                Node {
                    id: "alpha".into(),
                    subnet: "range".into(),
                    services: vec![],
                },
            ],
            links: vec![Link {
                id: "alpha-beta".into(),
                node_a: "alpha".into(),
                node_b: "beta".into(),
            }],
            subnets: vec![Subnet {
                id: "range".into(),
                cidr: "10.77.0.0/24".into(),
                trust_zone: "inside".into(),
            }],
            trust_zones: vec![TrustZone {
                id: "inside".into(),
            }],
            communication_identities: vec![],
            routes: vec![],
            external_boundaries: vec![],
            initial_mutations: vec![],
        }
    }

    #[test]
    fn identity_is_stable_across_manifest_order() {
        let first = manifest();
        let mut second = first.clone();
        second.nodes.reverse();

        first.validate().unwrap();
        second.validate().unwrap();
        assert_eq!(first.world_id(), second.world_id());
        assert_eq!(first.manifest_revision(), second.manifest_revision());
    }

    #[test]
    fn invalid_initial_mutation_is_rejected_without_panicking() {
        let mut world = manifest();
        world.initial_mutations.push(Mutation::SetLinkState {
            link_id: "missing".into(),
            state: LinkState::Partitioned,
        });

        assert!(matches!(
            world.validate(),
            Err(ManifestError::InvalidInitialMutation(_))
        ));
    }
}
