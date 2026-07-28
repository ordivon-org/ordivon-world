# Operations

## Prerequisites

- Rust 1.95 or newer;
- system `curl`;
- WSL networking commands (`ip`);
- Windows PowerShell interop for Surfshark observation;
- `wireguard-tools` and `iproute2` for optional isolated VPN execution;
- outbound DNS and TCP/443 for Web target checks.

HTTP/3 measurement additionally requires a `curl` build whose feature list contains `HTTP3`.

## Local Web plane

Run in the repository:

```bash
cargo run -p link-console -- \
  --bind 127.0.0.1:8787 \
  --database artifacts/runtime/edge.db \
  --targets config/targets/web.toml \
  --interval-seconds 30
```

Open:

```text
http://127.0.0.1:8787/
```

The first snapshot completes before the server starts accepting requests. Each later refresh retains the previous known state if collection fails. A snapshot older than `max(3 × interval, 60 seconds)` is returned with `freshness.stale=true`; `/api/v1/health` then returns HTTP 503 while `/api/v1/status` remains readable.

### API

```bash
curl -fsS http://127.0.0.1:8787/api/v1/health
curl -fsS http://127.0.0.1:8787/api/v1/status | jq '{snapshot, freshness}'
curl -fsS 'http://127.0.0.1:8787/api/v1/events?limit=20' | jq
curl -N http://127.0.0.1:8787/events
```

The API is sanitized. Do not add raw route output, IP addresses, target URLs, host identity, adapter names, or probe stderr to response models.

### Binding policy

The listener is hard-restricted to loopback addresses. Non-loopback binds are rejected and there is no override in this phase. Requests must also use a loopback Host value and an unambiguous raw path; DNS-rebinding names, encoded paths, dot segments, backslashes, and absolute-form request targets are rejected. A future reverse proxy or authenticated tunnel must connect to the loopback listener and requires a separate boundary design. The current phase must not be added to Cloudflare Tunnel.

### Database

Default development path:

```text
artifacts/runtime/edge.db
```

The database uses WAL, a five-second busy timeout, `trusted_schema=OFF`, explicit schema metadata, bounded retention, and sanitized records. It may be deleted during development to start with an empty history. Production state belongs outside the repository, such as `/var/lib/ordivon-link/edge.db`.

### systemd example

A hardened example is committed at:

```text
deploy/systemd/ordivon-link.service
```

Before installation:

1. build and install the binary as `/usr/local/bin/ordivon-link`;
2. copy `config/targets/web.toml` to `/etc/ordivon-link/targets.toml`;
3. verify Windows PowerShell interop under the selected service identity;
4. keep the listener on `127.0.0.1`;
5. do not stop the existing monitoring stack until parallel validation is complete.

## Service-check semantics

The Web registry uses HTTP HEAD checks through `link-probe`:

- any HTTP status from 100 through 599 proves the HTTP endpoint answered;
- success does not imply authorization or business-level success;
- a successful result at or above eight seconds is `degraded`;
- a transport/tool failure is `failed`;
- the Web runtime accepts at most 32 enabled HTTP/TLS targets; the shared registry accepts at most 64 targets;
- target IDs are bounded public labels: lowercase ASCII letters, digits, `-`, and `_`, beginning with a lowercase letter;
- each probe process has a hard deadline, captures at most 64 KiB stdout and 8 KiB stderr, and still drains both pipes completely;
- remote IPs, target URLs, and stderr are discarded before persistence.

## Reachability evidence collection

```bash
cargo run -p link-probe -- run \
  --targets config/targets/default.toml \
  --network wsl-current \
  --route host-current \
  --protocol all \
  --repeat 3 \
  --interval-seconds 60 \
  --timeout-seconds 15 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/reachability.ndjson
```

`--interval-seconds` is a start-to-start cadence. Completed observations are appended after each round.

A positive QUIC control proves only that one UDP/QUIC path worked in that time window:

```bash
cargo run -p link-probe -- run \
  --targets config/targets/quic-control.toml \
  --network wsl-current \
  --route host-current \
  --protocol quic \
  --repeat 3 \
  --no-env-proxy \
  --output artifacts/baseline/quic-control.ndjson
```

## Transfer and connection lifetime

```bash
cargo run -p link-probe -- transfer \
  --targets config/targets/transfer.toml \
  --network wsl-current \
  --route host-current \
  --protocol http-tls \
  --timeout-seconds 60 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/transfer.ndjson

cargo run -p link-probe -- lifetime \
  --targets config/targets/transfer.toml \
  --network wsl-current \
  --route host-current \
  --protocol http-tls \
  --duration-seconds 15 \
  --rate-limit-bytes-per-second 65536 \
  --no-env-proxy \
  --truncate-output \
  --output artifacts/baseline/lifetime.ndjson
```

The lifetime probe is a sustained response-body test, not idle keepalive, stream migration, or task recovery.

## Compare and report

```bash
cargo run -p link-probe -- compare \
  --input artifacts/baseline/reachability.ndjson \
  --output artifacts/baseline/reachability-summary.json

cargo run -p link-probe -- report \
  --input artifacts/baseline/reachability.ndjson \
  --output artifacts/baseline/reachability-report.md
```

## Raw evidence handling

Raw measurement artifacts can contain endpoint IPs, timestamps, labels, URLs, and stderr. They remain ignored by Git and must be reviewed before sharing.

The Web plane has a stricter boundary: it stores only sanitized reduced state. See [`privacy.md`](privacy.md).


## Isolated VPN namespace

Install the explicit control-plane scripts and systemd template:

```bash
sudo scripts/install-ordivon-vpn
sudo ordivon-vpn-keypair
ordivon-vpn doctor jp-tok
```

`ordivon-vpn-keypair` accepts the public key visibly and the matching private key through hidden terminal input. It rejects malformed or mismatched pairs before changing local state, backs up the previous root-only key/configuration set, and atomically rerenders every profile. `doctor` and `up` fail closed if a rendered profile no longer derives the canonical installed public key. `ordivon-vpn up` refuses to start while Windows Surfshark is active. It creates WireGuard in the WSL root namespace, moves the interface into the isolated namespace, and leaves the encrypted UDP socket on the root network path; no veth, NAT, IP forwarding, or firewall mutation is required.

Start one profile and run only selected commands through it:

```bash
sudo ordivon-vpn up jp-tok
ordivon-vpn status
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn down
```

The configuration directory is outside the repository. Do not copy private keys, rendered configuration, endpoint inventory, or egress evidence into Git. See [`vpn-namespace.md`](vpn-namespace.md).

### Surfshark route-state comparison

```bash
sudo surfshark-measure before
# Connect Surfshark in Windows, then wait 15–20 seconds.
sudo surfshark-measure after
sudo surfshark-measure compare
```

The state gates prevent a connected sample from being mislabeled as `before` or a disconnected sample as `after`. The utility stores root-only local evidence and never records WireGuard key values.

### Surfshark profile discovery

Validate all rendered profiles, then disconnect Windows Surfshark and scan them sequentially:

```bash
sudo surfshark-profile-scan validate
sudo surfshark-profile-scan scan
```

The scan records handshake reachability, endpoint UDP return evidence, HTTPS phase timings, and a bounded 1 MiB throughput sample. Results are root-only, resumable, and reduced to JSONL/CSV/ranking artifacts under `/root/backups/ordivon-link/surfshark-profile-scan`. The scanner remains an explicit measurement command; it does not enable automatic route selection or failover.
