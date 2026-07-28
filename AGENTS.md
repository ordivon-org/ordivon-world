# Agent instructions

## Scope

Ordivon Edge owns distributed external presence: remote Node identity and lifecycle, profile-scoped capabilities, execution evidence, Artifacts, receipts, reconstruction, and destruction. The current repository implements the narrow Cloudflare production profile.

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
15. Future disposable Nodes must keep management, experiment, observation, and evidence-export planes distinct.
16. Broad internal range capability does not imply external authority; every remote body must bind an explicit consequence profile.
17. The evaluated Agent must not control authoritative Node lifecycle, observer state, or destruction evidence.
14. Execution bounds, retention, and expected rate limits belong in `config/edge-policy.json`; do not introduce parallel constants.
15. Artifact downloads must fail closed on missing or mismatched SHA-256 metadata and must not partially replace destinations.
16. Prefer Cloudflare REST control-plane APIs for reads, lifecycle, promotion, and rollback. Wrangler may remain only where the public API cannot express the required operation, and every such effect must be time-bounded and reconciled against API state.

## Required checks

```bash
pnpm run ci
```
