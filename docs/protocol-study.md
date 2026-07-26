# Transport protocol source study

## Purpose and boundary

This study answers four questions for Ordivon Edge / Link:

1. What problem does each transport actually solve?
2. Which parts are public specifications, which parts are open implementations, and which claims depend on one project?
3. Where does the behavior live in source code?
4. Which failure modes must the measurement harness distinguish before any route is selected?

The repository remains an observation and control project. This study does not add a public proxy service, install a transport core, change host routes, create credentials, or design new cryptography.

The machine-readable source of the comparison is [`config/transports/protocols.toml`](../config/transports/protocols.toml). It pins the exact upstream revisions inspected on 2026-07-26. Generate the expanded report with:

```bash
cargo run -p edge-probe -- catalog
```

## First-principles model

Every candidate can be decomposed into the same pipeline:

```text
Application or IP packet
        │
        ▼
Proxy or tunnel semantics
        │  destination, authentication, streams, datagrams
        ▼
Record and multiplexing layer
        │  framing, replay handling, flow control
        ▼
Security layer
        │  key exchange, peer authentication, AEAD, certificates
        ▼
Carrier
        │  TCP, UDP, QUIC, TLS, HTTP/2, HTTP/3
        ▼
Observable network path
        │  endpoint IP, port, packet sizes, timing, duration, failures
        ▼
Overseas edge
        │
        ▼
Destination service
```

No protocol removes the observable network path. It only changes which facts are visible at each boundary and which peer is trusted with the cleartext destination.

A useful route therefore needs all of the following:

```text
reachable endpoint
∧ successful handshake
∧ correct authentication
∧ adequate path quality
∧ working destination relay
∧ stable return path
∧ acceptable host integration
```

Encryption is only one term. A cryptographically secure transport can still fail because UDP is impaired, MTU discovery is wrong, the endpoint is unavailable, the protocol is classified, the process leaks DNS, or the host route is misconfigured.

## Publicness is not binary

There are several different meanings of “public”:

| Level | Meaning | Example in this study |
|---|---|---|
| Open specification | Wire format and state transitions are documented independently of code | TUIC `SPEC.md`, Hysteria `PROTOCOL.md` |
| Open implementation | Source for a working client/server is available | WireGuard-go, OpenVPN, shadowsocks-rust, Xray-core, Hysteria, sing-box, NaiveProxy |
| Native/reference implementation | The project is the primary place where a protocol feature is defined and evolved | Xray-core for current VLESS/REALITY behavior |
| Multi-implementation protocol | Independent projects implement the same family, sometimes with semantic drift | Shadowsocks, TUIC, Hysteria2 adapters |
| Open code without stable source history | Source is visible, but revision tracking has unusual behavior | NaiveProxy master is rebased during Chromium imports |

Open source provides inspectability, reproducibility, and license rights. It does not automatically prove security, indistinguishability, interoperability, or operational reliability.

## Protocol-by-protocol decomposition

### WireGuard

**Role:** clean IP-tunnel baseline.

WireGuard's main value to this study is not camouflage. It gives a small peer/key/endpoint/AllowedIPs model against which more complex systems can be compared.

```text
TUN IP packet
  → peer lookup by AllowedIPs
  → Noise-derived session keys
  → encrypted WireGuard data message
  → UDP socket
  → remote peer
```

Code navigation:

- `device/noise-protocol.go`: handshake state and key derivation;
- `device/send.go` and `device/receive.go`: encrypted packet data path;
- `device/allowedips.go`: route-to-peer prefix trie;
- `conn/bind_std.go`: UDP binding;
- `tun/tun.go`: host TUN abstraction.

Principal drawbacks:

- UDP is a hard dependency for the normal protocol;
- a compact fixed protocol is easier to classify than browser-shaped traffic;
- DNS, default routes, split tunneling, MTU, kill-switch behavior, and leak prevention sit outside the protocol;
- one fixed server address remains an obvious availability and reputation dependency.

### OpenVPN

**Role:** mature feature-heavy VPN baseline.

OpenVPN separates a TLS control channel from an encrypted data channel and supports many historical compatibility modes.

```text
TUN/TAP packet
  → OpenVPN framing and packet identifiers
  → negotiated data-channel cipher
  → UDP or TCP carrier
  → server routing/bridging
```

Code navigation:

- `src/openvpn/openvpn.c`: process lifecycle;
- `forward.c`: packet forwarding loop;
- `ssl.c` and `ssl_pkt.c`: TLS control-channel state;
- `crypto.c`: data-channel cryptography;
- `reliable.c`: reliable control messages;
- `socket.c` and `tun.c`: network and virtual-interface integration.

Principal drawbacks:

- large configuration and compatibility surface;
- TCP carrier can create nested retransmission and head-of-line blocking;
- protocol and active-response fingerprints can survive payload encryption;
- certificates, plugins, ciphers, compression history, routing, and platform differences increase misconfiguration risk.

### Shadowsocks

**Role:** compact encrypted proxy comparator.

Shadowsocks forwards TCP streams and UDP datagrams using password-derived keys and AEAD records. It does not inherently claim to be normal HTTPS.

```text
SOCKS/TUN request
  → destination address encoding
  → AEAD salt/subkey and records
  → TCP stream or UDP datagram
  → server decrypts and connects to destination
```

Code navigation in `shadowsocks-rust`:

- `crates/shadowsocks/src/relay/tcprelay/aead.rs`;
- `crates/shadowsocks/src/relay/tcprelay/aead_2022.rs`;
- `crates/shadowsocks/src/relay/tcprelay/crypto_io.rs`;
- `crates/shadowsocks/src/relay/udprelay/aead.rs`;
- local and server relay code under `crates/shadowsocks-service/src/`.

Principal drawbacks:

- high-entropy opaque traffic can be treated as a feature rather than an absence of features;
- metadata still exposes the server, duration, packet sizes, and aggregate behavior;
- transparent proxy, DNS, UDP association, FakeDNS, and TUN behavior vary by implementation;
- legacy cipher compatibility must not be confused with safe modern profiles.

### VLESS + REALITY in Xray-core

**Role:** native implementation candidate for a TLS-facing stream proxy.

VLESS supplies proxy request semantics. REALITY changes the TLS-facing authentication and unauthenticated behavior. These are separate layers and should not be collapsed into one protocol label.

```text
application stream
  → VLESS request/addons encoding
  → selected flow and transport
  → REALITY/TLS-facing handshake
  → TCP, XHTTP, HTTP/2, HTTP/3, or related carrier
```

Code navigation:

- `proxy/vless/encoding/encoding.go`: request/response framing;
- `proxy/vless/outbound/outbound.go` and `inbound/inbound.go`: relay lifecycle;
- `transport/internet/reality/reality.go`: REALITY handshake behavior;
- `transport/internet/reality/config.go`: configuration transformation;
- `transport/internet/tls/ech.go`: separate ECH support and its boundary.

Principal drawbacks:

- the number of flow, transport, security, and version combinations is itself an operational risk;
- endpoint address, session timing, byte counts, and application behavior remain observable;
- TLS-facing similarity does not imply full browser/application equivalence;
- current behavior is implementation-led, so configuration examples can become stale quickly;
- downstream reuse must respect MPL file-level obligations and any licenses of combined components.

### Hysteria2

**Role:** QUIC path candidate for lossy and high-latency networks.

Hysteria2 combines QUIC/TLS with proxy commands, congestion-control choices, UDP handling, masquerade, and optional obfuscation.

```text
TCP stream or UDP datagram
  → Hysteria proxy command/framing
  → QUIC stream or datagram
  → TLS-authenticated UDP session
  → Hysteria edge
```

Code navigation:

- `PROTOCOL.md`: committed protocol description;
- `core/internal/protocol/proxy.go`: command framing;
- `core/client/client.go` and `core/server/server.go`: session lifecycle;
- `core/internal/congestion/brutal/brutal.go`: configured-rate congestion behavior;
- `core/internal/congestion/bbr/bbr_sender.go`: BBR implementation;
- `extras/obfs/salamander.go`: optional obfuscation;
- `extras/masq/server.go`: unauthenticated HTTP behavior;
- `extras/transport/udphop/conn.go`: UDP port-hopping transport.

Principal drawbacks:

- when UDP/QUIC is impaired, the path can fail while ordinary TCP still works;
- throughput-oriented congestion choices can produce burstiness, fairness, loss, or provider-policy problems;
- QUIC Initial behavior, endpoint IP, timing, and flow shape remain visible;
- optional masquerade, obfuscation, and port hopping introduce additional state and failure surfaces;
- one successful HTTP/3 probe is not evidence that a long proxy session will remain viable.

### TUIC v5

**Role:** specification reference, not a native implementation candidate.

The inspected repository contains a compact protocol document and explicitly states that it does not contain an official implementation. The command set is Authenticate, Connect, Packet, Dissociate, and Heartbeat over QUIC.

Principal drawbacks:

- no official implementation in the specification repository;
- error handling is under-specified, so implementations can diverge;
- 0-RTT requires replay-aware application semantics;
- UDP, QUIC, NAT, MTU, and path-quality dependencies remain;
- interoperability must be measured between named implementations rather than inferred from the protocol name.

For Edge, TUIC should initially be treated as a cross-implementation comparison inside sing-box or another maintained core, not as a standalone code dependency.

### NaiveProxy

**Role:** browser-stack camouflage comparator.

NaiveProxy reuses Chromium's networking stack for TLS and HTTP/2 or HTTP/3 CONNECT. Its strongest architectural idea is to reuse a real browser stack rather than manually copy a few TLS parameters.

```text
local SOCKS stream
  → Chromium HTTP CONNECT client
  → TLS + HTTP/2 or HTTP/3 frontend
  → authenticated forward proxy
  → destination
```

The project additionally documents padding of early payloads and selected HTTP/2 frames, plus application-layer routing for unauthenticated probes.

Principal drawbacks:

- Chromium-derived build and update cost is much larger than a focused transport library;
- the traffic-shape argument weakens when releases lag current Chrome;
- proxy sessions can still differ from ordinary browsing in duration, stream mix, volume, and reuse;
- the master branch is rebased across Chromium imports, so exact tags—not branch names—must own reproducibility;
- HTTP frontend, proxy authentication, certificates, and origin content must all remain coherent.

### sing-box

**Role:** local multi-protocol platform candidate, not a new wire protocol.

sing-box integrates TUN, DNS, routing, process matching, and many protocol adapters. This aligns with Ordivon Link's desired position above replaceable data planes.

```text
local TUN / SOCKS / application
  → sing-box inbound
  → DNS and route decision
  → selected outbound adapter
  → protocol-specific data plane
```

Code navigation:

- `box.go`: composition and lifecycle;
- `route/router.go`: routing state;
- `protocol/tun/inbound.go`: TUN integration;
- `protocol/vless/outbound.go`;
- `protocol/hysteria2/outbound.go`;
- `protocol/tuic/outbound.go`;
- `protocol/shadowsocks/outbound.go`;
- `protocol/naive/outbound.go`.

Principal drawbacks:

- breadth creates upgrade and configuration drift;
- DNS, routing, TUN, and all transports can share one process failure domain;
- adapter support does not prove semantic identity with native implementations;
- debugging requires preserving the distinction between Ordivon policy, sing-box orchestration, and protocol data-plane failures;
- GPL obligations constrain redistribution choices.

## Cross-cutting drawback matrix

| Failure surface | WireGuard | OpenVPN | Shadowsocks | VLESS/REALITY | Hysteria2 | TUIC | NaiveProxy | sing-box |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed endpoint dependency | high | high | high | high | high | high | high | depends on configuration |
| UDP hard dependency | yes | optional | partial | optional | yes | yes | HTTP/3 mode | depends on outbound |
| Large configuration surface | low | high | medium | high | medium | implementation-dependent | medium | very high |
| Browser-like outer behavior | no | no | no | partial/TLS-facing | partial HTTP/3 | not guaranteed | strongest comparator | depends on outbound |
| Active-probe resistance | no protocol claim | limited | implementation-dependent | explicit REALITY goal | masquerade/obfs options | implementation-dependent | frontend routing | depends on outbound |
| Native full-device integration | TUN | TUN/TAP | implementation-dependent | implementation-dependent | implementation-dependent | implementation-dependent | local proxy | TUN platform |
| Source reproducibility risk | low | medium | low | medium due rapid evolution | medium | high due no official implementation | high unless pinned to tags | medium |

The table is not a ranking. A low-complexity protocol may be easy to classify but easy to operate correctly. A browser-shaped protocol may reduce one class of signal while imposing much higher build and lifecycle cost.

## What Ordivon should measure

The current reachability, transfer, and sustained-response probes are necessary but insufficient. Protocol evaluation should add evidence in this order:

### P0 — adapter identity

Record for every run:

- implementation name and exact version or source revision;
- rendered configuration digest without secrets;
- selected carrier and security mode;
- edge identity and provider/region label;
- host route and TUN ownership facts that are actually controlled.

### P1 — transport viability

Measure separately:

- handshake success and phase timing;
- TCP and UDP target reachability through the established transport;
- bounded transfer throughput and time to first byte;
- sustained active connection lifetime;
- idle connection lifetime;
- reconnect time after server-side close.

### P2 — path stress

Add controlled tests for:

- packet loss and reordering;
- MTU and fragmentation sensitivity;
- IPv4 versus IPv6;
- network transition between mobile carriers or interfaces;
- UDP impairment with a TCP control path;
- concurrent streams and head-of-line behavior;
- DNS path and leak checks.

### P3 — observable-shape evidence

Packet capture should remain local and bounded. Record derived facts rather than committing raw personal traffic:

- outer destination and port category;
- TCP/UDP/QUIC selection;
- handshake packet count and sizes;
- burst and idle distributions;
- session duration;
- retransmission/loss indicators;
- whether unauthenticated probes receive ordinary content, silence, or protocol-specific errors.

This evidence can show differences between candidates. It cannot prove that a path is “undetectable.”

## Selection implications for Edge / Link

The current architectural hypothesis is:

```text
sing-box
  = local TUN, DNS, routing, and replaceable adapter orchestration

Xray-core VLESS/REALITY
  = native reference path for one TCP/TLS-facing candidate

Hysteria2 official core
  = native reference path for one QUIC/high-loss candidate

NaiveProxy
  = browser-stack comparison, not the default deployment

WireGuard and OpenVPN
  = clean VPN baselines

Shadowsocks and TUIC
  = protocol-shape/interoperability comparators
```

No production winner should be selected from architectural claims alone. Edge A/B should expose at least one TCP/TLS-oriented path and one UDP/QUIC-oriented path, then use repeated named-network evidence to determine where each fails.

## Source-handling rules

1. Never vendor upstream repositories into this repository merely for study.
2. Pin exact revisions in `config/transports/protocols.toml`.
3. Clone or fetch upstreams into an ignored external cache.
4. Treat file paths as navigation hints tied to the pinned revision, not permanent APIs.
5. Do not copy implementation code unless a concrete adapter requires it and its license has been reviewed.
6. Never commit endpoints, credentials, certificates, private keys, subscription links, or personal packet captures.
7. Separate protocol defects from implementation defects, configuration defects, and path defects.
