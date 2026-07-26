use crate::WireError;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionState {
    Disconnected,
    QuicHandshaking,
    Authenticated,
    Negotiating,
    Ready,
    Draining,
    Closed,
    Failed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionEvent {
    Start,
    QuicEstablished,
    BeginNegotiation,
    HelloAccepted,
    BeginDrain,
    TransportClosed,
    Fatal,
    Reset,
}

impl ConnectionState {
    pub fn transition(self, event: ConnectionEvent) -> Result<Self, WireError> {
        let next = match (self, event) {
            (Self::Disconnected, ConnectionEvent::Start) => Self::QuicHandshaking,
            (Self::QuicHandshaking, ConnectionEvent::QuicEstablished) => Self::Authenticated,
            (Self::Authenticated, ConnectionEvent::BeginNegotiation) => Self::Negotiating,
            (Self::Negotiating, ConnectionEvent::HelloAccepted) => Self::Ready,
            (Self::Ready, ConnectionEvent::BeginDrain) => Self::Draining,
            (Self::Ready | Self::Draining, ConnectionEvent::TransportClosed) => Self::Closed,
            (
                Self::QuicHandshaking
                | Self::Authenticated
                | Self::Negotiating
                | Self::Ready
                | Self::Draining,
                ConnectionEvent::Fatal,
            ) => Self::Failed,
            (Self::Closed | Self::Failed, ConnectionEvent::Reset) => Self::Disconnected,
            _ => {
                return Err(WireError::InvalidStateTransition {
                    state: self.name(),
                    event: event.name(),
                });
            }
        };
        Ok(next)
    }

    const fn name(self) -> &'static str {
        match self {
            Self::Disconnected => "disconnected",
            Self::QuicHandshaking => "quic_handshaking",
            Self::Authenticated => "authenticated",
            Self::Negotiating => "negotiating",
            Self::Ready => "ready",
            Self::Draining => "draining",
            Self::Closed => "closed",
            Self::Failed => "failed",
        }
    }
}

impl ConnectionEvent {
    const fn name(self) -> &'static str {
        match self {
            Self::Start => "start",
            Self::QuicEstablished => "quic_established",
            Self::BeginNegotiation => "begin_negotiation",
            Self::HelloAccepted => "hello_accepted",
            Self::BeginDrain => "begin_drain",
            Self::TransportClosed => "transport_closed",
            Self::Fatal => "fatal",
            Self::Reset => "reset",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TcpRelayState {
    Created,
    Opening,
    Relaying,
    HalfClosedLocal,
    HalfClosedRemote,
    Closed,
    Failed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TcpRelayEvent {
    SendOpen,
    OpenOk,
    OpenError,
    LocalEof,
    RemoteEof,
    PeerClosed,
    Reset,
}

impl TcpRelayState {
    pub fn transition(self, event: TcpRelayEvent) -> Result<Self, WireError> {
        let next = match (self, event) {
            (Self::Created, TcpRelayEvent::SendOpen) => Self::Opening,
            (Self::Opening, TcpRelayEvent::OpenOk) => Self::Relaying,
            (Self::Opening, TcpRelayEvent::OpenError) => Self::Failed,
            (Self::Relaying, TcpRelayEvent::LocalEof) => Self::HalfClosedLocal,
            (Self::Relaying, TcpRelayEvent::RemoteEof) => Self::HalfClosedRemote,
            (Self::HalfClosedLocal, TcpRelayEvent::RemoteEof)
            | (Self::HalfClosedRemote, TcpRelayEvent::LocalEof)
            | (Self::Relaying, TcpRelayEvent::PeerClosed) => Self::Closed,
            (
                Self::Opening | Self::Relaying | Self::HalfClosedLocal | Self::HalfClosedRemote,
                TcpRelayEvent::Reset,
            ) => Self::Failed,
            _ => {
                return Err(WireError::InvalidStateTransition {
                    state: self.name(),
                    event: event.name(),
                });
            }
        };
        Ok(next)
    }

    const fn name(self) -> &'static str {
        match self {
            Self::Created => "created",
            Self::Opening => "opening",
            Self::Relaying => "relaying",
            Self::HalfClosedLocal => "half_closed_local",
            Self::HalfClosedRemote => "half_closed_remote",
            Self::Closed => "closed",
            Self::Failed => "failed",
        }
    }
}

impl TcpRelayEvent {
    const fn name(self) -> &'static str {
        match self {
            Self::SendOpen => "send_open",
            Self::OpenOk => "open_ok",
            Self::OpenError => "open_error",
            Self::LocalEof => "local_eof",
            Self::RemoteEof => "remote_eof",
            Self::PeerClosed => "peer_closed",
            Self::Reset => "reset",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UdpAssociationState {
    Created,
    Active,
    Idle,
    Closed,
    Failed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UdpAssociationEvent {
    Activate,
    Activity,
    IdleTimer,
    Close,
    Error,
}

impl UdpAssociationState {
    pub fn transition(self, event: UdpAssociationEvent) -> Result<Self, WireError> {
        let next = match (self, event) {
            (Self::Created, UdpAssociationEvent::Activate) => Self::Active,
            (Self::Active, UdpAssociationEvent::Activity)
            | (Self::Idle, UdpAssociationEvent::Activity) => Self::Active,
            (Self::Active, UdpAssociationEvent::IdleTimer) => Self::Idle,
            (Self::Created | Self::Active | Self::Idle, UdpAssociationEvent::Close) => Self::Closed,
            (Self::Created | Self::Active | Self::Idle, UdpAssociationEvent::Error) => Self::Failed,
            _ => {
                return Err(WireError::InvalidStateTransition {
                    state: self.name(),
                    event: event.name(),
                });
            }
        };
        Ok(next)
    }

    const fn name(self) -> &'static str {
        match self {
            Self::Created => "created",
            Self::Active => "active",
            Self::Idle => "idle",
            Self::Closed => "closed",
            Self::Failed => "failed",
        }
    }
}

impl UdpAssociationEvent {
    const fn name(self) -> &'static str {
        match self {
            Self::Activate => "activate",
            Self::Activity => "activity",
            Self::IdleTimer => "idle_timer",
            Self::Close => "close",
            Self::Error => "error",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn connection_reaches_ready_only_through_negotiation() {
        let state = ConnectionState::Disconnected
            .transition(ConnectionEvent::Start)
            .expect("start")
            .transition(ConnectionEvent::QuicEstablished)
            .expect("quic")
            .transition(ConnectionEvent::BeginNegotiation)
            .expect("negotiate")
            .transition(ConnectionEvent::HelloAccepted)
            .expect("hello");
        assert_eq!(state, ConnectionState::Ready);
    }

    #[test]
    fn tcp_half_close_requires_other_eof_to_close() {
        let state = TcpRelayState::Created
            .transition(TcpRelayEvent::SendOpen)
            .expect("open")
            .transition(TcpRelayEvent::OpenOk)
            .expect("ok")
            .transition(TcpRelayEvent::LocalEof)
            .expect("local eof");
        assert_eq!(state, TcpRelayState::HalfClosedLocal);
        assert_eq!(
            state
                .transition(TcpRelayEvent::RemoteEof)
                .expect("remote eof"),
            TcpRelayState::Closed
        );
    }

    #[test]
    fn invalid_transition_is_rejected() {
        assert!(matches!(
            ConnectionState::Disconnected.transition(ConnectionEvent::HelloAccepted),
            Err(WireError::InvalidStateTransition { .. })
        ));
    }
}
