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

## Required checks

```bash
pnpm run ci
```
