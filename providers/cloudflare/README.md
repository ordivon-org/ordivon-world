# Cloudflare Provider for Ordivon World

This module is Ordivon World's production Cloudflare provider adapter. The `ordivon-edge` Worker, CLI, service, and receipt names are retained for operational compatibility, not as a separate top-level architecture.

## Active capability

- authenticated, bounded HTTPS Fetch;
- bounded same-origin Browser snapshots;
- private R2 body, screenshot, HTML, and manifest Artifacts;
- authoritative pending/committed request state;
- stable Request IDs, semantic request digests, lease generations, and stale-executor fencing;
- Receipt lookup and deterministic replay after response loss;
- policy/capability/Worker-version binding;
- release, zero-traffic smoke, promotion, rollback, retention, and cleanup.

The current deployment is a single trusted-principal service. It does not implement participant IAM, a provider marketplace, generic placement, automatic routing, a Sandbox platform, or Host Task lifecycle.

## Ownership

Provider-native request, execution, Receipt, Artifact, policy, and release facts remain authoritative here. Host owns Task/Effect meaning, UNKNOWN, reconciliation frontier, independent Verification, Artifact acceptance, and completion. World introduces no duplicate database or universal interaction ID.

## Contract boundaries

Fetch and Browser schemas reject unknown fields. Fetch targets use exact-host HTTPS allowlists; wildcard hosts are not accepted. Redirect targets are revalidated before another request. Browser snapshot Receipts preserve the requested URL and report `final_url_observed: false` because the provider response does not currently expose trustworthy final navigation identity. Consumers must not infer it.

## Historical research

Provider-neutral Node contracts, local `unshare` bodies, lifecycle controls, and Security composition are retained as historical experiments. They are not in the production Worker bundle or default CI and do not establish a general Sandbox or durable Agent body.

## Local client

```bash
scripts/install-edge-operations
ordivon-edge health
ordivon-edge status --repo /root/projects/ordivon-world --expected-ref HEAD
ordivon-edge fetch https://developers.cloudflare.com/
ordivon-edge browser-run https://example.com/ --full-page
ordivon-edge receipt <request-id> --wait
ordivon-edge artifact-get <artifact-key> --sha256 <receipt-sha256> --output ./artifact.bin
```

Installed release and GC tools resolve `/root/projects/ordivon-world/providers/cloudflare` by default. Set `ORDIVON_WORLD_REPO` when the checkout lives elsewhere. New release receipts are written under `/root/backups/ordivon-world/`.

## Release and lifecycle

```bash
python3 scripts/ordivon_edge_release.py release
python3 scripts/ordivon_edge_release.py rollback
scripts/configure-r2-lifecycle
python3 scripts/ordivon_edge_gc.py --dry-run
```

## Verification

```bash
pnpm install --frozen-lockfile
pnpm run ci
```
