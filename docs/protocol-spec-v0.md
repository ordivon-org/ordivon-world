# Ordivon Baseline protocol specification v0

## Status

This document defines the first executable wire contract. The repository contains pure encoding, decoding, limits, errors, and state transitions plus a localhost reference adapter using Quinn and rustls. No public Edge, host route mutation, production credential system, or external-network claim is included.

Normative terms such as **MUST**, **MUST NOT**, **SHOULD**, and **MAY** describe intended conformance behavior.

## Transport contract

- QUIC version: QUIC v1.
- Security: TLS 1.3 as integrated by the selected QUIC implementation.
- ALPN: `ordivon-baseline/0`.
- Authentication: server certificate plus mandatory client certificate.
- 0-RTT application data: disabled.
- Default port: UDP/443.
- Connection migration: disabled by policy in v0; path change triggers explicit reconnect.
- Congestion control: maintained QUIC library default.

A server MUST reject a connection that does not negotiate the exact v0 ALPN. There is no silent downgrade to another transport or weaker authentication mode.

## Connection lifecycle

```text
DISCONNECTED
  → QUIC_HANDSHAKING
  → AUTHENTICATED
  → NEGOTIATING
  → READY
  → DRAINING
  → CLOSED

Any active state may enter FAILED on a fatal protocol or transport error.
CLOSED or FAILED may be reset to DISCONNECTED before a new connection.
```

After QUIC and TLS complete, the client opens one bidirectional control stream. The first control frame MUST be `HELLO`. The server replies with either `HELLO_OK` or a connection-scoped `ERROR` and then closes the application session.

No TCP relay stream or UDP association may become active before `HELLO_OK`.

## QUIC variable-length integers

All fields described as `varint` use the QUIC variable-length integer representation with 1, 2, 4, or 8 bytes and a maximum value of `2^62 - 1`.

## Control frame envelope

```text
+----------------+------+-------+------------+---------+
| LENGTH         | TYPE | FLAGS | REQUEST_ID | PAYLOAD |
| QUIC varint    | u8   | u8    | varint     | bytes   |
+----------------+------+-------+------------+---------+
```

`LENGTH` is the number of bytes after the length field. The default maximum is 16 KiB.

Flag bit `0x01` is `CRITICAL`. An unknown critical frame terminates protocol processing with `INVALID_FRAME`. An unknown non-critical frame may be skipped because its length is known.

## Capabilities

The v0 capability bitset defines:

| Bit | Capability |
|---:|---|
| 0 | TCP relay |
| 1 | UDP relay |

Unknown capability bits do not enable behavior unless both peers explicitly understand them.

## HELLO

Type `0x01`, critical.

```text
minor_version   u16
capabilities    u64
device_id       16 bytes
client_build    varint length + UTF-8, max 64 bytes
```

The device identifier is the first 16 bytes of SHA-256 over the authenticated client leaf certificate DER. It is not a username and contains no user-selected personal information. The server MUST derive the same value from the mTLS peer certificate and reject a mismatched `HELLO` with `AUTHENTICATION_FAILED`.

## HELLO_OK

Type `0x02`, critical.

```text
minor_version           u16
capabilities            u64
session_id              16 bytes
server_build            varint length + UTF-8, max 64 bytes
max_control_frame_len   u32
max_domain_len          u16
max_build_len           u16
max_error_detail_len    u16
max_tcp_streams         u32
max_pending_tcp         u32
max_udp_associations    u32
max_udp_payload         u16
udp_idle_timeout_secs   u16
```

The client MUST enforce the server-advertised limits even when its own local limits are higher.

## Address encoding

```text
DOMAIN:
  type 0x00
  domain_length varint
  ASCII domain bytes
  port u16 big-endian

IPV4:
  type 0x01
  4 address bytes
  port u16 big-endian

IPV6:
  type 0x02
  16 address bytes
  port u16 big-endian
```

Domain values are ASCII A-labels. Internationalized names must be converted to an ASCII form before encoding. Empty labels, labels longer than 63 bytes, leading or trailing hyphens, and total names longer than 253 bytes are invalid.

A domain target is resolved by the Edge. An IP target is connected directly without a DNS lookup.

## TCP relay streams

Each relayed TCP connection uses one independent QUIC bidirectional stream.

### Client stream preface

```text
stream_kind    u8 = 0x01
request_id     varint
flags          u8 = 0 in v0
target         Address
```

The Edge validates the request and establishes the destination TCP connection. The client MUST wait for the response before sending application bytes.

### Server response

Success:

```text
status         u8 = 0x00
request_id     varint
```

Failure:

```text
status         u8 = 0x01
request_id     varint
error_code     u16
```

After success, the remainder of the QUIC stream is the unmodified application byte stream. QUIC provides ordering, reliability, per-stream flow control, reset, and half-close semantics. The Ordivon protocol adds no second acknowledgement or retransmission layer.

### TCP relay state

```text
CREATED → OPENING → RELAYING
                    ├→ HALF_CLOSED_LOCAL
                    └→ HALF_CLOSED_REMOTE
both EOF directions → CLOSED
opening error or reset → FAILED
```

A broken QUIC connection fails all active TCP relays. v0 does not replay stream contents or attempt transparent application-session recovery.

## UDP associations

### OPEN_UDP

Type `0x10`, critical.

```text
association_id       varint
idle_timeout_secs    u16
```

The Edge allocates association state subject to resource limits. IPv4 and IPv6 sockets may be allocated lazily when the first corresponding target is used. The effective timeout is bounded by server policy.

### OPEN_UDP_OK

Type `0x12`, critical.

```text
association_id       varint
idle_timeout_secs    u16
```

The response uses the same `REQUEST_ID` as `OPEN_UDP`. The client MUST NOT send application datagrams for the association before receiving this confirmation.

### CLOSE_UDP

Type `0x11`, non-critical.

```text
association_id    varint
error_code        u16
```

Closing an already closed association is handled idempotently by the session layer.

### UDP datagram

One QUIC DATAGRAM carries one application datagram:

```text
datagram_kind      u8 = 0x01
association_id     varint
address            Address
payload            remaining bytes
```

Message boundaries are preserved. The protocol does not acknowledge or retransmit UDP application data. The default configured payload limit is 1200 bytes, but the runtime effective limit MUST also respect the QUIC library's current maximum DATAGRAM size and may therefore be lower.

The Edge may receive responses from any remote address on the association socket and returns the actual source address in the response datagram.

## Liveness and shutdown frames

| Type | Name | Payload |
|---:|---|---|
| `0x20` | PING | nonce `u64` |
| `0x21` | PONG | nonce `u64` |
| `0x30` | DRAIN | retry-after milliseconds `u32` |
| `0x31` | GO_AWAY | error code `u16` |

`DRAIN` means the Edge will not accept new relay work but existing work may continue. `GO_AWAY` ends the application session after orderly shutdown behavior defined by the session implementation.

## ERROR frame

Type `0x7f`, critical.

```text
error_code      u16
scope           u8
related_id      varint
detail_length   varint
detail           UTF-8, max 256 bytes
```

Scopes:

| Value | Scope |
|---:|---|
| 0 | connection |
| 1 | request |
| 2 | association |

Error details are diagnostic only and MUST NOT contain private keys, credentials, application payload, or sensitive internal state.

## Stable error codes

| Code | Meaning |
|---:|---|
| `0x0000` | normal closure |
| `0x0001` | unsupported version |
| `0x0002` | authentication failed |
| `0x0003` | capability mismatch |
| `0x0004` | invalid frame |
| `0x0005` | frame too large |
| `0x0006` | resource limit |
| `0x0010` | DNS failed |
| `0x0011` | target refused |
| `0x0012` | target timeout |
| `0x0013` | target unreachable |
| `0x0014` | target denied by Edge policy |
| `0x0020` | UDP association unknown |
| `0x0021` | datagram too large |
| `0x0022` | UDP association idle timeout |
| `0x0030` | Edge draining |
| `0x0031` | internal error |

Text may change between builds. Machine behavior must depend on the numeric code.

## Default limits

| Limit | Default |
|---|---:|
| control frame | 16 KiB |
| domain | 253 bytes |
| build identifier | 64 bytes |
| error detail | 256 bytes |
| active TCP streams | 128 |
| pending TCP connects | 32 |
| UDP associations | 64 |
| configured UDP payload hard cap | 1200 bytes |
| UDP association idle timeout | 60 seconds |

Implementations may enforce lower values. All declared lengths must be validated before allocation.

## Retry semantics

- Transport reconnect creates a new session identifier.
- Existing TCP relays fail and are not replayed.
- Existing UDP associations expire and are not implicitly recreated.
- The application or Ordivon policy layer decides whether a new request is safe to issue.
- Protocol code must never infer application idempotency from payload bytes.

## Versioning

The ALPN carries the incompatible major version. Minor version and capability negotiation occur in `HELLO` and `HELLO_OK`.

A future incompatible wire format uses a new ALPN. v0 never silently interprets an unsupported major version as another protocol.
