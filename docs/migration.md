# Migration from Ordivon Edge and Ordivon Link

## Decision

The former repositories were prototypes that separated connectivity from
external execution. Later analysis showed that real Task-level external work
jointly depends on relationship, identity, path, provider capability, physical
execution, evidence, and recovery. Their top-level project boundary created
artificial attachment contracts and duplicate continuity models.

They are therefore replaced by Ordivon World. After both histories, implementations, tests, documentation, and final active Issues were migrated and verified, the original GitHub repositories were deleted on 30 July 2026.

## History preservation

Both repositories were imported with Git subtree merge commits. Their original
commits remain reachable in this repository's history. Source revisions and
retirement state are also recorded in `migration/sources.json`.

## Code placement

- former `ordivon-edge` → `providers/cloudflare/`;
- former `ordivon-link` → `modules/network-observation/`.

Module-local legacy names remain temporarily for operational compatibility and
historical honesty. New top-level code and documentation must use World
Interaction terminology rather than restoring separate project ownership.

## Issue migration

The final active product Issues—former Edge #24 and Link #18—were closed as migrated to World #1. Computing #66, #67, and #68 were closed as superseded by Computing #78. The original GitHub repositories were then deleted. Their source URLs now identify historical origins rather than live repositories; exact source commits remain reachable through this repository’s imported Git graph.

## Final disposition

- `zycxfyh/ordivon-edge`: deleted 30 July 2026 after importing main revision `409a21ea3964c0c2206df7fb8dafc3fc947ab8fa`;
- `zycxfyh/ordivon-link`: deleted 30 July 2026 after importing main revision `906f6268a27d4708eb24f10cae0da444309f2c9f`;
- replacement implementation and product issue: `zycxfyh/ordivon-world` and World #1;
- active foundational research: `zycxfyh/ordivon-computing` #78.

Legacy module-local names remain where changing them would break operations or falsify historical receipts. They are compatibility surfaces, not active project identities.
