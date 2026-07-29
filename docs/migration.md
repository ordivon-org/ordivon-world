# Migration from Ordivon Edge and Ordivon Link

## Decision

The former repositories were prototypes that separated connectivity from
external execution. Later analysis showed that real Task-level external work
jointly depends on relationship, identity, path, provider capability, physical
execution, evidence, and recovery. Their top-level project boundary created
artificial attachment contracts and duplicate continuity models.

They are therefore replaced by Ordivon World.

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

The final active product Issues from the old repositories are replaced by one
unified first-interaction Issue in this repository. The old Issues are closed
with migration references before the old repositories are retired.
