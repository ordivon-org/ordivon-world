#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProtocolLimits {
    pub max_control_frame_len: u32,
    pub max_domain_len: u16,
    pub max_build_len: u16,
    pub max_error_detail_len: u16,
    pub max_tcp_streams: u32,
    pub max_pending_tcp: u32,
    pub max_udp_associations: u32,
    pub max_udp_payload: u16,
    pub udp_idle_timeout_secs: u16,
}

impl Default for ProtocolLimits {
    fn default() -> Self {
        Self {
            max_control_frame_len: 16 * 1024,
            max_domain_len: 253,
            max_build_len: 64,
            max_error_detail_len: 256,
            max_tcp_streams: 128,
            max_pending_tcp: 32,
            max_udp_associations: 64,
            max_udp_payload: 1200,
            udp_idle_timeout_secs: 60,
        }
    }
}
