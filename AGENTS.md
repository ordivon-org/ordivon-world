# Agent instructions

## Mission

Ordivon World carries real external-provider and network-observation modules and runs bounded experiments about Task-to-world continuity. W1 proved that the current Fetch response-loss path does not require an independent World correlation layer.

Do not describe this repository as a mandatory production layer. The current retained composition is Host plus provider and observation adapters.

## Current slices

- `providers/cloudflare/` is a production external capability provider imported from `ordivon-edge`.
- `modules/network-observation/` is a source-native observation and private-operations module imported from `ordivon-link`.
- `experiments/` contains deletion-tested research implementations, not reusable production APIs by default.
- historical Node, Network World, wire, VPN, and command names are compatibility and evidence surfaces, not top-level architecture.

## W1 ownership result

1. Host owns Goal, Task, Attempt, Effect, Dispatch, UNKNOWN, recovery frontier, Verification, and completion.
2. Runtime owns trusted-local execution and process lifecycle.
3. Provider adapters own native endpoint, request digest, idempotency, Receipt, Artifact, policy, capability, and provider-version semantics.
4. Observation adapters own source-native observations and expose only bounded projections or references to Host.
5. World-specific correlation state has no production owner unless a later experiment reproduces a failure that these boundaries cannot explain.
6. Security/domain systems own consequence authority and final validity.

## Engineering constraints

1. Preserve the Cloudflare provider's production reliability and release boundary.
2. Preserve secret-free network observation and explicit private-operation boundaries.
3. Reconcile uncertain external work by its original provider identity before retry.
4. Never replace provider-native request or Receipt semantics with a generic digest or state machine.
5. Never copy Host Task truth, provider request truth, or raw observation truth into a synchronized World database.
6. Path, region, endpoint, identity, provider, capability, policy, and time may condition evidence; bind exact revisions where used.
7. Do not automate route, DNS, VPN, firewall, provider, or participant changes before a concrete requirement and invalidation failure exists.
8. Do not expand inherited Node or Network World fixtures into a production Sandbox or data plane.
9. Keep migration provenance and invalid experiments exact; do not rewrite evidence to make a failed Trial valid.
10. Every new abstraction needs a strong baseline, an observed failure when deleted, explicit ownership, measured net benefit, and a closeout disposition.

## W2 activation gate

W2 remains conditional. Activate it only after reproducing one exact failure caused by provider capability mismatch, provider contract drift, or a legitimate need to rebind one still-open semantic Effect.

A provider marketplace, universal broker, automatic routing, or blind redispatch is never implied by activation.

## Required checks

```bash
python3 scripts/check-repository-layout.py
python3 scripts/check-w1-evidence.py
cd experiments/w1-host-cloudflare && uv sync --frozen && uv run python -m unittest discover -s tests -v
cd providers/cloudflare && pnpm run ci
cd modules/network-observation && cargo fmt --all -- --check
cd modules/network-observation && cargo clippy --workspace --all-targets -- -D warnings
cd modules/network-observation && cargo test --workspace --all-targets
```
