# Current state

## Implemented

Phase 1 establishes a measurement-only foundation:

- Rust workspace with `edge-model` and `edge-probe`;
- minimum domain objects for devices, edges, targets, transports, probe results, and route decisions;
- TOML target registry validation;
- HTTP/1.1 over TLS probes;
- HTTP/3-only probes as the initial QUIC observation path;
- phase timing extraction from `curl` JSON output;
- stable NDJSON observations;
- grouped JSON comparison summaries;
- Markdown reports;
- unit and command-runner tests that do not depend on the public network.

## Not implemented

- Edge A or Edge B;
- sing-box, Xray-core, Hysteria2, or NaiveProxy adapters;
- route selection or automatic failover;
- node bootstrap, deployment, secret rotation, rollback, or backup;
- GitHub ephemeral runners;
- WARP or VPN lifecycle control;
- packet-loss, retransmission, sustained-throughput, or long-connection tests;
- continuous seven-day collection;
- any custom transport or cryptographic primitive.

## Current evidence boundary

A live baseline produced from WSL describes only that process and time window. `--no-env-proxy` disables application proxy environment variables for `curl`, but cannot prove that Windows, WSL, a VPN, a TUN device, the router, the ISP, or an upstream provider did not alter the path.

## Next admissible work

1. Collect repeated baselines from named network conditions.
2. Add sustained transfer and connection-lifetime probes.
3. Compare direct-process, inherited-proxy, current VPN, and WARP only when those routes can be explicitly controlled and named.
4. Create two experimental Edge nodes only after the measurement format is stable enough to compare them.
