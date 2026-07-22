# Ordivon Edge / Link

Ordivon Edge / Link is a single-user transport control and overseas execution project. It is not a proxy subscription service, a multi-user panel, or a new cryptographic protocol.

The project owns the layer above replaceable transport implementations:

```text
Desired state
→ Probe
→ Observe
→ Select
→ Render
→ Execute
→ Verify
→ Fail over
→ Recover
```

## Product boundary

- **Ordivon Link** observes local network paths, chooses routes, and recovers from path failures.
- **Ordivon Edge** manages overseas nodes, deployment workers, ephemeral CI runners, backups, and long-running operations.
- **Ordivon Runtime** remains the local Agent task execution and recovery system.
- **ordivon-web** remains the public website and release surface.

## Phase 1: facts before infrastructure

The first phase implements P0 and P1 only:

- a thin domain model;
- a target registry;
- reproducible HTTP/TLS and HTTP/3/QUIC probes using the system `curl` data plane;
- NDJSON observations;
- JSON comparison summaries;
- Markdown reports;
- a current WSL network baseline.

It does **not** deploy nodes, install proxy cores, alter host routes, manage secrets, or change the running Ordivon Runtime.

## Quick start

```bash
cargo test --workspace
cargo run -p edge-probe -- run \
  --targets config/targets/default.toml \
  --network wsl-current \
  --route direct-process \
  --protocol all \
  --no-env-proxy \
  --output artifacts/baseline/current.ndjson

cargo run -p edge-probe -- compare \
  --input artifacts/baseline/current.ndjson \
  --output artifacts/baseline/current-summary.json

cargo run -p edge-probe -- report \
  --input artifacts/baseline/current.ndjson \
  --output artifacts/baseline/current-report.md
```

`direct-process` means that the probe disables application-level proxy environment variables. A host VPN, WSL route, TUN adapter, carrier policy, or upstream network may still affect the physical path. Route labels are observations, not claims about the complete packet path.

## Current status

See [`docs/current-state.md`](docs/current-state.md). Architecture and operating semantics are in [`docs/architecture.md`](docs/architecture.md) and [`docs/operations.md`](docs/operations.md).
