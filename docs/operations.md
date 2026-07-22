# Operations

## Prerequisites

- Rust 1.95 or newer;
- `curl` with HTTP/3 support for QUIC observations;
- outbound DNS, TCP/443, and UDP/443 as allowed by the current network.

Check the data plane:

```bash
curl --version
```

The feature list must contain `HTTP3` for `--protocol quic` to be meaningful.

## Run a baseline

```bash
cargo run -p edge-probe -- run \
  --targets config/targets/default.toml \
  --network wsl-current \
  --route direct-process \
  --protocol all \
  --repeat 3 \
  --timeout-seconds 15 \
  --no-env-proxy \
  --output artifacts/baseline/wsl-current.ndjson
```

Use route names that describe controlled facts:

- `direct-process`: application proxies disabled with `curl --noproxy '*'`;
- `inherited-environment`: normal process environment;
- `current-vpn`: only when the VPN is explicitly known to be active;
- `warp`: only when WARP is explicitly known to be active;
- `edge-a` or `edge-b`: only after those nodes exist.

Do not label a result `direct` merely because no proxy environment variable exists.

## Compare and report

```bash
cargo run -p edge-probe -- compare \
  --input artifacts/baseline/wsl-current.ndjson \
  --output artifacts/baseline/wsl-current-summary.json

cargo run -p edge-probe -- report \
  --input artifacts/baseline/wsl-current.ndjson \
  --output artifacts/baseline/wsl-current-report.md
```

Summaries group by network, route, protocol, and target. P50 and P95 use successful samples only. A failed sample still contributes to sample count and success rate.

## Raw evidence handling

Raw baseline artifacts are ignored by Git. Before sharing any result, review:

- `remote_ip`;
- network and route labels;
- timestamps;
- target list;
- stderr fragments.

## Failure interpretation

A failed HTTP/3-only probe means the selected path did not complete that observation. It does not by itself prove UDP blocking: the target may not offer HTTP/3, DNS may differ, local `curl` may be misconfigured, or the handshake may fail for another reason. Repeated controlled comparisons are required.
