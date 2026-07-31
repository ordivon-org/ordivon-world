# Research Route

## W0 — completed

W0 classified 16 inherited carrier groups as `retain`, `adapter-only`, `historical`, or `delete-candidate` and froze the first experiment without admitting an inherited Edge or Link schema.

See [`w0-carrier-inventory.md`](w0-carrier-inventory.md).

## W1 — completed; direct integration won

W1 compared:

1. B0 direct Host integration using provider-native Request ID, Receipt lookup, and Artifact verification;
2. B1 the exact same path plus one hash-chained World correlation journal.

Both arms survived a post-commit/pre-admission response loss, resumed in a fresh process, queried the original Receipt before any POST, verified the exact Artifact, and completed one Host Task exactly once. B1 added six events and 4,535 bytes while reducing no Host or provider state.

Decision:

- do not retain an independent World correlation layer;
- keep Host semantic lifecycle unchanged;
- keep provider-native reliability in provider adapters;
- bind source-native observations through Host StateRefs;
- retain W1 code and evidence as historical experiment material.

See [`w1-results.md`](w1-results.md).

## W2 — conditional and inactive

W2 activates only if a later trajectory reproduces one exact failure caused by provider capability mismatch, provider contract drift, or a valid need to rebind one still-open Effect.

When activated, compare static configuration, manual replacement through native Receipts, and the smallest explicit capability/binding decision. No marketplace, universal broker, automatic routing, or blind redispatch is authorized.

## Later work

Callbacks, participant handoff, remote-to-remote Artifact movement, fan-out/join, and programmable Sandboxes remain hypotheses. They enter the portfolio only through a real failure and a strong direct-integration baseline.

## Current portfolio disposition

The repository retains provider and observation modules plus historical experiments. The top-level World semantic layer is not active work.
