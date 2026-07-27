mod codec;
mod error;
mod frame;
mod limits;
mod state;

pub use codec::{decode_varint, encode_varint};
pub use error::{ProtocolErrorCode, WireError};
pub use frame::{
    Address, Capabilities, ControlFrame, ErrorScope, FrameFlags, TcpOpen, TcpOpenResponse,
    UdpDatagram,
};
pub use limits::ProtocolLimits;
pub use state::{
    ConnectionEvent, ConnectionState, TcpRelayEvent, TcpRelayState, UdpAssociationEvent,
    UdpAssociationState,
};

pub const ALPN_V0: &[u8] = b"ordivon-baseline/0";
pub const PROTOCOL_MAJOR: u16 = 0;
pub const PROTOCOL_MINOR: u16 = 0;
