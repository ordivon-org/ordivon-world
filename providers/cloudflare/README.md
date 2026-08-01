# Cloudflare Provider for Ordivon World

This module is Ordivon World's production Cloudflare provider adapter. The `ordivon-edge` Worker, CLI, service, and receipt names are retained for operational compatibility, not as a separate top-level architecture.

## Active capability

- authenticated, bounded HTTPS Fetch;
- bounded same-origin Browser snapshots;
- private R2 body, screenshot, HTML, and manifest Artifacts;
- authoritative pending/committed request state;
- stable Request IDs, semantic request digests, lease generations, and stale-executor fencing;
- Receipt lookup and deterministic replay after response loss;
- durable `evidence.run.v1` Workflows with provider-native instance handles, inspect, termination, and immutable R2 manifests;
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
ordivon-edge evidence-run ./evidence-run.json --request-id req_<stable-id>
ordivon-edge evidence-status evidence-req_<stable-id> --wait
ordivon-edge evidence-terminate evidence-req_<stable-id>
ordivon-world-evidence capture-source https://developers.cloudflare.com/workflows/ --output ./source-evidence.json
ordivon-world-evidence accept-provider --output ./provider-acceptance.json
```

An evidence run contains one to eight bounded `fetch` or `browser.run` steps. Cloudflare Workflows owns durable step execution and the instance lifecycle; R2 owns input, result, failure, and source Artifacts; Host or the consumer owns why the run exists, independent Verification, and completion.

Installed release and GC tools resolve `/root/projects/ordivon-world/providers/cloudflare` by default. Set `ORDIVON_WORLD_REPO` when the checkout lives elsewhere. The evidence consumer imports the shared client from `/usr/local/lib/ordivon-world/ordivon_edge_client.py`; the protocol implementation is not copied into a second package. New release receipts are written under `/root/backups/ordivon-world/`.

## Release and lifecycle

The release controller uploads the candidate Worker at zero traffic, validates or bootstraps the `ordivon-evidence-run` Workflow resource, runs Fetch, Browser, and durable `evidence.run` candidate smokes, verifies the Workflow step's Worker version, and only then promotes the candidate. Existing Workflow resources are validated by script and class and are not rewritten on every release.

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
