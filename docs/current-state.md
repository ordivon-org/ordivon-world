# Current state

## Implemented

The P0/P1 foundation currently provides:

- Rust workspace with `edge-model` and `edge-probe`;
- minimum domain objects for devices, edges, targets, transports, probe results, and route decisions;
- validated TOML registries for service targets, a bounded transfer target, and a QUIC control target;
- HTTP/1.1 over TLS and HTTP/3-only over QUIC observations through the system `curl` data plane;
- three explicit probe kinds: reachability, transfer, and connection lifetime;
- repeated collection with collection identity, sample index, and start-to-start cadence;
- DNS, connect, TLS, TTFB, completion, bytes, throughput, connection count, and HTTP-version fields;
- stable NDJSON observations, grouped JSON summaries, and Markdown reports;
- backward reading of the first observation schema;
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
- sing-box, Xray-core, Hysteria2, or NaiveProxy adapters;
- route selection, automatic failover, deployment, secrets, runners, backups, or custom transport work.

## Next evidence gate

1. Collect repeated named-network samples without relabeling uncontrolled paths.
2. Compare reachability, transfer, and sustained-response lifetime under the same conditions.
3. Add packet-loss/retransmission and network-transition probes only when their collection method is explicit.
4. Create experimental Edge nodes only after the evidence format is stable enough to compare them fairly.
