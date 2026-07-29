# Ordivon Baseline v0 charter

## Purpose

Ordivon Baseline v0 is a private, single-user reference protocol for measuring and understanding secure overseas relay behavior. It exists to provide a small, explicit zero point for later transport, camouflage, failover, and routing experiments.

The first version must make every connection state, wire field, error, resource limit, and measurement claim understandable without reading a feature-heavy proxy core.

## Frozen decisions

### D-001 — private single-user scope

The protocol connects devices controlled by one user to Edge nodes controlled by the same user. It is not a public proxy, subscription service, multi-user panel, traffic resale system, or anonymous relay network.

### D-002 — relay semantics

The protocol carries:

- reliable ordered TCP-style byte streams;
- message-preserving UDP datagrams.

It does not carry arbitrary IP packets in v0. TUN, route installation, DNS interception, kill switches, and full-device transparency remain outside the protocol core.

### D-003 — QUIC-first reference transport

The reference carrier is:

```text
UDP
→ QUIC v1
→ TLS 1.3
→ ALPN ordivon-baseline/0
→ Ordivon control, TCP streams, and UDP datagrams
```

The implementation must use a maintained QUIC/TLS library. It must not implement new cryptography, a new TLS handshake, packet recovery, flow control, or congestion control.

### D-004 — identity

Every device has an independent client certificate and private key. Every Edge has a server certificate rooted in an Ordivon-controlled trust anchor. TLS client authentication is required. The v0 device identifier is the first 16 bytes of SHA-256 over the authenticated leaf certificate DER, and the server rejects a `HELLO` that claims a different identifier.

TLS 0-RTT application data is disabled in v0. Session resumption may be evaluated later without early application data.

### D-005 — deliberate omissions

Baseline v0 contains no:

- traffic camouflage or protocol mimicry;
- padding policy;
- port hopping;
- domain fronting;
- custom congestion controller;
- transparent QUIC path migration;
- automatic replay of failed application streams;
- TUN integration;
- multi-path aggregation;
- public user/account layer;
- self-designed cryptographic primitive.

These omissions are intentional. They keep later changes measurable against a stable baseline.

## Real network constraint

The current user environment has three materially different paths:

```text
A. direct-no-vpn
   China carrier path without Surfshark.
   Many overseas destinations are unavailable or impaired.

B. surfshark-vpn
   Known working overseas egress and current practical control path.

C. cloudflare-reachable
   ordivon.com and Cloudflare-hosted HTTP services are reachable without Surfshark.
```

This fact changes deployment and testing, but it does not change the v0 wire protocol.

## Plane separation

```text
┌──────────────────────────────────────────────────────────┐
│ Control / bootstrap / recovery plane                     │
│ HTTPS and ordinary HTTP/3 through Cloudflare             │
│ Signed manifests, public status, release metadata,       │
│ reachability controls, and recovery instructions         │
└──────────────────────────┬───────────────────────────────┘
                           │ does not carry custom QUIC
                           ▼
┌──────────────────────────────────────────────────────────┐
│ Baseline data plane                                      │
│ custom ALPN ordivon-baseline/0 over direct UDP/443       │
│ client ↔ user-controlled overseas Edge                  │
└──────────────────────────┬───────────────────────────────┘
                           ▼
                    destination services
```

A normal Cloudflare-proxied hostname terminates HTTP/3 as an HTTP service. It must not be assumed to transparently forward an arbitrary custom QUIC ALPN. Cloudflare Tunnel is also not treated as a public arbitrary-UDP ingress for Baseline v0.

Therefore the custom QUIC endpoint must initially be a direct Edge endpoint, normally represented by a DNS-only hostname under the Ordivon domain or by an explicitly pinned IP. The Cloudflare path remains a control and diagnostic path.

## What v0 success means

v0 succeeds when:

1. the wire contract is deterministic and bounded;
2. localhost QUIC/mTLS TCP and UDP relay tests pass;
3. malformed inputs cannot cause unbounded allocation or parser panic;
4. every failure is classified by stable protocol and path evidence;
5. the same direct Edge test can be run under both `direct-no-vpn` and `surfshark-vpn` labels;
6. Cloudflare HTTP/3 controls distinguish general UDP/443 failure from failure specific to the direct Edge or custom protocol.

v0 success does **not** mean that Surfshark has been replaced. Replacement becomes an empirical conclusion only if repeated direct-no-VPN Edge tests succeed with adequate stability and performance.

## Trust and privacy boundary

The Edge necessarily learns destination addresses and connection metadata because it creates the outbound connection. The protocol does not record or inspect application payloads by default.

Never commit:

- device or Edge private keys;
- certificates containing sensitive deployment metadata unless explicitly public;
- endpoint credentials;
- subscription links;
- raw personal packet captures;
- complete browsing histories;
- application payloads.

## Ownership boundary

- `link-wire` owns the pure wire contract, bounded parsing, identifiers, limits, and state transitions.
- `link-transport-quic` owns the localhost reference integration with Quinn, rustls, mTLS, certificate-bound device identity, TCP relay, and UDP associations.
- `link-probe` owns external path observations and comparison evidence.
- Ordivon Link will later own local route selection and recovery policy.
- Ordivon Edge will later own node deployment and lifecycle.
