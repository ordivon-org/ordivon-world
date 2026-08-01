# Agent instructions

## Scope

This directory is the production Cloudflare provider adapter carried by Ordivon World. Legacy `ordivon-edge` command and service names remain for operational compatibility; they do not restore an independent Edge architecture.

The active surface is bounded Fetch, Browser snapshot, private R2 Artifacts, provider request state, Receipts, reconciliation, release, rollback, retention, and cleanup. Historical Node/body/lifecycle research remains source evidence outside default CI.

## Owned facts

The provider owns only provider-native facts: signed request body and identity, semantic request digest, execution lease generation, policy and capability revision, Worker version, pending/committed state, Receipt, Artifact key and metadata, ambiguous-commit reread, and generation-scoped cleanup.

Host owns Task/Effect meaning, UNKNOWN, Verification, Artifact acceptance, replanning, and completion. Runtime owns trusted-local execution. Observation modules own source-native path facts. Security/domain systems own consequence authority.

## Rules

1. Preserve HMAC authentication, exact request identity, CAS admission/commit, stale-executor fencing, and reconcile-before-retry.
2. Fetch and Browser input schemas fail closed on unknown fields and bounded policy violations.
3. External URLs are HTTPS-only, exact-host allowlisted, credential-free, standard-port, and revalidated after redirects.
4. Browser Receipts must distinguish requested URL from observed final URL; never invent navigation evidence the provider does not expose.
5. R2 remains private. Artifact reads verify key scope and digest and return attachment/no-store headers.
6. New output is generation-scoped and committed only through authoritative request state.
7. Production release identity binds the World Git commit and exact `providers/cloudflare` release inputs.
8. Installed release/GC tools resolve the World repository through `ORDIVON_WORLD_REPO` or `/root/projects/ordivon-world`.
9. Do not add routing, VPN, DNS, generic Sandbox, VM, scheduler, browser implementation, provider marketplace, or Task lifecycle.
10. Historical Node research may be run explicitly, but must not silently re-enter the production bundle or default CI.

## Required check

```bash
pnpm run ci
```
