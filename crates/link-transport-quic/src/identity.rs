use anyhow::{Context, Result, bail};
use quinn::Connection;
use rustls::pki_types::CertificateDer;
use sha2::{Digest, Sha256};

pub fn device_id_from_certificate(certificate: &CertificateDer<'_>) -> [u8; 16] {
    let digest = Sha256::digest(certificate.as_ref());
    let mut id = [0u8; 16];
    id.copy_from_slice(&digest[..16]);
    id
}

pub(crate) fn peer_device_id(connection: &Connection) -> Result<[u8; 16]> {
    let identity = connection
        .peer_identity()
        .context("authenticated peer identity is unavailable")?;
    let certificates = identity
        .downcast::<Vec<CertificateDer<'static>>>()
        .map_err(|_| anyhow::anyhow!("unexpected QUIC peer identity type"))?;
    let leaf = certificates
        .first()
        .context("authenticated peer certificate chain is empty")?;
    if leaf.is_empty() {
        bail!("authenticated peer leaf certificate is empty");
    }
    Ok(device_id_from_certificate(leaf))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn certificate_identity_is_deterministic_and_certificate_specific() {
        let first = CertificateDer::from(vec![1, 2, 3]);
        let second = CertificateDer::from(vec![1, 2, 4]);
        assert_eq!(
            device_id_from_certificate(&first),
            device_id_from_certificate(&first)
        );
        assert_ne!(
            device_id_from_certificate(&first),
            device_id_from_certificate(&second)
        );
    }
}
