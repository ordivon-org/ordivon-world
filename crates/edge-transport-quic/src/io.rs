use anyhow::{Context, Result, bail};
use edge_wire::{ControlFrame, ProtocolLimits, TcpOpen, TcpOpenResponse, WireError, decode_varint};
use quinn::{RecvStream, SendStream};
use tokio::io::AsyncWriteExt;

pub(crate) async fn write_control_frame(
    send: &mut SendStream,
    frame: &ControlFrame,
    limits: &ProtocolLimits,
) -> Result<()> {
    let encoded = frame.encode(limits).context("encode control frame")?;
    send.write_all(&encoded)
        .await
        .context("write control frame")?;
    send.flush().await.context("flush control frame")?;
    Ok(())
}

pub(crate) async fn read_control_frame(
    recv: &mut RecvStream,
    limits: &ProtocolLimits,
) -> Result<ControlFrame> {
    let (body_len, prefix) = read_varint_with_bytes(recv).await?;
    if body_len > u64::from(limits.max_control_frame_len) {
        bail!("control frame exceeds negotiated limit");
    }
    let body_len = usize::try_from(body_len).context("control frame length does not fit usize")?;
    let mut body = vec![0u8; body_len];
    recv.read_exact(&mut body)
        .await
        .context("read control frame body")?;
    let mut encoded = prefix;
    encoded.extend_from_slice(&body);
    ControlFrame::decode(&encoded, limits).context("decode control frame")
}

pub(crate) async fn read_tcp_open(
    recv: &mut RecvStream,
    limits: &ProtocolLimits,
) -> Result<TcpOpen> {
    read_incremental(recv, usize::from(limits.max_domain_len) + 32, |bytes| {
        TcpOpen::decode(bytes, limits)
    })
    .await
    .context("read TCP open preface")
}

pub(crate) async fn write_tcp_response(
    send: &mut SendStream,
    response: &TcpOpenResponse,
) -> Result<()> {
    let encoded = response.encode().context("encode TCP open response")?;
    send.write_all(&encoded)
        .await
        .context("write TCP open response")?;
    send.flush().await.context("flush TCP open response")?;
    Ok(())
}

pub(crate) async fn read_tcp_response(recv: &mut RecvStream) -> Result<TcpOpenResponse> {
    read_incremental(recv, 16, TcpOpenResponse::decode)
        .await
        .context("read TCP open response")
}

async fn read_incremental<T>(
    recv: &mut RecvStream,
    maximum: usize,
    decode: impl Fn(&[u8]) -> Result<T, WireError>,
) -> Result<T> {
    let mut bytes = Vec::new();
    loop {
        if bytes.len() >= maximum {
            bail!("wire value exceeds bounded preface size");
        }
        let mut byte = [0u8; 1];
        recv.read_exact(&mut byte)
            .await
            .context("read wire value")?;
        bytes.push(byte[0]);
        match decode(&bytes) {
            Ok(value) => return Ok(value),
            Err(WireError::UnexpectedEof) => continue,
            Err(error) => return Err(error.into()),
        }
    }
}

async fn read_varint_with_bytes(recv: &mut RecvStream) -> Result<(u64, Vec<u8>)> {
    let mut first = [0u8; 1];
    recv.read_exact(&mut first)
        .await
        .context("read QUIC varint prefix")?;
    let length = 1usize << usize::from(first[0] >> 6);
    let mut bytes = vec![0u8; length];
    bytes[0] = first[0];
    if length > 1 {
        recv.read_exact(&mut bytes[1..])
            .await
            .context("read QUIC varint remainder")?;
    }
    let (value, consumed) = decode_varint(&bytes).context("decode QUIC varint")?;
    if consumed != bytes.len() {
        bail!("invalid QUIC varint length");
    }
    Ok((value, bytes))
}
