# Operations

## Prerequisites

- Rust 1.95 or newer;
- `curl` with HTTP/3 support for QUIC observations;
- outbound DNS, TCP/443, and UDP/443 as permitted by the current network.

Check the data plane:

```bash
curl --version
```

The feature list must contain `HTTP3` before QUIC observations are meaningful.

## Reachability collection

Reachability uses HTTP HEAD and does not download response bodies.

```bash
cargo run -p edge-probe -- run \
  --targets config/targets/default.toml \
  --network wsl-current \
  --route direct-process \
  --protocol all \
  --repeat 3 \
  --interval-seconds 60 \
  --timeout-seconds 15 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/reachability.ndjson
```

`--interval-seconds` is a start-to-start cadence. If one round exceeds the interval, the next begins immediately. Results are appended after every round so completed observations survive a later interruption.

For an externally supervised seven-day hourly collection, use 168 rounds with a 3600-second cadence. The repository does not install or start a background collector automatically.

A positive QUIC control proves that at least one UDP/QUIC path worked during that window:

```bash
cargo run -p edge-probe -- run \
  --targets config/targets/quic-control.toml \
  --network wsl-current \
  --route direct-process \
  --protocol quic \
  --repeat 3 \
  --no-env-proxy \
  --output artifacts/baseline/quic-control.ndjson
```

A failed control still does not prove that UDP is blocked; the endpoint, DNS result, client implementation, or transient path may have failed.

## Transfer collection

```bash
cargo run -p edge-probe -- transfer \
  --targets config/targets/transfer.toml \
  --network wsl-current \
  --route direct-process \
  --protocol http-tls \
  --timeout-seconds 60 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/transfer.ndjson
```

The committed transfer target is a bounded experimental dependency. A target outage or behavior change must not be interpreted as a route failure without a control target.

## Sustained-response lifetime

```bash
cargo run -p edge-probe -- lifetime \
  --targets config/targets/transfer.toml \
  --network wsl-current \
  --route direct-process \
  --protocol http-tls \
  --duration-seconds 15 \
  --rate-limit-bytes-per-second 65536 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/lifetime.ndjson
```

Success requires one connection, non-zero transferred bytes, and at least 95% of the requested duration. This is a sustained response-body test, not an idle keepalive or session-recovery test.

## Route labels

Use labels that describe controlled facts:

- `direct-process`: application proxies disabled with `curl --noproxy '*'`;
- `inherited-environment`: normal process environment;
- `current-vpn`: only when the VPN is explicitly known to be active;
- `warp`: only when WARP is explicitly known to be active;
- `edge-a` or `edge-b`: only after those nodes exist.

Do not label a result `direct` merely because no proxy environment variable exists.

## Compare and report

```bash
cargo run -p edge-probe -- compare \
  --input artifacts/baseline/reachability.ndjson \
  --output artifacts/baseline/reachability-summary.json

cargo run -p edge-probe -- report \
  --input artifacts/baseline/reachability.ndjson \
  --output artifacts/baseline/reachability-report.md
```

Summaries group by probe kind, network, route, protocol, and target. Success rate includes all samples; P50/P95 timings, bytes, and throughput use successful samples only.

## Raw evidence handling

Raw baseline artifacts are ignored by Git. Before sharing results, review remote IPs, network and route labels, timestamps, target URLs, and stderr fragments.

A failed HTTP/3-only observation does not by itself prove UDP blocking. Repeated controlled comparisons are required.
