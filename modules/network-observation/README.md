# Network Observation for Ordivon World

This module supplies source-native network observations and private local operations to Ordivon World. Legacy `link-*` names preserve command and evidence compatibility; there is no independent Link authority or production data plane.

## Active default workspace

```text
link-model ← link-probe ← link-observer ← link-console
```

It provides bounded HTTPS/QUIC reachability, transfer, and connection-lifetime probes; reduced route/service observations; sanitized SQLite history; and a loopback-only console. These are method- and time-conditioned observations, not complete path truth, participant authority, isolation proof, or routing decisions.

Host may reference or project these facts into Task Context. The module does not own Task requirements, Interaction Binding, provider selection, Effect recovery, participant handoff, or completion.

## Historical and private carriers

- `link-world` — deterministic network-condition research fixture;
- `link-wire` and `link-transport-quic` — reference transport experiments;
- VPN and Surfshark scripts — explicit private operator tools.

The historical crates are excluded from the default Cargo workspace. Private network mutation is outside default CI and remains manual, isolated, and recoverable.

## Local observation

```bash
cargo run -p link-probe -- --help
cargo run -p link-console -- \
  --bind 127.0.0.1:8787 \
  --database artifacts/runtime/link.db \
  --targets config/targets/web.toml \
  --interval-seconds 30
```

## Explicit isolated VPN operation

```bash
sudo scripts/install-ordivon-vpn
sudo ordivon-vpn-keypair
ordivon-vpn doctor jp-tok
sudo ordivon-vpn up jp-tok
sudo ordivon-vpn exec curl -fsS https://www.cloudflare.com/cdn-cgi/trace
sudo ordivon-vpn down
```

## Verification

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
