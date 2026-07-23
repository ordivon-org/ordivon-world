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
- parallel HTTP/TLS checks for a bounded Web registry: at most 32 enabled Web targets, with globally validated public-label target IDs;
- sanitized `EdgeSnapshot` state reduction;
- SQLite storage for snapshots, service checks, and state-change events;
- bounded retention of 25,000 snapshots and 5,000 events;
- Axum HTTP API, explicit snapshot freshness, 15-second SSE freshness updates, and embedded local Web UI;
- hard loopback-only binding, Host allowlisting, and raw request-target validation before Axum routing;
- CSP, frame denial, no-referrer, no-store, COOP/CORP, and restrictive browser permissions headers;
- hard probe-process deadlines, bounded child output capture, SQLite busy recovery, and a systemd example validated with `DynamicUser` and the real WSL/Surfshark observer.

## Privacy guarantees in this phase

The API, SQLite store, events, and application logs contain no public/private IP, remote IP, hostname, username, MAC address, local address, target URL, or raw command output. Status-only child processes are silent, probe output is bounded, and probe results are converted into a smaller sanitized service-health type before persistence.

No Cloudflare route is created for the Web plane. Any future remote exposure requires a separate authentication and disclosure review.

## Current meaning

A `tunneled` path means both conditions were observed:

1. Surfshark service plus a Surfshark-labelled adapter are active on Windows;
2. WSL has both IPv4 `/1` routes through the effective public interface.

An unrelated WireGuard or OpenVPN adapter cannot satisfy the provider check.

It does not prove every packet took a particular physical route. It does not reveal the exit IP.

An IPv6 physical default without an IPv6 tunnel route is reported as a latent risk. Failure to observe IPv6 routes is reported as `unknown`, not as proof that no route exists. The runtime does not call either condition a confirmed leak without a successful public IPv6 observation.

## Not implemented

- Surfshark reconnect, profile, protocol, or location control;
- route, DNS, firewall, adapter, or MTU mutation;
- automatic failover or rollback;
- WARP or remote Edge provider adapters;
- authenticated remote Web access;
- ntfy delivery from the new runtime;
- migration of historical Gatus/Prometheus data;
- retirement of the existing workstation monitoring stack.

## Deep validation completed

The current branch has passed:

- 32 parallel probes, 3,500 HTTP requests at concurrency 64, and 64 concurrent SSE clients;
- twelve forced `SIGKILL` restart cycles with SQLite integrity preserved;
- an external SQLite write lock long enough to make the snapshot stale, followed by automatic recovery;
- real WSL + Surfshark multi-cycle Dogfood with all configured Web targets healthy;
- real Windows Chromium rendering through the Chrome DevTools Protocol;
- API, SSE, database, WAL, application-log, and rendered-DOM privacy scans;
- RustSec dependency audit with no current vulnerability or maintenance warning;
- transient systemd execution with `DynamicUser`; `systemd-analyze security` improved from 7.3/medium to 3.3/OK.

## Next gate

Before retiring the existing workstation monitoring stack:

1. perform an operator-controlled Surfshark disconnect/reconnect and protocol-switch exercise;
2. install the local systemd service only after reviewing the deployment paths;
3. run parallel Dogfood long enough to compare failure and recovery events with the existing stack.
