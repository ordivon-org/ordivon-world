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
- periodic refresh failures retain the last known snapshot and expose its age; snapshots older than `max(3 × interval, 60 seconds)` are explicitly stale;
- SQLite uses WAL, normal synchronous mode, a five-second busy timeout, `trusted_schema=OFF`, schema metadata, and fallback past a corrupt newest snapshot;
- snapshot and event retention are bounded;
- SSE consumers can reconnect without affecting collection and receive a periodic freshness update even when no new snapshot is committed;
- probes have a hard process deadline, bounded stdout/stderr retention, and no orphan child process after timeout;
- systemd may restart the single process after failure under a validated `DynamicUser` sandbox;
- no automatic network mutation exists in this phase, preventing a faulty control loop from disconnecting the host.


## Local HTTP boundary

The Edge listener is loopback-only. Before requests reach Axum routing, an outer Tower service:

- allows only `localhost`, `127.0.0.1`, and `[::1]` Host values with optional numeric ports;
- rejects absolute-form requests, percent-encoded paths, dot segments, backslashes, non-ASCII paths, and unexpected path characters;
- leaves parser-level malformed requests to Hyper, which fails closed before the application service.

All application responses, including rejected requests, receive the same privacy and browser-security headers. No CORS origin is enabled.

## External dependencies

Retained data planes:

- system `curl` for HTTP/TLS/HTTP3 behavior;
- Windows Surfshark services and adapters;
- WSL/Linux routing and resolver facilities;
- systemd for process supervision;
- optional Cloudflare Tunnel for other Ordivon management surfaces.

The new local Web plane does not require Gatus, Grafana, Prometheus, Caddy, CoreDNS, or Docker.
