use std::net::{Ipv4Addr, SocketAddr};
use std::sync::Arc;
use std::time::Duration;

use edge_transport_quic::{
    BaselineClient, BaselineServer, ProtocolRejection, ServerOptions, build_client_config,
    build_server_config, device_id_from_certificate,
};
use edge_wire::{Address, ProtocolErrorCode, ProtocolLimits, UdpDatagram};
use rcgen::{
    BasicConstraints, Certificate, CertificateParams, DnType, ExtendedKeyUsagePurpose, IsCa,
    Issuer, KeyPair, KeyUsagePurpose,
};
use rustls::RootCertStore;
use rustls::pki_types::{CertificateDer, PrivateKeyDer, PrivatePkcs8KeyDer};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, UdpSocket};
use tokio::time::timeout;

struct Identity {
    certificate_chain: Vec<CertificateDer<'static>>,
    private_key: PrivateKeyDer<'static>,
}

struct TestPki {
    ca_certificate: CertificateDer<'static>,
    server: Identity,
    client: Identity,
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn localhost_mtls_tcp_and_udp_relay_complete() {
    let pki = test_pki("localhost");
    let limits = ProtocolLimits::default();
    let server_config = build_server_config(
        pki.server.certificate_chain,
        pki.server.private_key,
        root_store(pki.ca_certificate.clone()),
        limits,
    )
    .expect("server config");
    let device_id = device_id_from_certificate(&pki.client.certificate_chain[0]);
    let client_config = build_client_config(
        pki.client.certificate_chain,
        pki.client.private_key,
        root_store(pki.ca_certificate),
        limits,
    )
    .expect("client config");

    let tcp_listener = TcpListener::bind((Ipv4Addr::LOCALHOST, 0))
        .await
        .expect("bind TCP echo");
    let tcp_address = tcp_listener.local_addr().expect("TCP echo address");
    let tcp_echo = tokio::spawn(async move {
        let (mut stream, _) = tcp_listener.accept().await.expect("accept TCP echo");
        let mut bytes = Vec::new();
        stream.read_to_end(&mut bytes).await.expect("read TCP echo");
        stream.write_all(&bytes).await.expect("write TCP echo");
        stream.shutdown().await.expect("close TCP echo");
    });

    let udp_socket = UdpSocket::bind((Ipv4Addr::LOCALHOST, 0))
        .await
        .expect("bind UDP echo");
    let udp_address = udp_socket.local_addr().expect("UDP echo address");
    let udp_echo = tokio::spawn(async move {
        let mut buffer = [0u8; 2048];
        let (length, peer) = udp_socket
            .recv_from(&mut buffer)
            .await
            .expect("receive UDP echo");
        udp_socket
            .send_to(&buffer[..length], peer)
            .await
            .expect("send UDP echo");
    });

    let server = Arc::new(
        BaselineServer::bind(
            SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
            server_config,
            ServerOptions {
                session_id: [9; 16],
                ..ServerOptions::default()
            },
        )
        .expect("bind Baseline server"),
    );
    let server_address = server.local_addr().expect("Baseline server address");
    let serving = {
        let server = server.clone();
        tokio::spawn(async move { server.accept_once().await })
    };

    let mut client = BaselineClient::connect(
        SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
        client_config,
        server_address,
        "localhost",
        device_id,
        "edge-client/test",
    )
    .await
    .expect("connect Baseline client");

    client.ping(0xfeed_beef).await.expect("PING/PONG");

    let denied = client
        .open_tcp(Address::Ipv4 {
            address: Ipv4Addr::new(192, 0, 2, 1),
            port: 443,
        })
        .await
        .expect_err("default policy must deny non-loopback targets");
    assert_eq!(
        denied
            .downcast_ref::<ProtocolRejection>()
            .expect("typed target rejection")
            .code,
        ProtocolErrorCode::TargetDenied
    );

    let (mut tcp_send, mut tcp_recv) = client
        .open_tcp(Address::Ipv4 {
            address: Ipv4Addr::LOCALHOST,
            port: tcp_address.port(),
        })
        .await
        .expect("open TCP relay");
    tcp_send
        .write_all(b"baseline tcp")
        .await
        .expect("write TCP relay");
    tcp_send.finish().expect("half-close TCP relay");
    let tcp_response = timeout(Duration::from_secs(5), tcp_recv.read_to_end(1024))
        .await
        .expect("TCP relay deadline")
        .expect("read TCP relay");
    assert_eq!(tcp_response, b"baseline tcp");

    assert_eq!(client.open_udp(41).await.expect("open UDP association"), 60);
    client
        .send_udp(UdpDatagram {
            association_id: 41,
            address: Address::Ipv4 {
                address: Ipv4Addr::LOCALHOST,
                port: udp_address.port(),
            },
            payload: b"baseline udp".to_vec(),
        })
        .expect("send UDP relay");
    let udp_response = timeout(Duration::from_secs(5), client.recv_udp())
        .await
        .expect("UDP relay deadline")
        .expect("read UDP relay");
    assert_eq!(udp_response.association_id, 41);
    assert_eq!(udp_response.payload, b"baseline udp");
    client.close_udp(41).await.expect("close UDP association");

    client.close();
    timeout(Duration::from_secs(5), client.wait_idle())
        .await
        .expect("client close deadline");
    timeout(Duration::from_secs(5), serving)
        .await
        .expect("server close deadline")
        .expect("server task")
        .expect("serve connection");
    server.close();

    timeout(Duration::from_secs(5), tcp_echo)
        .await
        .expect("TCP echo deadline")
        .expect("TCP echo task");
    timeout(Duration::from_secs(5), udp_echo)
        .await
        .expect("UDP echo deadline")
        .expect("UDP echo task");
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn hello_device_id_must_match_authenticated_certificate() {
    let pki = test_pki("localhost");
    let limits = ProtocolLimits::default();
    let server_config = build_server_config(
        pki.server.certificate_chain,
        pki.server.private_key,
        root_store(pki.ca_certificate.clone()),
        limits,
    )
    .expect("server config");
    let actual_device_id = device_id_from_certificate(&pki.client.certificate_chain[0]);
    let mut mismatched_device_id = actual_device_id;
    mismatched_device_id[0] ^= 0xff;
    let client_config = build_client_config(
        pki.client.certificate_chain,
        pki.client.private_key,
        root_store(pki.ca_certificate),
        limits,
    )
    .expect("client config");

    let server = Arc::new(
        BaselineServer::bind(
            SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
            server_config,
            ServerOptions::default(),
        )
        .expect("bind Baseline server"),
    );
    let server_address = server.local_addr().expect("Baseline server address");
    let serving = {
        let server = server.clone();
        tokio::spawn(async move { server.accept_once().await })
    };

    let error = match BaselineClient::connect(
        SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
        client_config,
        server_address,
        "localhost",
        mismatched_device_id,
        "edge-client/mismatched-device",
    )
    .await
    {
        Ok(client) => {
            client.close();
            panic!("mismatched HELLO device identifier was accepted");
        }
        Err(error) => error,
    };
    assert_eq!(
        error
            .downcast_ref::<ProtocolRejection>()
            .expect("typed identity rejection")
            .code,
        ProtocolErrorCode::AuthenticationFailed
    );

    timeout(Duration::from_secs(5), serving)
        .await
        .expect("server identity-rejection deadline")
        .expect("server task")
        .expect("serve rejected connection");
    server.close();
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn untrusted_client_certificate_is_rejected() {
    let server_pki = test_pki("localhost");
    let untrusted_pki = test_pki("localhost");
    let limits = ProtocolLimits::default();
    let server_config = build_server_config(
        server_pki.server.certificate_chain,
        server_pki.server.private_key,
        root_store(server_pki.ca_certificate.clone()),
        limits,
    )
    .expect("server config");
    let client_config = build_client_config(
        untrusted_pki.client.certificate_chain,
        untrusted_pki.client.private_key,
        root_store(server_pki.ca_certificate),
        limits,
    )
    .expect("client config");

    let server = Arc::new(
        BaselineServer::bind(
            SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
            server_config,
            ServerOptions::default(),
        )
        .expect("bind Baseline server"),
    );
    let server_address = server.local_addr().expect("Baseline server address");
    let serving = {
        let server = server.clone();
        tokio::spawn(async move { server.accept_once().await })
    };

    let result = BaselineClient::connect(
        SocketAddr::from((Ipv4Addr::LOCALHOST, 0)),
        client_config,
        server_address,
        "localhost",
        [8; 16],
        "edge-client/untrusted",
    )
    .await;
    assert!(result.is_err());

    let server_result = timeout(Duration::from_secs(5), serving)
        .await
        .expect("server rejection deadline")
        .expect("server task");
    assert!(server_result.is_err());
    server.close();
}

fn root_store(certificate: CertificateDer<'static>) -> RootCertStore {
    let mut roots = RootCertStore::empty();
    roots.add(certificate).expect("add CA root");
    roots
}

fn test_pki(server_name: &str) -> TestPki {
    let (ca_certificate, issuer) = certificate_authority();
    let server = leaf_identity(server_name, ExtendedKeyUsagePurpose::ServerAuth, &issuer);
    let client = leaf_identity(
        "ordivon-test-device",
        ExtendedKeyUsagePurpose::ClientAuth,
        &issuer,
    );
    TestPki {
        ca_certificate: CertificateDer::from(ca_certificate.der().to_vec()),
        server,
        client,
    }
}

fn certificate_authority() -> (Certificate, Issuer<'static, KeyPair>) {
    let mut params = CertificateParams::new(Vec::<String>::new()).expect("CA parameters");
    params.is_ca = IsCa::Ca(BasicConstraints::Unconstrained);
    params
        .distinguished_name
        .push(DnType::CommonName, "Ordivon Baseline Test CA");
    params.key_usages.push(KeyUsagePurpose::DigitalSignature);
    params.key_usages.push(KeyUsagePurpose::KeyCertSign);
    params.key_usages.push(KeyUsagePurpose::CrlSign);
    let key = KeyPair::generate().expect("CA key");
    let certificate = params.self_signed(&key).expect("CA certificate");
    (certificate, Issuer::new(params, key))
}

fn leaf_identity(
    name: &str,
    purpose: ExtendedKeyUsagePurpose,
    issuer: &Issuer<'static, KeyPair>,
) -> Identity {
    let mut params = CertificateParams::new(vec![name.to_owned()]).expect("leaf parameters");
    params.distinguished_name.push(DnType::CommonName, name);
    params.key_usages.push(KeyUsagePurpose::DigitalSignature);
    params.extended_key_usages.push(purpose);
    params.use_authority_key_identifier_extension = true;
    let key = KeyPair::generate().expect("leaf key");
    let certificate = params
        .signed_by(&key, issuer)
        .expect("signed leaf certificate");
    Identity {
        certificate_chain: vec![CertificateDer::from(certificate.der().to_vec())],
        private_key: PrivatePkcs8KeyDer::from(key.serialize_der()).into(),
    }
}
