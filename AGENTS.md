# Agent instructions

## Scope

Ordivon Edge owns distributed external presence: Node identity and lifecycle,
profile-scoped capabilities, provider-isolated bodies, execution evidence,
Artifacts, receipts, reconstruction, and destruction.

Phase 0 contains four deliberately separate areas:

- **Agent-native core**: provider-neutral Node identity, lifecycle, lease,
  evidence, and reconstruction contracts;
- **supervisor/control**: `ResearchNodeControlSession` and its bounded JSONL
  session;
- **providers**: the operationally critical Cloudflare Worker production
  provider and the narrow local-unshare research conformance/reference
  provider;
- **ops**: the Cloudflare client, release, GC, and lifecycle scripts.

The Cloudflare production provider remains the mature production execution
plane. It is not the whole repository, and the local-unshare provider is not a
second production plane. See `docs/component-map.md`.

## Frozen vocabulary and ownership

- A **Node** is the long-lived semantic identity of an Agent presence.
- A **Sandbox** is one isolated instance of a Node on a Provider, including
  that instance's generation.
- An **Execution** is one bounded action inside a Sandbox.
- The current code has no independent `Sandbox` type. Its Node identity input,
  local provider body, lifecycle record, and generations encode parts of that
  model. Do not document or design around a fictitious implemented Sandbox
  abstraction.
- Edge owns body/Sandbox semantics and authoritative Node lifecycle. Ordivon
  Runtime owns trusted supervisor/process supervision plus its own Task,
  workspace, and recovery lifecycle.
- Ordivon Link may consume a future generation-bound attachment handle. It does
  not own or advance Node or Sandbox lifecycle. Phase 0 does not implement that
  handle.

## Phase 0 exclusions

The local-unshare provider is frozen as a narrow conformance/reference provider
for the research profile. Do not grow it into a home-built container Runtime.
OCI/runc-backed providers are future direction only and are not implemented or
authorized by Phase 0.

Do not build a container runtime, VM orchestrator, network stack, scheduler, or
workspace runtime in this repository. Future providers may adapt established
external isolation systems while keeping Edge contracts and authority
boundaries intact.

## Rules

1. Do not add local route, VPN, DNS, WARP, TUN, path-selection, or transport-client code.
2. Do not reimplement Ordivon Runtime task, process, workspace, or recovery lifecycle.
3. Every executable capability needs authentication, authorization, budgets, and a receipt.
4. External fetch must reject unsupported schemes, unsafe ports, private/link-local destinations, unbounded redirects, and unbounded bodies.
5. Browser Run must have explicit time, action, and artifact budgets.
6. R2 remains private by default; do not enable `r2.dev` or a public object route without review.
7. Never expose account IDs, bucket names, tokens, cookies, private URLs, or raw external response bodies in status APIs or logs.
8. Keep platform adapters thin and stable contracts independently testable.
9. `pnpm check:boundary` must continue to reject Link/network code.
10. New execution outputs must be generation-scoped and committed through the authoritative request state.
11. Never serialize lease tokens or R2 ETags into Receipts, logs, manifests, or client responses.
12. Production release must use `scripts/ordivon_edge_release.py`; do not deploy directly from a feature branch.
13. Cleanup tasks may delete only matching-generation `fetch/v2` or `browser/v2` Artifacts.
14. Production, research, and adversarial-range profiles must have separate credentials, authority, and lifecycle policy.
15. Disposable Provider bodies and future Sandbox instances must keep management, experiment, observation, and evidence-export planes distinct.
16. Broad internal range capability does not imply external authority; every remote body must bind an explicit consequence profile.
17. The evaluated Agent must not control authoritative Node lifecycle, observer state, or destruction evidence.
18. Execution bounds, retention, and expected rate limits belong in `config/edge-policy.json`; do not introduce parallel constants.
19. Artifact downloads must fail closed on missing or mismatched SHA-256 metadata and must not partially replace destinations.
20. Prefer Cloudflare REST control-plane APIs for reads, lifecycle, promotion, and rollback. Wrangler may remain only where the public API cannot express the required operation, and every such effect must be time-bounded and reconciled against API state.
21. Keep local-unshare limited to its research conformance/reference role; do not add generic image management, package installation, writable workspace, daemon supervision, or multi-tenant scheduling.
22. Do not add a Sandbox type by relabeling the current Node or local body. A future Sandbox contract must model provider instance identity and generation explicitly.
23. Link integration may use only an explicit generation-bound attachment handle and must not transfer lifecycle authority out of Edge.
24. Do not implement a container runtime, VM orchestrator, network stack, scheduler, or workspace runtime.

## Required checks

```bash
pnpm run ci
```
