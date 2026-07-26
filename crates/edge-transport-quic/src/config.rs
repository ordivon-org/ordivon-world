use std::sync::Arc;

use anyhow::{Context, Result};
use edge_wire::{ALPN_V0, ProtocolLimits};
use quinn::crypto::rustls::{QuicClientConfig, QuicServerConfig};
use quinn::{ClientConfig, ServerConfig, TransportConfig, VarInt};
use rustls::pki_types::{CertificateDer, PrivateKeyDer};
use rustls::server::WebPkiClientVerifier;
use rustls::{RootCertStore, version};

pub fn build_server_config(
    certificate_chain: Vec<CertificateDer<'static>>,
    private_key: PrivateKeyDer<'static>,
    client_roots: RootCertStore,
    limits: ProtocolLimits,
) -> Result<ServerConfig> {
    let provider = Arc::new(rustls::crypto::ring::default_provider());
    let verifier =
        WebPkiClientVerifier::builder_with_provider(Arc::new(client_roots), provider.clone())
            .build()
            .context("build mandatory client certificate verifier")?;
    let mut crypto = rustls::ServerConfig::builder_with_provider(provider)
        .with_protocol_versions(&[&version::TLS13])
        .context("enable TLS 1.3")?
        .with_client_cert_verifier(verifier)
        .with_single_cert(certificate_chain, private_key)
        .context("configure Edge certificate")?;
    crypto.alpn_protocols = vec![ALPN_V0.to_vec()];
    crypto.max_early_data_size = 0;

    let mut transport = TransportConfig::default();
    transport
        .max_concurrent_bidi_streams(VarInt::from_u32(limits.max_tcp_streams.saturating_add(1)))
        .max_concurrent_uni_streams(VarInt::from_u32(0))
        .datagram_receive_buffer_size(Some(1024 * 1024))
        .datagram_send_buffer_size(1024 * 1024);

    let mut config = ServerConfig::with_crypto(Arc::new(
        QuicServerConfig::try_from(crypto).context("create QUIC server crypto")?,
    ));
    config.transport_config(Arc::new(transport));
    config.migration(false);
    Ok(config)
}

pub fn build_client_config(
    certificate_chain: Vec<CertificateDer<'static>>,
    private_key: PrivateKeyDer<'static>,
    server_roots: RootCertStore,
    limits: ProtocolLimits,
) -> Result<ClientConfig> {
    let provider = Arc::new(rustls::crypto::ring::default_provider());
    let mut crypto = rustls::ClientConfig::builder_with_provider(provider)
        .with_protocol_versions(&[&version::TLS13])
        .context("enable TLS 1.3")?
        .with_root_certificates(server_roots)
        .with_client_auth_cert(certificate_chain, private_key)
        .context("configure device certificate")?;
    crypto.alpn_protocols = vec![ALPN_V0.to_vec()];
    crypto.enable_early_data = false;

    let mut transport = TransportConfig::default();
    transport
        .max_concurrent_bidi_streams(VarInt::from_u32(limits.max_tcp_streams.saturating_add(1)))
        .max_concurrent_uni_streams(VarInt::from_u32(0))
        .datagram_receive_buffer_size(Some(1024 * 1024))
        .datagram_send_buffer_size(1024 * 1024);

    let mut config = ClientConfig::new(Arc::new(
        QuicClientConfig::try_from(crypto).context("create QUIC client crypto")?,
    ));
    config.transport_config(Arc::new(transport));
    Ok(config)
}
