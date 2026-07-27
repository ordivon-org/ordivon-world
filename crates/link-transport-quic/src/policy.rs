use link_wire::Address;

pub trait TargetPolicy: Send + Sync + 'static {
    fn allows(&self, target: &Address) -> bool;
}

#[derive(Debug, Default)]
pub struct LoopbackOnlyPolicy;

impl TargetPolicy for LoopbackOnlyPolicy {
    fn allows(&self, target: &Address) -> bool {
        match target {
            Address::Domain { host, .. } => host.eq_ignore_ascii_case("localhost"),
            Address::Ipv4 { address, .. } => address.is_loopback(),
            Address::Ipv6 { address, .. } => address.is_loopback(),
        }
    }
}
