# Current state

## Implemented

### Evidence layer

- Rust workspace with `edge-model` and `edge-probe`;
- validated TOML target registries;
- HTTP/TLS and HTTP/3 observations through the system `curl` data plane;
- reachability, bounded transfer, and sustained-response lifetime probes;
- repeated collection with collection identity and start-to-start cadence;
- NDJSON evidence, grouped JSON summaries, and Markdown reports;
- tests that do not require public network access.

### Read-only Web plane

- `edge-runtime` host observer for WSL route, MTU, DNS mode, Surfshark Windows services/adapters, Cloudflare Tunnel process state, and Ordivon MCP service state;
- independent verification that Surfshark is connected and that WSL IPv4 traffic has the expected split-tunnel route;
- explicit IPv6 route-risk classification without claiming a leak that was not observed;
- parallel HTTP/TLS checks for the minimal Web target registry;
- sanitized `EdgeSnapshot` state reduction;
- SQLite storage for snapshots, service checks, and state-change events;
- bounded retention of 25,000 snapshots and 5,000 events;
- Axum HTTP API, SSE updates, and embedded local Web UI;
- hard loopback-only binding with a non-loopback rejection guard;
- CSP, frame denial, no-referrer, no-store, and restrictive browser permissions headers;
- systemd deployment example with restart and sandboxing controls.

## Privacy guarantees in this phase

The API and SQLite store contain no public/private IP, remote IP, hostname, username, MAC address, local address, raw command output, or target URL. Probe results are converted into a smaller sanitized service-health type before persistence.

No Cloudflare route is created for the Web plane. Any future remote exposure requires a separate authentication and disclosure review.

## Current meaning

A `tunneled` path means both conditions were observed:

1. Surfshark service plus a WireGuard/OpenVPN adapter are active on Windows;
2. WSL has both IPv4 `/1` routes through the effective public interface.

It does not prove every packet took a particular physical route. It does not reveal the exit IP.

An IPv6 physical default without an IPv6 tunnel route is reported as a latent risk. The runtime does not call it a confirmed leak without a successful public IPv6 observation.

## Not implemented

- Surfshark reconnect, profile, protocol, or location control;
- route, DNS, firewall, adapter, or MTU mutation;
- automatic failover or rollback;
- WARP or remote Edge provider adapters;
- authenticated remote Web access;
- ntfy delivery from the new runtime;
- migration of historical Gatus/Prometheus data;
- retirement of the existing workstation monitoring stack.

## Next gate

Run the new Web plane beside the current workstation stack and compare:

1. Surfshark/path-state accuracy across connect, disconnect, and reconnect;
2. service failure and recovery detection;
3. false-degraded rate under normal China-to-overseas latency;
4. SQLite growth and restart recovery;
5. privacy scans of API, database, logs, and browser output.

Only after parallel validation should Gatus, Grafana, Prometheus, or the old shell diagnostics be retired.
