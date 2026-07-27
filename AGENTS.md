# Agent instructions

## Scope

Ordivon Link owns local network observation, evidence, selection inputs, replaceable transports, and recovery policy. Keep Cloudflare execution and Agent process execution outside this repository.

## Engineering rules

1. Keep `link-model ← link-probe ← link-observer ← link-console` acyclic.
2. Keep `link-wire ← link-transport-quic` independent from the observation slice.
3. Do not add Cloudflare Workers, Browser Rendering, R2, Queue, or external fetch implementation here.
4. Do not add Ordivon Runtime workspace, task, process, or artifact lifecycle here.
5. Route and network labels describe controlled facts only.
6. Never commit credentials, private keys, tokens, subscription links, node addresses, or personal egress evidence.
7. Persist only sanitized reduced observations; raw command and probe output stays bounded and ephemeral.
8. The console remains loopback-only and read-only unless a separate authenticated boundary is approved.
9. Tests must not require public network access or mutate host networking.
10. Use maintained TLS, QUIC, and proxy implementations; do not create cryptographic primitives.
11. Explicit VPN mutation must be isolated to a dedicated namespace, remain root-only, preserve the WSL root default route, and roll back transactionally.
12. CI may syntax-check the VPN controller but must never create namespaces, interfaces, routes, firewall rules, or public probes.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```
