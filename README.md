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

## Current phase: facts before infrastructure

P0 and P1 establish a measurement-only foundation:

- a thin domain model and validated target registries;
- HTTP/TLS and HTTP/3/QUIC reachability observations;
- repeated collection with a start-to-start cadence;
- bounded object-transfer measurements;
- single-response connection-lifetime measurements;
- NDJSON evidence, JSON comparisons, and Markdown reports.

The project does **not** yet deploy nodes, install proxy cores, alter host routes, manage secrets, or change the running Ordivon Runtime.

## Quick start

Reachability:

```bash
cargo run -p edge-probe -- run \
  --network wsl-current \
  --route direct-process \
  --protocol all \
  --repeat 3 \
  --interval-seconds 60 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/reachability.ndjson
```

Transfer and sustained-response lifetime:

```bash
cargo run -p edge-probe -- transfer \
  --network wsl-current \
  --route direct-process \
  --protocol http-tls \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/transfer.ndjson

cargo run -p edge-probe -- lifetime \
  --network wsl-current \
  --route direct-process \
  --protocol http-tls \
  --duration-seconds 15 \
  --rate-limit-bytes-per-second 65536 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/lifetime.ndjson
```

Reports:

```bash
cargo run -p edge-probe -- report \
  --input artifacts/baseline/reachability.ndjson \
  --output artifacts/baseline/reachability.md
```

`direct-process` means only that application-level proxy environment variables are disabled for `curl`. A host VPN, WSL route, TUN adapter, carrier policy, or upstream network may still affect the physical path. Route labels are observations, not claims about the complete packet path.

See [`docs/current-state.md`](docs/current-state.md), [`docs/architecture.md`](docs/architecture.md), and [`docs/operations.md`](docs/operations.md).
