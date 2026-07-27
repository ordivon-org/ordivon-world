# Agent instructions

## Scope

Keep the repository thin and executable. Source, tests, Git history, target declarations, and actual probe output own their respective facts.

## Engineering rules

1. Do not add a platform layer before a real use case requires it.
2. Treat TLS, QUIC, proxy cores, and operating-system networking as replaceable data planes.
3. Keep route and network labels descriptive; do not infer a physical path that was not measured.
4. Never commit credentials, private keys, access tokens, subscription links, node addresses, or personal egress data.
5. The Web API, SQLite store, logs, events, and rendered UI must not expose or retain public/private IPs, usernames, hostnames, MAC addresses, local addresses, account paths, target URLs, or raw command/probe output.
6. Keep the Web listener loopback-only by default. Any non-loopback or Cloudflare exposure requires a separate authenticated design review.
7. Any deployment, route change, firewall change, provider action, or node mutation requires an explicit later phase.
8. Tests must not require public network access. Live probes are separate operational evidence.
9. Target IDs are public labels, not a place for IPs, usernames, hostnames, account identifiers, or private route names.
10. Raw Host and request-target validation must remain outside the Axum Router so path normalization cannot bypass it.
11. Child-process output must be suppressed or bounded, and timeouts must terminate the child rather than only dropping the wait future.
12. Prefer narrow adapters and stable serialized observations over framework abstractions.
13. A reachable service does not prove that the intended VPN path is active; provider and route state must be verified independently.

## Required checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```
