# Ordivon Edge / Link

Ordivon Edge is a private, single-user control plane for network paths, critical Web services, and recovery. It does not implement a new VPN, proxy protocol, DNS server, or public multi-user panel.

The project owns the layer above replaceable data planes:

```text
Desired state
→ Observe
→ Verify
→ Select
→ Execute
→ Verify again
→ Recover
```

## Current implementation

The repository now contains three usable layers:

- `edge-model`: stable observations and path-domain types;
- `edge-probe`: HTTP/TLS, HTTP/3, transfer, and connection-lifetime evidence;
- `edge-runtime` + `edge-server`: a read-only local Web control plane with WSL/Surfshark observation, sanitized service health, SQLite history, state-change events, explicit freshness, and SSE updates.

The Web plane is intentionally a modular monolith:

```text
one Rust process
one SQLite file
one loopback HTTP listener
embedded HTML/CSS/JavaScript
```

It does not require Gatus, Grafana, Prometheus, Caddy, Node.js, or a separate database at runtime.

## Privacy boundary

Private identity is excluded by design. The Web API and SQLite store do not retain or return:

- public or private IP addresses;
- usernames or hostnames;
- MAC addresses;
- Windows account paths;
- raw PowerShell, route, DNS, or probe output;
- target URLs or remote endpoint addresses.

The server binds to `127.0.0.1`, rejects non-loopback binds and untrusted Host headers, and validates the raw request target before routing. See [`docs/privacy.md`](docs/privacy.md).

## Run the local Web plane

```bash
cargo run -p edge-server -- \
  --bind 127.0.0.1:8787 \
  --database artifacts/runtime/edge.db \
  --targets config/targets/web.toml
```

Then open:

```text
http://127.0.0.1:8787/
```

Read-only endpoints:

```text
GET /api/v1/health
GET /api/v1/status   # { snapshot, freshness }
GET /api/v1/events?limit=50
GET /events
```

The initial release observes and verifies only. A retained snapshot is marked stale when refreshes stop succeeding; the health endpoint then returns 503 while the last sanitized status remains readable. It does not reconnect Surfshark, alter routes, change DNS, or expose the Web plane through Cloudflare.

## Measurement CLI

The lower-level evidence collector remains available:

```bash
cargo run -p edge-probe -- run \
  --network wsl-current \
  --route host-current \
  --protocol all \
  --repeat 3 \
  --interval-seconds 60 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/reachability.ndjson
```

`--no-env-proxy` disables process-level proxy environment variables only. Windows, WSL, Surfshark, TUN adapters, routers, carriers, and upstream networks may still affect the physical path.

## Product boundary

- **Ordivon Link** observes local paths, chooses routes, and recovers from path failures.
- **Ordivon Edge** provides the local control plane and later manages user-controlled remote anchors.
- **Ordivon Runtime** remains the local Agent execution and recovery system.
- **ordivon-web** remains the public project and release website.

See [`docs/current-state.md`](docs/current-state.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/operations.md`](docs/operations.md).
