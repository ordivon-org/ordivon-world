use thiserror::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[repr(u16)]
pub enum ProtocolErrorCode {
    NormalClosure = 0x0000,
    UnsupportedVersion = 0x0001,
    AuthenticationFailed = 0x0002,
    CapabilityMismatch = 0x0003,
    InvalidFrame = 0x0004,
    FrameTooLarge = 0x0005,
    ResourceLimit = 0x0006,
    DnsFailed = 0x0010,
    TargetRefused = 0x0011,
    TargetTimeout = 0x0012,
    TargetUnreachable = 0x0013,
    TargetDenied = 0x0014,
    UdpAssociationUnknown = 0x0020,
    DatagramTooLarge = 0x0021,
    UdpIdleTimeout = 0x0022,
    EdgeDraining = 0x0030,
    InternalError = 0x0031,
}

impl TryFrom<u16> for ProtocolErrorCode {
    type Error = WireError;

    fn try_from(value: u16) -> Result<Self, Self::Error> {
        let code = match value {
            0x0000 => Self::NormalClosure,
            0x0001 => Self::UnsupportedVersion,
            0x0002 => Self::AuthenticationFailed,
            0x0003 => Self::CapabilityMismatch,
            0x0004 => Self::InvalidFrame,
            0x0005 => Self::FrameTooLarge,
            0x0006 => Self::ResourceLimit,
            0x0010 => Self::DnsFailed,
            0x0011 => Self::TargetRefused,
            0x0012 => Self::TargetTimeout,
            0x0013 => Self::TargetUnreachable,
            0x0014 => Self::TargetDenied,
            0x0020 => Self::UdpAssociationUnknown,
            0x0021 => Self::DatagramTooLarge,
            0x0022 => Self::UdpIdleTimeout,
            0x0030 => Self::EdgeDraining,
            0x0031 => Self::InternalError,
            _ => return Err(WireError::UnknownErrorCode(value)),
        };
        Ok(code)
    }
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum WireError {
    #[error("unexpected end of input")]
    UnexpectedEof,
    #[error("invalid QUIC variable-length integer")]
    InvalidVarInt,
    #[error("value for {field} is too large: {actual} > {max}")]
    ValueTooLarge {
        field: &'static str,
        actual: u64,
        max: u64,
    },
    #[error("invalid UTF-8")]
    InvalidUtf8,
    #[error("invalid domain name")]
    InvalidDomain,
    #[error("invalid address type {0:#04x}")]
    InvalidAddressType(u8),
    #[error("invalid frame type {0:#04x}")]
    InvalidFrameType(u8),
    #[error("unknown critical frame type {0:#04x}")]
    UnknownCriticalFrame(u8),
    #[error("unknown protocol error code {0:#06x}")]
    UnknownErrorCode(u16),
    #[error("invalid error scope {0:#04x}")]
    InvalidErrorScope(u8),
    #[error("invalid stream kind {0:#04x}")]
    InvalidStreamKind(u8),
    #[error("invalid response status {0:#04x}")]
    InvalidResponseStatus(u8),
    #[error("trailing bytes after a complete value")]
    TrailingBytes,
    #[error("invalid state transition from {state} on {event}")]
    InvalidStateTransition {
        state: &'static str,
        event: &'static str,
    },
}
