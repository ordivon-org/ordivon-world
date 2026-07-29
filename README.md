# Ordivon Edge

Ordivon Edge is the Task-to-external-execution continuity overlay of the
Ordivon stack. It lets open Tasks obtain and bind mature external execution
providers, reconcile uncertain remote outcomes, export durable Artifacts and
evidence, and continue when a browser, Sandbox, machine, region, or provider is
replaced.

Edge does **not** build a browser, Sandbox, container runtime, VM orchestrator,
scheduler, device platform, or cloud control plane. Those classical systems
remain authoritative for physical execution and native lifecycle.

```text
Host Goal / Task / Attempt / Effect
                │
                ▼
 placement requirement and exact binding
                │
                ▼
 mature external provider
 Browser / Fetch / Sandbox / VM / function / device
                │
                ▼
 provider execution identity, Receipt, Artifact, residual evidence
                │
                ▼
        Host continues the Task
```

## Current repository truth

The repository currently contains three different classes of result:

1. **Production provider** — a mature Cloudflare Worker execution plane for
   bounded external Fetch, Browser Run, private R2 Artifacts, transactional
   request state, release, rollback, and operations.
2. **Remote-effect reliability mechanisms** — stable Request IDs,
   pending/committed state, generation fencing, ambiguous-write reread, Receipt
   replay, policy/version binding, and generation-scoped cleanup.
3. **Body/lifecycle research substrate** — provider-neutral Node contracts,
   deterministic lifecycle, a narrow local `unshare` body, Security control,
   evidence export, reconstruction, and residual classification.

The third class is a research hypothesis and conformance substrate. It is no
longer described as a proven long-term Agent-native Node core. Current code does
not implement Task-level Placement Requirements, candidate comparison,
Host-level Placement Bindings, cross-provider continuation, or an automatic
provider router.

See [`docs/component-map.md`](docs/component-map.md) and
[`docs/research-route.md`](docs/research-route.md).

## Active route

```text
E0 preserve the Cloudflare production provider
→ E1 bind one real Host Effect to exact provider execution and Receipt
→ E2 derive Placement Requirement from two real workloads
→ E3 prove continuation across two external providers
→ E4 test heterogeneous multi-body branch and join
→ E5 revisit persistent Agent presence only if real workloads require it
```

The cross-project research source is
[`EDGE-CHARTER-003`](https://github.com/zycxfyh/ordivon-computing/blob/main/research/charters/EDGE-CHARTER-003.md).

## Provisional research vocabulary

- **Placement Requirement** — what one Attempt or Effect needs from an external
  execution environment.
- **Provider Capability Observation** — versioned and time-bounded facts about
  one provider's available capabilities and limits.
- **Placement Binding** — the exact relation from Task/Attempt/Effect/Dispatch
  references to one provider, body or Sandbox generation, policy, capability,
  and provider execution identity.
- **Provider Execution** — the provider-native physical execution object.
- **Artifact / Observation provenance** — durable identity and origin of results
  exported from a temporary body.
- **Semantic reconstruction** — the minimum sufficient declared inputs needed to
  continue on another body.
- **Residual evidence** — what remains after the body is retired or destroyed.

These are research candidates, not frozen public schemas.

The current code's `EdgeNodeIdentity`, lifecycle, body, and generation terms
remain valid descriptions of the existing experiment. They must not be treated
as proof that one permanent Agent Node identity is the correct long-term center.

## Strict boundary

Edge may own Task-to-external-execution placement, exact provider binding,
remote outcome reconciliation, external Artifact provenance, semantic
reconstruction, and residual closure.

Edge references but does not redefine Goal, Task, Attempt, Effect, Dispatch,
Claim, Verification, or Fact. Host and the semantic Kernel own open-work and
Effect history. Runtime owns trusted-local Workspace, Job, process, and recovery
lifecycle. Link owns Task-conditioned connectivity, path, and communication
identity. Providers own physical bodies and native lifecycle.

Forbidden expansions include:

- a self-developed container runtime, VM manager, scheduler, browser, or device
  platform;
- local route, VPN, DNS, WARP, TUN, path-selection, or transport-client code;
- automatic provider routing before two real workloads establish a stable
  requirement model;
- relabeling the current Node contract as an implemented universal Sandbox or
  permanent Agent presence.

## Cloudflare production execution plane

The production provider currently supplies:

- HMAC-SHA256 service authentication and bounded signed requests;
- one authoritative `requests/v2` state object per operation;
- queryable pending state and conditionally committed final Receipts;
- generation-scoped execution leases and stale-executor fencing;
- ambiguous-write recovery by rereading authoritative state;
- deterministic Receipt replay and generation-scoped Artifact cleanup;
- bounded HTTPS Fetch and same-origin Browser Run snapshots;
- private PNG, rendered HTML, manifest, and body Artifacts in R2;
- policy fingerprint, capability, Worker version, and lease generation binding;
- release upload, zero-traffic smoke, promotion, rollback, GC, and lifecycle
  operations.

## Research body control

```bash
corepack enable
pnpm node-control -- --root /private/edge-provider-root
```

The JSONL session exposes the narrow local conformance body for Security
experiments. It is not a production Sandbox API, scheduler, workspace manager,
or second Runtime.

## Verification

```bash
pnpm install --frozen-lockfile
pnpm run ci
```

## Local production client

```bash
scripts/install-edge-operations
ordivon-edge health
ordivon-edge status --repo /root/projects/ordivon-edge --expected-ref HEAD
ordivon-edge fetch https://developers.cloudflare.com/
ordivon-edge browser-run https://example.com/ --full-page
ordivon-edge receipt <request-id> --wait
ordivon-edge artifact-get <artifact-key> --sha256 <receipt-sha256> --output ./artifact.bin
```

## Release and lifecycle

```bash
python3 scripts/ordivon_edge_release.py release
python3 scripts/ordivon_edge_release.py rollback
scripts/configure-r2-lifecycle
python3 scripts/ordivon_edge_gc.py --dry-run
```
