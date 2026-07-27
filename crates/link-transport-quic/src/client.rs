use std::net::SocketAddr;
use std::sync::atomic::{AtomicU64, Ordering};

use anyhow::{Context, Result, bail};
use bytes::Bytes;
use link_wire::{
    Address, Capabilities, ControlFrame, PROTOCOL_MINOR, ProtocolLimits, TcpOpen, TcpOpenResponse,
    UdpDatagram,
};
use quinn::{ClientConfig, Connection, Endpoint, RecvStream, SendStream, VarInt};
use tokio::io::AsyncWriteExt;

use crate::ProtocolRejection;
use crate::io::{read_control_frame, read_tcp_response, write_control_frame};

pub struct BaselineClient {
    endpoint: Endpoint,
    connection: Connection,
    control_send: SendStream,
    control_recv: RecvStream,
    limits: ProtocolLimits,
    next_request_id: AtomicU64,
}

impl BaselineClient {
    pub async fn connect(
        bind: SocketAddr,
        config: ClientConfig,
        remote: SocketAddr,
        server_name: &str,
        device_id: [u8; 16],
        client_build: impl Into<String>,
    ) -> Result<Self> {
        let mut endpoint = Endpoint::client(bind).context("bind QUIC client endpoint")?;
        endpoint.set_default_client_config(config);
        let connection = endpoint
            .connect(remote, server_name)
            .context("start QUIC connection")?
            .await
            .context("complete QUIC and mTLS handshake")?;
        let (mut control_send, mut control_recv) =
            connection.open_bi().await.context("open control stream")?;
        let local_limits = ProtocolLimits::default();
        let hello = ControlFrame::Hello {
            request_id: 1,
            minor_version: PROTOCOL_MINOR,
            capabilities: Capabilities::TCP_RELAY.union(Capabilities::UDP_RELAY),
            device_id,
            client_build: client_build.into(),
        };
        write_control_frame(&mut control_send, &hello, &local_limits).await?;
        let response = read_control_frame(&mut control_recv, &local_limits).await?;
        let limits = match response {
            ControlFrame::HelloOk {
                request_id: 1,
                minor_version,
                capabilities,
                limits,
                ..
            } if minor_version == PROTOCOL_MINOR
                && capabilities.contains(Capabilities::TCP_RELAY)
                && capabilities.contains(Capabilities::UDP_RELAY) =>
            {
                limits
            }
            ControlFrame::Error {
                code,
                scope,
                related_id,
                detail,
                ..
            } => {
                return Err(ProtocolRejection {
                    code,
                    scope,
                    related_id,
                    detail,
                }
                .into());
            }
            other => bail!("unexpected HELLO response: {other:?}"),
        };

        Ok(Self {
            endpoint,
            connection,
            control_send,
            control_recv,
            limits,
            next_request_id: AtomicU64::new(2),
        })
    }

    pub fn limits(&self) -> ProtocolLimits {
        self.limits
    }

    pub fn remote_address(&self) -> SocketAddr {
        self.connection.remote_address()
    }

    pub async fn open_tcp(&self, target: Address) -> Result<(SendStream, RecvStream)> {
        let request_id = self.next_request_id.fetch_add(1, Ordering::Relaxed);
        let (mut send, mut recv) = self
            .connection
            .open_bi()
            .await
            .context("open TCP relay stream")?;
        let open = TcpOpen {
            request_id,
            flags: 0,
            target,
        };
        let encoded = open.encode(&self.limits).context("encode TCP open")?;
        send.write_all(&encoded)
            .await
            .context("write TCP open preface")?;
        send.flush().await.context("flush TCP open preface")?;
        match read_tcp_response(&mut recv).await? {
            TcpOpenResponse::Ok {
                request_id: response_id,
            } if response_id == request_id => Ok((send, recv)),
            TcpOpenResponse::Error {
                request_id: response_id,
                code,
            } if response_id == request_id => {
                Err(ProtocolRejection::request(code, request_id, "TCP relay open rejected").into())
            }
            response => bail!("mismatched TCP open response: {response:?}"),
        }
    }

    pub async fn open_udp(&mut self, association_id: u64) -> Result<u16> {
        let request_id = self.next_request_id.fetch_add(1, Ordering::Relaxed);
        let frame = ControlFrame::OpenUdp {
            request_id,
            association_id,
            idle_timeout_secs: self.limits.udp_idle_timeout_secs,
        };
        write_control_frame(&mut self.control_send, &frame, &self.limits).await?;
        match read_control_frame(&mut self.control_recv, &self.limits).await? {
            ControlFrame::OpenUdpOk {
                request_id: response_id,
                association_id: response_association,
                idle_timeout_secs,
            } if response_id == request_id && response_association == association_id => {
                Ok(idle_timeout_secs)
            }
            ControlFrame::Error {
                code,
                scope,
                related_id,
                detail,
                ..
            } => Err(ProtocolRejection {
                code,
                scope,
                related_id,
                detail,
            }
            .into()),
            response => bail!("unexpected UDP association response: {response:?}"),
        }
    }

    pub async fn close_udp(&mut self, association_id: u64) -> Result<()> {
        let request_id = self.next_request_id.fetch_add(1, Ordering::Relaxed);
        let frame = ControlFrame::CloseUdp {
            request_id,
            association_id,
            code: link_wire::ProtocolErrorCode::NormalClosure,
        };
        write_control_frame(&mut self.control_send, &frame, &self.limits).await
    }

    pub fn send_udp(&self, datagram: UdpDatagram) -> Result<()> {
        let encoded = datagram
            .encode(&self.limits)
            .context("encode UDP datagram")?;
        if self
            .connection
            .max_datagram_size()
            .is_some_and(|maximum| encoded.len() > maximum)
        {
            bail!("encoded UDP datagram exceeds current QUIC path limit");
        }
        self.connection
            .send_datagram(Bytes::from(encoded))
            .context("send QUIC datagram")
    }

    pub async fn recv_udp(&self) -> Result<UdpDatagram> {
        let bytes = self
            .connection
            .read_datagram()
            .await
            .context("receive QUIC datagram")?;
        UdpDatagram::decode(&bytes, &self.limits).context("decode UDP datagram")
    }

    pub async fn ping(&mut self, nonce: u64) -> Result<()> {
        let request_id = self.next_request_id.fetch_add(1, Ordering::Relaxed);
        write_control_frame(
            &mut self.control_send,
            &ControlFrame::Ping { request_id, nonce },
            &self.limits,
        )
        .await?;
        match read_control_frame(&mut self.control_recv, &self.limits).await? {
            ControlFrame::Pong {
                request_id: response_id,
                nonce: response_nonce,
            } if response_id == request_id && response_nonce == nonce => Ok(()),
            response => bail!("unexpected PONG response: {response:?}"),
        }
    }

    pub fn close(&self) {
        self.connection
            .close(VarInt::from_u32(0), b"baseline client close");
    }

    pub async fn wait_idle(&self) {
        self.endpoint.wait_idle().await;
    }
}
