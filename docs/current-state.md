# Current state

## Implemented

The P0/P1 foundation currently provides:

- Rust workspace with `edge-model`, `edge-probe`, `edge-wire`, and `edge-transport-quic`;
- minimum domain objects for devices, edges, targets, transports, probe results, and route decisions;
- validated TOML registries for service targets, a bounded transfer target, and a QUIC control target;
- HTTP/1.1 over TLS and HTTP/3-only over QUIC observations through the system `curl` data plane;
- three explicit probe kinds: reachability, transfer, and connection lifetime;
- repeated collection with collection identity, sample index, and start-to-start cadence;
- DNS, connect, TLS, TTFB, completion, bytes, throughput, connection count, and HTTP-version fields;
- stable NDJSON observations, grouped JSON summaries, and Markdown reports;
- backward reading of the first observation schema;
- a validated transport catalog with pinned upstream revisions, source status, licenses, protocol layers, carriers, limitations, and code entry points;
- a source-level protocol study covering WireGuard, OpenVPN, Shadowsocks, VLESS/REALITY, Hysteria2, TUIC, NaiveProxy, and sing-box;
- a frozen Baseline v0 charter, wire specification, security model, and controlled path test plan;
- pure `edge-wire` support for QUIC varints, bounded control frames, address encoding, strict TCP open semantics, confirmed UDP associations, stable errors, negotiated limits, and legal state transitions;
- a localhost-only Quinn/rustls reference adapter with TLS 1.3, exact ALPN, mandatory client certificates, certificate-derived device identifiers, disabled early data, disabled server migration, loopback-only target policy, TCP relay, UDP relay, liveness, cleanup, and idle expiry;
- integration tests proving trusted mTLS, rejection of an untrusted client certificate, rejection of a certificate/HELLO identity mismatch, default denial of non-loopback targets, TCP echo relay, and UDP echo relay without public network access or host-route changes;
- tests that do not require public network access.

## Measurement meaning

`connection_lifetime` currently means one response-body connection remained active until the requested deadline while data continued to flow. It does not prove idle connection survival, application-session continuity, stream migration, or task recovery.

A live result describes only the named process, network label, route label, and time window. `--no-env-proxy` disables application proxy environment variables but cannot prove that Windows, WSL, a VPN, a TUN device, the router, the ISP, or an upstream provider did not alter the packet path.

## Not implemented

- seven completed days of evidence;
- controlled home, school, hotspot, mobile, VPN, and WARP comparisons;
- packet-loss and retransmission telemetry;
- idle long-connection, network-migration, or application-session tests;
- Edge A or Edge B;
- production certificate issuance, rotation, revocation, or secret storage;
- public Baseline endpoint and direct-no-VPN versus Surfshark path evidence;
- sing-box, Xray-core, Hysteria2, or NaiveProxy adapters;
- route selection, automatic failover, deployment, secrets, runners, backups, or host-route mutation.

## Next evidence gate

1. Add malformed-input/property/fuzz coverage and targeted resource-limit, idle-expiry, wrong-ALPN, and shutdown tests around the now-working localhost adapter.
2. Design production device and Edge certificate issuance, rotation, revocation, and external secret storage without committing key material.
3. Package the reference server and client as explicit experimental commands while preserving the default loopback-only target policy.
4. Only then create a direct Edge and run the controlled Cloudflare HTTP/3, direct TCP, direct Baseline QUIC, and Surfshark comparison matrix.
