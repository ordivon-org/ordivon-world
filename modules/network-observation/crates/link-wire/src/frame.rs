use std::net::{Ipv4Addr, Ipv6Addr};

use crate::codec::{Cursor, encode_varint, write_string};
use crate::{ProtocolErrorCode, ProtocolLimits, WireError};

const FRAME_HELLO: u8 = 0x01;
const FRAME_HELLO_OK: u8 = 0x02;
const FRAME_OPEN_UDP: u8 = 0x10;
const FRAME_CLOSE_UDP: u8 = 0x11;
const FRAME_OPEN_UDP_OK: u8 = 0x12;
const FRAME_PING: u8 = 0x20;
const FRAME_PONG: u8 = 0x21;
const FRAME_DRAIN: u8 = 0x30;
const FRAME_GO_AWAY: u8 = 0x31;
const FRAME_ERROR: u8 = 0x7f;

const STREAM_KIND_TCP: u8 = 0x01;
const UDP_DATAGRAM_KIND: u8 = 0x01;
const TCP_RESPONSE_OK: u8 = 0x00;
const TCP_RESPONSE_ERROR: u8 = 0x01;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FrameFlags(u8);

impl FrameFlags {
    pub const NONE: Self = Self(0);
    pub const CRITICAL: Self = Self(0x01);

    pub const fn bits(self) -> u8 {
        self.0
    }

    pub const fn from_bits(bits: u8) -> Self {
        Self(bits)
    }

    pub const fn is_critical(self) -> bool {
        self.0 & Self::CRITICAL.0 != 0
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Capabilities(u64);

impl Capabilities {
    pub const NONE: Self = Self(0);
    pub const TCP_RELAY: Self = Self(1 << 0);
    pub const UDP_RELAY: Self = Self(1 << 1);

    pub const fn bits(self) -> u64 {
        self.0
    }

    pub const fn from_bits(bits: u64) -> Self {
        Self(bits)
    }

    pub const fn contains(self, other: Self) -> bool {
        self.0 & other.0 == other.0
    }

    pub const fn union(self, other: Self) -> Self {
        Self(self.0 | other.0)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Address {
    Domain { host: String, port: u16 },
    Ipv4 { address: Ipv4Addr, port: u16 },
    Ipv6 { address: Ipv6Addr, port: u16 },
}

impl Address {
    fn encode(&self, output: &mut Vec<u8>, limits: &ProtocolLimits) -> Result<(), WireError> {
        match self {
            Self::Domain { host, port } => {
                validate_domain(host, limits.max_domain_len as usize)?;
                output.push(0x00);
                write_string(output, "domain", host, limits.max_domain_len as usize)?;
                output.extend_from_slice(&port.to_be_bytes());
            }
            Self::Ipv4 { address, port } => {
                output.push(0x01);
                output.extend_from_slice(&address.octets());
                output.extend_from_slice(&port.to_be_bytes());
            }
            Self::Ipv6 { address, port } => {
                output.push(0x02);
                output.extend_from_slice(&address.octets());
                output.extend_from_slice(&port.to_be_bytes());
            }
        }
        Ok(())
    }

    fn decode(cursor: &mut Cursor<'_>, limits: &ProtocolLimits) -> Result<Self, WireError> {
        let address = match cursor.read_u8()? {
            0x00 => {
                let host = cursor.read_string("domain", limits.max_domain_len as usize)?;
                validate_domain(&host, limits.max_domain_len as usize)?;
                let port = cursor.read_u16()?;
                Self::Domain { host, port }
            }
            0x01 => {
                let bytes = cursor.read_exact(4)?;
                let address = Ipv4Addr::new(bytes[0], bytes[1], bytes[2], bytes[3]);
                let port = cursor.read_u16()?;
                Self::Ipv4 { address, port }
            }
            0x02 => {
                let bytes = cursor.read_exact(16)?;
                let mut octets = [0u8; 16];
                octets.copy_from_slice(bytes);
                let address = Ipv6Addr::from(octets);
                let port = cursor.read_u16()?;
                Self::Ipv6 { address, port }
            }
            value => return Err(WireError::InvalidAddressType(value)),
        };
        Ok(address)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorScope {
    Connection,
    Request,
    Association,
}

impl ErrorScope {
    const fn code(self) -> u8 {
        match self {
            Self::Connection => 0x00,
            Self::Request => 0x01,
            Self::Association => 0x02,
        }
    }

    fn from_code(value: u8) -> Result<Self, WireError> {
        match value {
            0x00 => Ok(Self::Connection),
            0x01 => Ok(Self::Request),
            0x02 => Ok(Self::Association),
            other => Err(WireError::InvalidErrorScope(other)),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ControlFrame {
    Hello {
        request_id: u64,
        minor_version: u16,
        capabilities: Capabilities,
        device_id: [u8; 16],
        client_build: String,
    },
    HelloOk {
        request_id: u64,
        minor_version: u16,
        capabilities: Capabilities,
        session_id: [u8; 16],
        server_build: String,
        limits: ProtocolLimits,
    },
    OpenUdp {
        request_id: u64,
        association_id: u64,
        idle_timeout_secs: u16,
    },
    OpenUdpOk {
        request_id: u64,
        association_id: u64,
        idle_timeout_secs: u16,
    },
    CloseUdp {
        request_id: u64,
        association_id: u64,
        code: ProtocolErrorCode,
    },
    Ping {
        request_id: u64,
        nonce: u64,
    },
    Pong {
        request_id: u64,
        nonce: u64,
    },
    Drain {
        request_id: u64,
        retry_after_ms: u32,
    },
    GoAway {
        request_id: u64,
        code: ProtocolErrorCode,
    },
    Error {
        request_id: u64,
        code: ProtocolErrorCode,
        scope: ErrorScope,
        related_id: u64,
        detail: String,
    },
    Unknown {
        frame_type: u8,
        flags: FrameFlags,
        request_id: u64,
        payload: Vec<u8>,
    },
}

impl ControlFrame {
    pub fn encode(&self, limits: &ProtocolLimits) -> Result<Vec<u8>, WireError> {
        let (frame_type, flags, request_id, payload) = self.encode_parts(limits)?;
        let mut body = Vec::with_capacity(2 + payload.len() + 8);
        body.push(frame_type);
        body.push(flags.bits());
        encode_varint(request_id, &mut body)?;
        body.extend_from_slice(&payload);

        if body.len() > limits.max_control_frame_len as usize {
            return Err(WireError::ValueTooLarge {
                field: "control_frame",
                actual: body.len() as u64,
                max: limits.max_control_frame_len as u64,
            });
        }

        let mut output = Vec::with_capacity(body.len() + 8);
        encode_varint(body.len() as u64, &mut output)?;
        output.extend_from_slice(&body);
        Ok(output)
    }

    pub fn decode(bytes: &[u8], limits: &ProtocolLimits) -> Result<Self, WireError> {
        let mut envelope = Cursor::new(bytes);
        let body_len =
            usize::try_from(envelope.read_varint()?).map_err(|_| WireError::ValueTooLarge {
                field: "control_frame",
                actual: u64::MAX,
                max: limits.max_control_frame_len as u64,
            })?;
        if body_len > limits.max_control_frame_len as usize {
            return Err(WireError::ValueTooLarge {
                field: "control_frame",
                actual: body_len as u64,
                max: limits.max_control_frame_len as u64,
            });
        }
        let body = envelope.read_exact(body_len)?;
        envelope.finish()?;

        let mut cursor = Cursor::new(body);
        let frame_type = cursor.read_u8()?;
        let flags = FrameFlags::from_bits(cursor.read_u8()?);
        let request_id = cursor.read_varint()?;
        let frame = match frame_type {
            FRAME_HELLO => Self::Hello {
                request_id,
                minor_version: cursor.read_u16()?,
                capabilities: Capabilities::from_bits(cursor.read_u64()?),
                device_id: read_id(&mut cursor)?,
                client_build: cursor.read_string("client_build", limits.max_build_len as usize)?,
            },
            FRAME_HELLO_OK => Self::HelloOk {
                request_id,
                minor_version: cursor.read_u16()?,
                capabilities: Capabilities::from_bits(cursor.read_u64()?),
                session_id: read_id(&mut cursor)?,
                server_build: cursor.read_string("server_build", limits.max_build_len as usize)?,
                limits: decode_limits(&mut cursor)?,
            },
            FRAME_OPEN_UDP => Self::OpenUdp {
                request_id,
                association_id: cursor.read_varint()?,
                idle_timeout_secs: cursor.read_u16()?,
            },
            FRAME_OPEN_UDP_OK => Self::OpenUdpOk {
                request_id,
                association_id: cursor.read_varint()?,
                idle_timeout_secs: cursor.read_u16()?,
            },
            FRAME_CLOSE_UDP => Self::CloseUdp {
                request_id,
                association_id: cursor.read_varint()?,
                code: ProtocolErrorCode::try_from(cursor.read_u16()?)?,
            },
            FRAME_PING => Self::Ping {
                request_id,
                nonce: cursor.read_u64()?,
            },
            FRAME_PONG => Self::Pong {
                request_id,
                nonce: cursor.read_u64()?,
            },
            FRAME_DRAIN => Self::Drain {
                request_id,
                retry_after_ms: cursor.read_u32()?,
            },
            FRAME_GO_AWAY => Self::GoAway {
                request_id,
                code: ProtocolErrorCode::try_from(cursor.read_u16()?)?,
            },
            FRAME_ERROR => Self::Error {
                request_id,
                code: ProtocolErrorCode::try_from(cursor.read_u16()?)?,
                scope: ErrorScope::from_code(cursor.read_u8()?)?,
                related_id: cursor.read_varint()?,
                detail: cursor.read_string("error_detail", limits.max_error_detail_len as usize)?,
            },
            unknown if flags.is_critical() => return Err(WireError::UnknownCriticalFrame(unknown)),
            unknown => {
                let payload = cursor.remaining().to_vec();
                return Ok(Self::Unknown {
                    frame_type: unknown,
                    flags,
                    request_id,
                    payload,
                });
            }
        };
        cursor.finish()?;
        Ok(frame)
    }

    fn encode_parts(
        &self,
        limits: &ProtocolLimits,
    ) -> Result<(u8, FrameFlags, u64, Vec<u8>), WireError> {
        let mut payload = Vec::new();
        let parts = match self {
            Self::Hello {
                request_id,
                minor_version,
                capabilities,
                device_id,
                client_build,
            } => {
                payload.extend_from_slice(&minor_version.to_be_bytes());
                payload.extend_from_slice(&capabilities.bits().to_be_bytes());
                payload.extend_from_slice(device_id);
                write_string(
                    &mut payload,
                    "client_build",
                    client_build,
                    limits.max_build_len as usize,
                )?;
                (FRAME_HELLO, FrameFlags::CRITICAL, *request_id)
            }
            Self::HelloOk {
                request_id,
                minor_version,
                capabilities,
                session_id,
                server_build,
                limits: negotiated_limits,
            } => {
                payload.extend_from_slice(&minor_version.to_be_bytes());
                payload.extend_from_slice(&capabilities.bits().to_be_bytes());
                payload.extend_from_slice(session_id);
                write_string(
                    &mut payload,
                    "server_build",
                    server_build,
                    limits.max_build_len as usize,
                )?;
                encode_limits(&mut payload, negotiated_limits);
                (FRAME_HELLO_OK, FrameFlags::CRITICAL, *request_id)
            }
            Self::OpenUdp {
                request_id,
                association_id,
                idle_timeout_secs,
            } => {
                encode_varint(*association_id, &mut payload)?;
                payload.extend_from_slice(&idle_timeout_secs.to_be_bytes());
                (FRAME_OPEN_UDP, FrameFlags::CRITICAL, *request_id)
            }
            Self::OpenUdpOk {
                request_id,
                association_id,
                idle_timeout_secs,
            } => {
                encode_varint(*association_id, &mut payload)?;
                payload.extend_from_slice(&idle_timeout_secs.to_be_bytes());
                (FRAME_OPEN_UDP_OK, FrameFlags::CRITICAL, *request_id)
            }
            Self::CloseUdp {
                request_id,
                association_id,
                code,
            } => {
                encode_varint(*association_id, &mut payload)?;
                payload.extend_from_slice(&(*code as u16).to_be_bytes());
                (FRAME_CLOSE_UDP, FrameFlags::NONE, *request_id)
            }
            Self::Ping { request_id, nonce } => {
                payload.extend_from_slice(&nonce.to_be_bytes());
                (FRAME_PING, FrameFlags::NONE, *request_id)
            }
            Self::Pong { request_id, nonce } => {
                payload.extend_from_slice(&nonce.to_be_bytes());
                (FRAME_PONG, FrameFlags::NONE, *request_id)
            }
            Self::Drain {
                request_id,
                retry_after_ms,
            } => {
                payload.extend_from_slice(&retry_after_ms.to_be_bytes());
                (FRAME_DRAIN, FrameFlags::CRITICAL, *request_id)
            }
            Self::GoAway { request_id, code } => {
                payload.extend_from_slice(&(*code as u16).to_be_bytes());
                (FRAME_GO_AWAY, FrameFlags::CRITICAL, *request_id)
            }
            Self::Error {
                request_id,
                code,
                scope,
                related_id,
                detail,
            } => {
                payload.extend_from_slice(&(*code as u16).to_be_bytes());
                payload.push(scope.code());
                encode_varint(*related_id, &mut payload)?;
                write_string(
                    &mut payload,
                    "error_detail",
                    detail,
                    limits.max_error_detail_len as usize,
                )?;
                (FRAME_ERROR, FrameFlags::CRITICAL, *request_id)
            }
            Self::Unknown {
                frame_type,
                flags,
                request_id,
                payload: unknown_payload,
            } => {
                payload.extend_from_slice(unknown_payload);
                (*frame_type, *flags, *request_id)
            }
        };
        Ok((parts.0, parts.1, parts.2, payload))
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TcpOpen {
    pub request_id: u64,
    pub flags: u8,
    pub target: Address,
}

impl TcpOpen {
    pub fn encode(&self, limits: &ProtocolLimits) -> Result<Vec<u8>, WireError> {
        let mut output = vec![STREAM_KIND_TCP];
        encode_varint(self.request_id, &mut output)?;
        output.push(self.flags);
        self.target.encode(&mut output, limits)?;
        Ok(output)
    }

    pub fn decode(bytes: &[u8], limits: &ProtocolLimits) -> Result<Self, WireError> {
        let mut cursor = Cursor::new(bytes);
        let kind = cursor.read_u8()?;
        if kind != STREAM_KIND_TCP {
            return Err(WireError::InvalidStreamKind(kind));
        }
        let request_id = cursor.read_varint()?;
        let flags = cursor.read_u8()?;
        let target = Address::decode(&mut cursor, limits)?;
        cursor.finish()?;
        Ok(Self {
            request_id,
            flags,
            target,
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TcpOpenResponse {
    Ok {
        request_id: u64,
    },
    Error {
        request_id: u64,
        code: ProtocolErrorCode,
    },
}

impl TcpOpenResponse {
    pub fn encode(&self) -> Result<Vec<u8>, WireError> {
        let mut output = Vec::new();
        match self {
            Self::Ok { request_id } => {
                output.push(TCP_RESPONSE_OK);
                encode_varint(*request_id, &mut output)?;
            }
            Self::Error { request_id, code } => {
                output.push(TCP_RESPONSE_ERROR);
                encode_varint(*request_id, &mut output)?;
                output.extend_from_slice(&(*code as u16).to_be_bytes());
            }
        }
        Ok(output)
    }

    pub fn decode(bytes: &[u8]) -> Result<Self, WireError> {
        let mut cursor = Cursor::new(bytes);
        let response = match cursor.read_u8()? {
            TCP_RESPONSE_OK => Self::Ok {
                request_id: cursor.read_varint()?,
            },
            TCP_RESPONSE_ERROR => Self::Error {
                request_id: cursor.read_varint()?,
                code: ProtocolErrorCode::try_from(cursor.read_u16()?)?,
            },
            status => return Err(WireError::InvalidResponseStatus(status)),
        };
        cursor.finish()?;
        Ok(response)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UdpDatagram {
    pub association_id: u64,
    pub address: Address,
    pub payload: Vec<u8>,
}

impl UdpDatagram {
    pub fn encode(&self, limits: &ProtocolLimits) -> Result<Vec<u8>, WireError> {
        if self.payload.len() > limits.max_udp_payload as usize {
            return Err(WireError::ValueTooLarge {
                field: "udp_payload",
                actual: self.payload.len() as u64,
                max: limits.max_udp_payload as u64,
            });
        }
        let mut output = vec![UDP_DATAGRAM_KIND];
        encode_varint(self.association_id, &mut output)?;
        self.address.encode(&mut output, limits)?;
        output.extend_from_slice(&self.payload);
        Ok(output)
    }

    pub fn decode(bytes: &[u8], limits: &ProtocolLimits) -> Result<Self, WireError> {
        let mut cursor = Cursor::new(bytes);
        let kind = cursor.read_u8()?;
        if kind != UDP_DATAGRAM_KIND {
            return Err(WireError::InvalidFrameType(kind));
        }
        let association_id = cursor.read_varint()?;
        let address = Address::decode(&mut cursor, limits)?;
        let payload = cursor.remaining().to_vec();
        if payload.len() > limits.max_udp_payload as usize {
            return Err(WireError::ValueTooLarge {
                field: "udp_payload",
                actual: payload.len() as u64,
                max: limits.max_udp_payload as u64,
            });
        }
        Ok(Self {
            association_id,
            address,
            payload,
        })
    }
}

fn validate_domain(domain: &str, max: usize) -> Result<(), WireError> {
    if domain.is_empty() || domain.len() > max || !domain.is_ascii() {
        return Err(WireError::InvalidDomain);
    }
    for label in domain.split('.') {
        if label.is_empty() || label.len() > 63 {
            return Err(WireError::InvalidDomain);
        }
        let bytes = label.as_bytes();
        if bytes.first() == Some(&b'-') || bytes.last() == Some(&b'-') {
            return Err(WireError::InvalidDomain);
        }
        if !bytes
            .iter()
            .all(|byte| byte.is_ascii_alphanumeric() || *byte == b'-')
        {
            return Err(WireError::InvalidDomain);
        }
    }
    Ok(())
}

fn read_id(cursor: &mut Cursor<'_>) -> Result<[u8; 16], WireError> {
    let bytes = cursor.read_exact(16)?;
    let mut id = [0u8; 16];
    id.copy_from_slice(bytes);
    Ok(id)
}

fn encode_limits(output: &mut Vec<u8>, limits: &ProtocolLimits) {
    output.extend_from_slice(&limits.max_control_frame_len.to_be_bytes());
    output.extend_from_slice(&limits.max_domain_len.to_be_bytes());
    output.extend_from_slice(&limits.max_build_len.to_be_bytes());
    output.extend_from_slice(&limits.max_error_detail_len.to_be_bytes());
    output.extend_from_slice(&limits.max_tcp_streams.to_be_bytes());
    output.extend_from_slice(&limits.max_pending_tcp.to_be_bytes());
    output.extend_from_slice(&limits.max_udp_associations.to_be_bytes());
    output.extend_from_slice(&limits.max_udp_payload.to_be_bytes());
    output.extend_from_slice(&limits.udp_idle_timeout_secs.to_be_bytes());
}

fn decode_limits(cursor: &mut Cursor<'_>) -> Result<ProtocolLimits, WireError> {
    Ok(ProtocolLimits {
        max_control_frame_len: cursor.read_u32()?,
        max_domain_len: cursor.read_u16()?,
        max_build_len: cursor.read_u16()?,
        max_error_detail_len: cursor.read_u16()?,
        max_tcp_streams: cursor.read_u32()?,
        max_pending_tcp: cursor.read_u32()?,
        max_udp_associations: cursor.read_u32()?,
        max_udp_payload: cursor.read_u16()?,
        udp_idle_timeout_secs: cursor.read_u16()?,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_round_trips() {
        let limits = ProtocolLimits::default();
        let frame = ControlFrame::Hello {
            request_id: 7,
            minor_version: 0,
            capabilities: Capabilities::TCP_RELAY.union(Capabilities::UDP_RELAY),
            device_id: [3; 16],
            client_build: "edge-client/0.1".into(),
        };

        let encoded = frame.encode(&limits).expect("encode");
        let decoded = ControlFrame::decode(&encoded, &limits).expect("decode");
        assert_eq!(decoded, frame);
    }

    #[test]
    fn hello_ok_round_trips_limits() {
        let limits = ProtocolLimits::default();
        let frame = ControlFrame::HelloOk {
            request_id: 8,
            minor_version: 0,
            capabilities: Capabilities::TCP_RELAY.union(Capabilities::UDP_RELAY),
            session_id: [9; 16],
            server_build: "link-console/0.1".into(),
            limits,
        };
        let encoded = frame.encode(&limits).expect("encode");
        assert_eq!(
            ControlFrame::decode(&encoded, &limits).expect("decode"),
            frame
        );
    }

    #[test]
    fn open_udp_ok_round_trips() {
        let limits = ProtocolLimits::default();
        let frame = ControlFrame::OpenUdpOk {
            request_id: 10,
            association_id: 41,
            idle_timeout_secs: 60,
        };
        let encoded = frame.encode(&limits).expect("encode");
        assert_eq!(
            ControlFrame::decode(&encoded, &limits).expect("decode"),
            frame
        );
    }

    #[test]
    fn unknown_noncritical_frame_is_preserved() {
        let limits = ProtocolLimits::default();
        let frame = ControlFrame::Unknown {
            frame_type: 0x55,
            flags: FrameFlags::NONE,
            request_id: 12,
            payload: vec![1, 2, 3],
        };
        let encoded = frame.encode(&limits).expect("encode");
        assert_eq!(
            ControlFrame::decode(&encoded, &limits).expect("decode"),
            frame
        );
    }

    #[test]
    fn unknown_critical_frame_is_rejected() {
        let limits = ProtocolLimits::default();
        let frame = ControlFrame::Unknown {
            frame_type: 0x56,
            flags: FrameFlags::CRITICAL,
            request_id: 13,
            payload: vec![],
        };
        let encoded = frame.encode(&limits).expect("encode");
        assert_eq!(
            ControlFrame::decode(&encoded, &limits),
            Err(WireError::UnknownCriticalFrame(0x56))
        );
    }

    #[test]
    fn tcp_open_round_trips_domain() {
        let limits = ProtocolLimits::default();
        let open = TcpOpen {
            request_id: 99,
            flags: 0,
            target: Address::Domain {
                host: "example.com".into(),
                port: 443,
            },
        };
        let encoded = open.encode(&limits).expect("encode");
        assert_eq!(TcpOpen::decode(&encoded, &limits).expect("decode"), open);
    }

    #[test]
    fn invalid_domain_is_rejected() {
        let limits = ProtocolLimits::default();
        let open = TcpOpen {
            request_id: 1,
            flags: 0,
            target: Address::Domain {
                host: "bad_domain.example".into(),
                port: 443,
            },
        };
        assert_eq!(open.encode(&limits), Err(WireError::InvalidDomain));
    }

    #[test]
    fn udp_payload_limit_is_enforced() {
        let limits = ProtocolLimits {
            max_udp_payload: 4,
            ..ProtocolLimits::default()
        };
        let datagram = UdpDatagram {
            association_id: 1,
            address: Address::Ipv4 {
                address: Ipv4Addr::LOCALHOST,
                port: 53,
            },
            payload: vec![0; 5],
        };
        assert!(matches!(
            datagram.encode(&limits),
            Err(WireError::ValueTooLarge {
                field: "udp_payload",
                ..
            })
        ));
    }
}
