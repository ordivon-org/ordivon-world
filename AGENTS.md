# Agent instructions

## Scope

Ordivon Edge owns externally hosted bounded execution, R2 artifacts, Browser Run, fetch policy, receipts, and optional remote-node lifecycle.

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

## Required checks

```bash
pnpm run ci
```
