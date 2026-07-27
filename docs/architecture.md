# Architecture

## Platform shell

`src/index.ts` is the narrow Cloudflare Worker adapter. It owns HTTP routing and converts platform events into stable Edge contracts.

## Stable contracts

`src/contracts.ts` defines capabilities, operations, artifacts, and receipts without embedding Cloudflare account identifiers or resource names.

## Artifact layer

The production Worker has one private R2 binding named `ARTIFACTS`. Artifact keys are normalized, bounded, and namespaced. No public `r2.dev` access or public object route is part of this repository phase.

## Planned adapters

```text
fetch adapter
  → URL policy
  → redirect and response budgets
  → bounded body
  → R2 artifact
  → receipt

Browser Run adapter
  → action policy
  → browser-time budget
  → screenshot / extracted result
  → R2 artifact
  → receipt
```

Neither adapter may call back into local network selection. Link decides connectivity; Edge executes external capabilities.
