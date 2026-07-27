use std::collections::HashMap;
use std::io;
use std::net::{IpAddr, Ipv4Addr, Ipv6Addr, SocketAddr};
use std::sync::Arc;
use std::time::Duration;

use anyhow::{Context, Result, anyhow, bail};
use bytes::Bytes;
use link_wire::{
    Address, Capabilities, ControlFrame, ErrorScope, PROTOCOL_MINOR, ProtocolErrorCode,
    ProtocolLimits, TcpOpenResponse, UdpDatagram,
};
use quinn::{Connection, Endpoint, RecvStream, SendStream, ServerConfig, VarInt};
use tokio::io::{AsyncWriteExt, copy};
use tokio::net::{TcpStream, UdpSocket};
use tokio::sync::{Mutex, OwnedSemaphorePermit, Semaphore};
use tokio::task::JoinHandle;
use tokio::time::{Instant, interval, timeout};

use crate::identity::peer_device_id;
use crate::io::{read_control_frame, read_tcp_open, write_control_frame, write_tcp_response};
use crate::{LoopbackOnlyPolicy, TargetPolicy};

#[derive(Clone)]
pub struct ServerOptions {
    pub build: String,
    pub session_id: [u8; 16],
    pub limits: ProtocolLimits,
    pub connect_timeout: Duration,
    pub target_policy: Arc<dyn TargetPolicy>,
}

impl Default for ServerOptions {
    fn default() -> Self {
        Self {
            build: "link-console/0.1".into(),
            session_id: [0; 16],
            limits: ProtocolLimits::default(),
            connect_timeout: Duration::from_secs(10),
            target_policy: Arc::new(LoopbackOnlyPolicy),
        }
    }
}

pub struct BaselineServer {
    endpoint: Endpoint,
    options: ServerOptions,
}

impl BaselineServer {
    pub fn bind(address: SocketAddr, config: ServerConfig, options: ServerOptions) -> Result<Self> {
        let endpoint = Endpoint::server(config, address).context("bind QUIC server endpoint")?;
        Ok(Self { endpoint, options })
    }

    pub fn local_addr(&self) -> Result<SocketAddr> {
        self.endpoint.local_addr().context("read server address")
    }

    pub async fn accept_once(&self) -> Result<()> {
        let incoming = self
            .endpoint
            .accept()
            .await
            .ok_or_else(|| anyhow!("server endpoint closed"))?;
        let connection = incoming.await.context("accept QUIC and mTLS connection")?;
        serve_connection(connection, self.options.clone()).await
    }

    pub fn close(&self) {
        self.endpoint
            .close(VarInt::from_u32(0), b"baseline server close");
    }
}

type SharedControlSend = Arc<Mutex<SendStream>>;
type Associations = Arc<Mutex<HashMap<u64, Association>>>;

struct Association {
    idle_timeout: Duration,
    last_activity: Arc<Mutex<Instant>>,
    ipv4: Option<SocketHandle>,
    ipv6: Option<SocketHandle>,
}

struct SocketHandle {
    socket: Arc<UdpSocket>,
    receiver: JoinHandle<()>,
}

impl Association {
    fn abort(self) {
        if let Some(handle) = self.ipv4 {
            handle.receiver.abort();
        }
        if let Some(handle) = self.ipv6 {
            handle.receiver.abort();
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum SocketFamily {
    Ipv4,
    Ipv6,
}

async fn serve_connection(connection: Connection, options: ServerOptions) -> Result<()> {
    let authenticated_device_id = peer_device_id(&connection)?;
    let (mut control_send, mut control_recv) = connection
        .accept_bi()
        .await
        .context("accept control stream")?;
    let hello = read_control_frame(&mut control_recv, &options.limits).await?;
    match hello {
        ControlFrame::Hello {
            request_id,
            minor_version,
            capabilities,
            device_id,
            ..
        } if device_id == authenticated_device_id
            && minor_version == PROTOCOL_MINOR
            && capabilities.contains(Capabilities::TCP_RELAY)
            && capabilities.contains(Capabilities::UDP_RELAY) =>
        {
            write_control_frame(
                &mut control_send,
                &ControlFrame::HelloOk {
                    request_id,
                    minor_version: PROTOCOL_MINOR,
                    capabilities: Capabilities::TCP_RELAY.union(Capabilities::UDP_RELAY),
                    session_id: options.session_id,
                    server_build: options.build.clone(),
                    limits: options.limits,
                },
                &options.limits,
            )
            .await?;
        }
        ControlFrame::Hello {
            request_id,
            device_id,
            ..
        } if device_id != authenticated_device_id => {
            write_control_frame(
                &mut control_send,
                &ControlFrame::Error {
                    request_id,
                    code: ProtocolErrorCode::AuthenticationFailed,
                    scope: ErrorScope::Connection,
                    related_id: request_id,
                    detail: "HELLO device identifier does not match the authenticated certificate"
                        .into(),
                },
                &options.limits,
            )
            .await?;
            control_send
                .finish()
                .context("finish rejected HELLO response")?;
            let _ = timeout(Duration::from_secs(1), control_send.stopped()).await;
            connection.close(VarInt::from_u32(2), b"device identity mismatch");
            return Ok(());
        }
        ControlFrame::Hello { request_id, .. } => {
            write_control_frame(
                &mut control_send,
                &ControlFrame::Error {
                    request_id,
                    code: ProtocolErrorCode::CapabilityMismatch,
                    scope: ErrorScope::Connection,
                    related_id: request_id,
                    detail: "unsupported Baseline capabilities or minor version".into(),
                },
                &options.limits,
            )
            .await?;
            control_send
                .finish()
                .context("finish rejected HELLO response")?;
            let _ = timeout(Duration::from_secs(1), control_send.stopped()).await;
            connection.close(VarInt::from_u32(1), b"HELLO rejected");
            return Ok(());
        }
        _ => bail!("first control frame was not HELLO"),
    }

    let control_send = Arc::new(Mutex::new(control_send));
    let associations: Associations = Arc::new(Mutex::new(HashMap::new()));
    let pending = Arc::new(Semaphore::new(options.limits.max_pending_tcp as usize));

    let control = control_loop(
        connection.clone(),
        control_send.clone(),
        control_recv,
        associations.clone(),
        options.clone(),
    );
    let tcp = tcp_accept_loop(connection.clone(), pending, options.clone());
    let udp = udp_datagram_loop(
        connection.clone(),
        control_send.clone(),
        associations.clone(),
        options.clone(),
    );
    let expiry = udp_expiry_loop(
        connection.clone(),
        control_send,
        associations.clone(),
        options.limits,
    );

    let result = tokio::select! {
        result = control => result,
        result = tcp => result,
        result = udp => result,
        result = expiry => result,
    };
    connection.close(VarInt::from_u32(0), b"baseline session ended");
    cleanup_associations(&associations).await;
    result
}

async fn control_loop(
    connection: Connection,
    control_send: SharedControlSend,
    mut control_recv: RecvStream,
    associations: Associations,
    options: ServerOptions,
) -> Result<()> {
    loop {
        let frame = match read_control_frame(&mut control_recv, &options.limits).await {
            Ok(frame) => frame,
            Err(_error) if connection.close_reason().is_some() => return Ok(()),
            Err(error) => return Err(error),
        };
        match frame {
            ControlFrame::OpenUdp {
                request_id,
                association_id,
                idle_timeout_secs,
            } => {
                let accepted_timeout = idle_timeout_secs
                    .max(1)
                    .min(options.limits.udp_idle_timeout_secs);
                let mut map = associations.lock().await;
                if !map.contains_key(&association_id)
                    && map.len() >= options.limits.max_udp_associations as usize
                {
                    drop(map);
                    send_error(
                        &control_send,
                        &options.limits,
                        request_id,
                        ProtocolErrorCode::ResourceLimit,
                        ErrorScope::Association,
                        association_id,
                        "UDP association limit reached",
                    )
                    .await?;
                    continue;
                }
                map.entry(association_id).or_insert_with(|| Association {
                    idle_timeout: Duration::from_secs(u64::from(accepted_timeout)),
                    last_activity: Arc::new(Mutex::new(Instant::now())),
                    ipv4: None,
                    ipv6: None,
                });
                drop(map);
                send_control(
                    &control_send,
                    &ControlFrame::OpenUdpOk {
                        request_id,
                        association_id,
                        idle_timeout_secs: accepted_timeout,
                    },
                    &options.limits,
                )
                .await?;
            }
            ControlFrame::CloseUdp { association_id, .. } => {
                if let Some(association) = associations.lock().await.remove(&association_id) {
                    association.abort();
                }
            }
            ControlFrame::Ping { request_id, nonce } => {
                send_control(
                    &control_send,
                    &ControlFrame::Pong { request_id, nonce },
                    &options.limits,
                )
                .await?;
            }
            ControlFrame::GoAway { .. } => return Ok(()),
            ControlFrame::Unknown { .. } => {}
            ControlFrame::Hello { request_id, .. }
            | ControlFrame::HelloOk { request_id, .. }
            | ControlFrame::OpenUdpOk { request_id, .. }
            | ControlFrame::Pong { request_id, .. }
            | ControlFrame::Drain { request_id, .. }
            | ControlFrame::Error { request_id, .. } => {
                send_error(
                    &control_send,
                    &options.limits,
                    request_id,
                    ProtocolErrorCode::InvalidFrame,
                    ErrorScope::Connection,
                    request_id,
                    "unexpected client control frame",
                )
                .await?;
                return Ok(());
            }
        }
    }
}

async fn tcp_accept_loop(
    connection: Connection,
    pending: Arc<Semaphore>,
    options: ServerOptions,
) -> Result<()> {
    loop {
        let (send, recv) = match connection.accept_bi().await {
            Ok(streams) => streams,
            Err(_) if connection.close_reason().is_some() => return Ok(()),
            Err(error) => return Err(error).context("accept TCP relay stream"),
        };
        let permit = pending
            .clone()
            .acquire_owned()
            .await
            .context("pending TCP semaphore closed")?;
        let options = options.clone();
        tokio::spawn(async move {
            let _ = handle_tcp_stream(send, recv, options, permit).await;
        });
    }
}

async fn handle_tcp_stream(
    mut send: SendStream,
    mut recv: RecvStream,
    options: ServerOptions,
    pending_permit: OwnedSemaphorePermit,
) -> Result<()> {
    let open = read_tcp_open(&mut recv, &options.limits).await?;
    if !options.target_policy.allows(&open.target) {
        write_tcp_response(
            &mut send,
            &TcpOpenResponse::Error {
                request_id: open.request_id,
                code: ProtocolErrorCode::TargetDenied,
            },
        )
        .await?;
        let _ = send.finish();
        return Ok(());
    }

    let target = match timeout(options.connect_timeout, resolve_address(&open.target)).await {
        Ok(Ok(target)) => target,
        Ok(Err(code)) => {
            write_tcp_error(&mut send, open.request_id, code).await?;
            return Ok(());
        }
        Err(_) => {
            write_tcp_error(&mut send, open.request_id, ProtocolErrorCode::TargetTimeout).await?;
            return Ok(());
        }
    };
    let stream = match timeout(options.connect_timeout, TcpStream::connect(target)).await {
        Ok(Ok(stream)) => stream,
        Ok(Err(error)) => {
            write_tcp_error(&mut send, open.request_id, map_connect_error(&error)).await?;
            return Ok(());
        }
        Err(_) => {
            write_tcp_error(&mut send, open.request_id, ProtocolErrorCode::TargetTimeout).await?;
            return Ok(());
        }
    };
    drop(pending_permit);

    write_tcp_response(
        &mut send,
        &TcpOpenResponse::Ok {
            request_id: open.request_id,
        },
    )
    .await?;

    let (mut target_read, mut target_write) = stream.into_split();
    let client_to_target = async {
        copy(&mut recv, &mut target_write)
            .await
            .context("relay client bytes to target")?;
        target_write
            .shutdown()
            .await
            .context("half-close target write")?;
        Ok::<(), anyhow::Error>(())
    };
    let target_to_client = async {
        copy(&mut target_read, &mut send)
            .await
            .context("relay target bytes to client")?;
        send.finish().context("finish QUIC relay stream")?;
        Ok::<(), anyhow::Error>(())
    };
    tokio::try_join!(client_to_target, target_to_client)?;
    Ok(())
}

async fn udp_datagram_loop(
    connection: Connection,
    control_send: SharedControlSend,
    associations: Associations,
    options: ServerOptions,
) -> Result<()> {
    loop {
        let bytes = match connection.read_datagram().await {
            Ok(bytes) => bytes,
            Err(_) if connection.close_reason().is_some() => return Ok(()),
            Err(error) => return Err(error).context("read QUIC datagram"),
        };
        let datagram = match UdpDatagram::decode(&bytes, &options.limits) {
            Ok(datagram) => datagram,
            Err(error) => {
                send_error(
                    &control_send,
                    &options.limits,
                    0,
                    ProtocolErrorCode::InvalidFrame,
                    ErrorScope::Association,
                    0,
                    &format!("invalid UDP datagram: {error}"),
                )
                .await?;
                continue;
            }
        };
        if !options.target_policy.allows(&datagram.address) {
            send_error(
                &control_send,
                &options.limits,
                0,
                ProtocolErrorCode::TargetDenied,
                ErrorScope::Association,
                datagram.association_id,
                "UDP target denied by server policy",
            )
            .await?;
            continue;
        }
        let target = match resolve_address(&datagram.address).await {
            Ok(target) => target,
            Err(code) => {
                send_error(
                    &control_send,
                    &options.limits,
                    0,
                    code,
                    ErrorScope::Association,
                    datagram.association_id,
                    "UDP target resolution failed",
                )
                .await?;
                continue;
            }
        };
        let socket = match association_socket(
            datagram.association_id,
            target,
            &connection,
            &associations,
            options.limits,
        )
        .await
        {
            Ok(socket) => socket,
            Err(code) => {
                send_error(
                    &control_send,
                    &options.limits,
                    0,
                    code,
                    ErrorScope::Association,
                    datagram.association_id,
                    "UDP association unavailable",
                )
                .await?;
                continue;
            }
        };
        socket
            .send_to(&datagram.payload, target)
            .await
            .context("send UDP payload to target")?;
    }
}

async fn association_socket(
    association_id: u64,
    target: SocketAddr,
    connection: &Connection,
    associations: &Associations,
    limits: ProtocolLimits,
) -> Result<Arc<UdpSocket>, ProtocolErrorCode> {
    let family = if target.is_ipv4() {
        SocketFamily::Ipv4
    } else {
        SocketFamily::Ipv6
    };
    {
        let map = associations.lock().await;
        let association = map
            .get(&association_id)
            .ok_or(ProtocolErrorCode::UdpAssociationUnknown)?;
        *association.last_activity.lock().await = Instant::now();
        let existing = match family {
            SocketFamily::Ipv4 => association.ipv4.as_ref(),
            SocketFamily::Ipv6 => association.ipv6.as_ref(),
        };
        if let Some(existing) = existing {
            return Ok(existing.socket.clone());
        }
    }

    let bind_address = match family {
        SocketFamily::Ipv4 => SocketAddr::new(IpAddr::V4(Ipv4Addr::UNSPECIFIED), 0),
        SocketFamily::Ipv6 => SocketAddr::new(IpAddr::V6(Ipv6Addr::UNSPECIFIED), 0),
    };
    let socket = Arc::new(
        UdpSocket::bind(bind_address)
            .await
            .map_err(|_| ProtocolErrorCode::InternalError)?,
    );
    let activity = {
        let map = associations.lock().await;
        map.get(&association_id)
            .ok_or(ProtocolErrorCode::UdpAssociationUnknown)?
            .last_activity
            .clone()
    };
    let receiver = spawn_udp_receiver(
        socket.clone(),
        association_id,
        connection.clone(),
        activity,
        limits,
    );
    let mut map = associations.lock().await;
    let Some(association) = map.get_mut(&association_id) else {
        receiver.abort();
        return Err(ProtocolErrorCode::UdpAssociationUnknown);
    };
    let slot = match family {
        SocketFamily::Ipv4 => &mut association.ipv4,
        SocketFamily::Ipv6 => &mut association.ipv6,
    };
    if let Some(existing) = slot {
        receiver.abort();
        return Ok(existing.socket.clone());
    }
    *slot = Some(SocketHandle {
        socket: socket.clone(),
        receiver,
    });
    Ok(socket)
}

fn spawn_udp_receiver(
    socket: Arc<UdpSocket>,
    association_id: u64,
    connection: Connection,
    activity: Arc<Mutex<Instant>>,
    limits: ProtocolLimits,
) -> JoinHandle<()> {
    tokio::spawn(async move {
        let mut buffer = vec![0u8; usize::from(limits.max_udp_payload) + 1];
        loop {
            let (length, source) = match socket.recv_from(&mut buffer).await {
                Ok(result) => result,
                Err(_) => return,
            };
            if length > usize::from(limits.max_udp_payload) {
                continue;
            }
            *activity.lock().await = Instant::now();
            let address = match source {
                SocketAddr::V4(value) => Address::Ipv4 {
                    address: *value.ip(),
                    port: value.port(),
                },
                SocketAddr::V6(value) => Address::Ipv6 {
                    address: *value.ip(),
                    port: value.port(),
                },
            };
            let datagram = UdpDatagram {
                association_id,
                address,
                payload: buffer[..length].to_vec(),
            };
            let Ok(encoded) = datagram.encode(&limits) else {
                continue;
            };
            if connection
                .max_datagram_size()
                .is_some_and(|maximum| encoded.len() > maximum)
            {
                continue;
            }
            if connection.send_datagram(Bytes::from(encoded)).is_err() {
                return;
            }
        }
    })
}

async fn udp_expiry_loop(
    connection: Connection,
    control_send: SharedControlSend,
    associations: Associations,
    limits: ProtocolLimits,
) -> Result<()> {
    let mut ticker = interval(Duration::from_secs(1));
    loop {
        ticker.tick().await;
        if connection.close_reason().is_some() {
            return Ok(());
        }
        let snapshots = {
            let map = associations.lock().await;
            map.iter()
                .map(|(id, association)| {
                    (
                        *id,
                        association.idle_timeout,
                        association.last_activity.clone(),
                    )
                })
                .collect::<Vec<_>>()
        };
        let mut expired = Vec::new();
        for (id, idle_timeout, activity) in snapshots {
            if activity.lock().await.elapsed() >= idle_timeout {
                expired.push(id);
            }
        }
        for association_id in expired {
            if let Some(association) = associations.lock().await.remove(&association_id) {
                association.abort();
                send_control(
                    &control_send,
                    &ControlFrame::CloseUdp {
                        request_id: 0,
                        association_id,
                        code: ProtocolErrorCode::UdpIdleTimeout,
                    },
                    &limits,
                )
                .await?;
            }
        }
    }
}

async fn resolve_address(address: &Address) -> Result<SocketAddr, ProtocolErrorCode> {
    match address {
        Address::Ipv4 { address, port } => Ok(SocketAddr::new(IpAddr::V4(*address), *port)),
        Address::Ipv6 { address, port } => Ok(SocketAddr::new(IpAddr::V6(*address), *port)),
        Address::Domain { host, port } => tokio::net::lookup_host((host.as_str(), *port))
            .await
            .map_err(|_| ProtocolErrorCode::DnsFailed)?
            .next()
            .ok_or(ProtocolErrorCode::DnsFailed),
    }
}

fn map_connect_error(error: &io::Error) -> ProtocolErrorCode {
    match error.kind() {
        io::ErrorKind::ConnectionRefused => ProtocolErrorCode::TargetRefused,
        io::ErrorKind::TimedOut => ProtocolErrorCode::TargetTimeout,
        io::ErrorKind::AddrNotAvailable
        | io::ErrorKind::NetworkUnreachable
        | io::ErrorKind::HostUnreachable => ProtocolErrorCode::TargetUnreachable,
        _ => ProtocolErrorCode::TargetUnreachable,
    }
}

async fn write_tcp_error(
    send: &mut SendStream,
    request_id: u64,
    code: ProtocolErrorCode,
) -> Result<()> {
    write_tcp_response(send, &TcpOpenResponse::Error { request_id, code }).await?;
    let _ = send.finish();
    Ok(())
}

async fn send_control(
    control_send: &SharedControlSend,
    frame: &ControlFrame,
    limits: &ProtocolLimits,
) -> Result<()> {
    let mut send = control_send.lock().await;
    write_control_frame(&mut send, frame, limits).await
}

async fn send_error(
    control_send: &SharedControlSend,
    limits: &ProtocolLimits,
    request_id: u64,
    code: ProtocolErrorCode,
    scope: ErrorScope,
    related_id: u64,
    detail: &str,
) -> Result<()> {
    send_control(
        control_send,
        &ControlFrame::Error {
            request_id,
            code,
            scope,
            related_id,
            detail: detail
                .chars()
                .take(usize::from(limits.max_error_detail_len))
                .collect(),
        },
        limits,
    )
    .await
}

async fn cleanup_associations(associations: &Associations) {
    let values = associations
        .lock()
        .await
        .drain()
        .map(|(_, value)| value)
        .collect::<Vec<_>>();
    for association in values {
        association.abort();
    }
}
