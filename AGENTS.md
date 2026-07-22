# Agent instructions

## Scope

Keep the repository thin and executable. Source, tests, Git history, target declarations, and actual probe output own their respective facts.

## Engineering rules

1. Do not add a platform layer before a real use case requires it.
2. Treat TLS, QUIC, proxy cores, and operating-system networking as replaceable data planes.
3. Keep route and network labels descriptive; do not infer a physical path that was not measured.
4. Never commit credentials, private keys, access tokens, subscription links, node addresses, or personal egress data.
5. Any deployment, route change, firewall change, or node mutation requires an explicit later phase.
6. Tests must not require public network access. Live probes are separate operational evidence.
7. Prefer narrow adapters and stable serialized observations over framework abstractions.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```
