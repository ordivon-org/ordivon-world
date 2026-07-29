# Agent instructions

## Mission

Ordivon World is the Task-to-external-world interaction boundary. It unifies the
former Edge and Link research objects because real remote work jointly depends
on target, identity, path, transport, provider capability, execution, evidence,
and recovery.

The repository does not create a new network stack, proxy, VPN, CNI, service
mesh, browser, Sandbox, scheduler, workflow engine, identity platform, or cloud
control plane. Reuse mature mechanisms and add only proven Task-level semantics
above them.

## Current slices

- `providers/cloudflare/` is a production external capability provider imported
  from `ordivon-edge`.
- `modules/network-observation/` is an observation/research module imported from
  `ordivon-link`.
- Historical Node, Network World, wire, VPN, and command names are compatibility
  and evidence surfaces, not top-level architecture.

## Candidate unified vocabulary

Use these terms only as research vocabulary until real workloads prove them:

- World Interaction intent;
- target/capability/path/identity candidate observation;
- Interaction Binding;
- provider execution and communication delivery identity;
- conditioned Artifact/Observation provenance;
- invalidation, reconciliation, rebinding, and residual closure.

Do not introduce a universal schema, global World ID, or automatic resolver from
documentation alone.

## Ownership

1. Host owns Goal, Task, Attempt, Effect, participant responsibility, strategy,
   and completion.
2. Runtime owns trusted-local execution and process lifecycle.
3. World may own exact external binding, remote uncertainty, conditioned
   evidence, and rebinding correlation when those semantics are proven reusable.
4. Providers and classical infrastructure own native endpoints, routes,
   identities, sessions, bodies, storage, queues, and lifecycle.
5. Security/domain systems own consequence authority and final validity.

## Engineering constraints

1. Preserve the Cloudflare provider's production reliability and release
   boundary.
2. Preserve secret-free network observation and explicit private-operation
   boundaries.
3. Do not centralize remote-to-remote data flow through Host or World merely for
   observability; preserve references, digests, authority, and Receipts instead.
4. Reconcile uncertain external work before retry or participant/provider
   replacement.
5. Path, region, endpoint, identity, provider, capability, policy, and time may
   condition evidence; never silently generalize one observation.
6. Do not automate route, DNS, VPN, firewall, provider, or participant changes
   before the requirement and invalidation model is proved.
7. Do not expand the inherited local body or Network World experiments into a
   production Sandbox or data plane.
8. Do not preserve Edge/Link project boundaries through artificial internal
   protocols. Use ordinary modules until an external consumer proves a stable
   contract.
9. Keep migration provenance exact. Never rewrite historical evidence to pretend
   the unified model existed earlier.
10. Every new abstraction needs a strong classical baseline, two materially
    different workloads, an observed failure when deleted, and a cost comparison.

## Required checks

```bash
python3 scripts/check-repository-layout.py
cd providers/cloudflare && pnpm run ci
cd modules/network-observation && cargo fmt --all -- --check
cd modules/network-observation && cargo clippy --workspace --all-targets -- -D warnings
cd modules/network-observation && cargo test --workspace --all-targets
```
