# Architecture

## Boundary

Ordivon owns path observation, state reduction, service semantics, decision history, recovery policy, and the user-facing control plane. Mature implementations continue to own TLS, QUIC, WireGuard, OpenVPN, DNS serving, and public ingress.

```text
Windows / WSL facts              Web target registry
        │                                │
        ▼                                ▼
  SystemObserver                    edge-probe
        │                                │
        └──────────────┬─────────────────┘
                       ▼
                 EdgeSnapshot
                       │
              ┌────────┴────────┐
              ▼                 ▼
        SQLite event store   broadcast channel
              │                 │
              └────────┬────────┘
                       ▼
              Axum API + SSE
                       │
                       ▼
             embedded local Web UI
```

## Runtime shape

The production target is one modular Rust process:

```text
edge-runtime
├── host observer
├── service probes
├── path-state reducer
├── sanitized event derivation
└── SQLite store

edge-server
├── REST API
├── SSE stream
├── security headers
└── embedded static assets
```

There is no internal message broker, separate frontend server, metrics database, or container dependency.

## State model

Current path states:

- `unknown`: provider state cannot be observed;
- `direct`: Surfshark is detected but no active tunnel is observed;
- `tunneled`: Surfshark and the WSL IPv4 tunnel route are independently observed;
- `degraded`: provider and effective route disagree;
- `failed`: no public IPv4 route can be observed.

Service health is separate from path health. A reachable application does not prove that the intended tunnel is active.

## Persistence

SQLite stores only reduced, sanitized data:

- `snapshots`: complete sanitized Edge snapshots;
- `service_checks`: target ID, state, latency, and failure class;
- `events`: meaningful state transitions.

Raw route output, PowerShell output, target URLs, endpoint IPs, and probe stderr are discarded before persistence. NDJSON remains the explicit import/export format for lower-level measurement evidence, not the Web plane database.

## High-availability behavior

- the server performs an initial observation before accepting requests;
- periodic refresh failures retain the last known snapshot;
- SQLite uses WAL and normal synchronous mode;
- snapshot and event retention are bounded;
- SSE consumers can reconnect without affecting collection;
- systemd may restart the single process after failure;
- no automatic network mutation exists in this phase, preventing a faulty control loop from disconnecting the host.

## External dependencies

Retained data planes:

- system `curl` for HTTP/TLS/HTTP3 behavior;
- Windows Surfshark services and adapters;
- WSL/Linux routing and resolver facilities;
- systemd for process supervision;
- optional Cloudflare Tunnel for other Ordivon management surfaces.

The new local Web plane does not require Gatus, Grafana, Prometheus, Caddy, CoreDNS, or Docker.
