# Current state

## Implemented

- stable models for targets, transports, observations, route decisions, snapshots, and events;
- reachability, bounded transfer, and sustained-response lifetime probes;
- repeated collection with append-safe NDJSON, JSON comparison, and Markdown reporting;
- a pinned source catalog covering WireGuard, OpenVPN, Shadowsocks, VLESS/REALITY, Hysteria2, TUIC, NaiveProxy, and sing-box;
- local WSL/Windows/Surfshark, route, MTU, DNS, Cloudflare Tunnel, Ordivon MCP, and service-health observation;
- sanitized SQLite snapshot and state-change history;
- a loopback-only read-only Web console with freshness semantics, SSE updates, restrictive headers, and raw request-target validation;
- Baseline v0 bounded wire frames, addresses, errors, negotiated limits, and state machines;
- localhost Quinn/rustls TLS 1.3 mTLS reference transport with certificate-bound device identity, strict TCP relay, confirmed UDP associations, liveness, cleanup, and loopback-only target policy;
- tests that require neither public network access nor host-route mutation.

## Not implemented

- route-selection execution or automatic failover;
- host route, DNS, firewall, TUN, or VPN mutation;
- production device and remote-node certificate lifecycle;
- public Baseline endpoint and repeated direct-no-VPN versus VPN evidence;
- production transport adapters for sing-box, Xray-core, Hysteria2, or NaiveProxy;
- seven-day controlled path evidence;
- Cloudflare fetch, Browser Rendering, R2 artifact execution, or external task receipts;
- local Agent task execution or workspace management.

The final two categories are intentionally excluded: they belong to Ordivon Edge and Ordivon Runtime respectively.
