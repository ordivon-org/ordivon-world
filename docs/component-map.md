# Phase 0 component map

This map classifies the current repository by responsibility and authority. It
is descriptive of Phase 0; it does not claim an independent Sandbox
implementation.

## Frozen terms

- **Node** — the long-lived semantic identity of an Agent presence.
- **Sandbox** — one isolated instance of a Node on a Provider, including that
  instance's generation.
- **Execution** — one bounded action inside a Sandbox.

There is no standalone `Sandbox` type in the current code. In particular,
`EdgeNodeIdentity`, `LocalDisposableNodeAdapter`, a provider body, or a lease
generation must not be renamed or described as though any one of them were the
complete Sandbox abstraction.

## Components

| Classification | Key files | Authority | Phase 0 disposition |
| --- | --- | --- | --- |
| Agent-native core | `src/node-contracts.ts`, `src/node-lifecycle.ts` | Edge defines Node identity, lifecycle, lease, observation/evidence, and reconstruction semantics. Lifecycle authority stays with trusted Edge management, never the evaluated Agent, Security, Runtime, or Link. | Implemented provider-neutral contracts and deterministic lifecycle; keep stable. The current generation fields do not amount to an independent Sandbox model. |
| Supervisor/control | `src/research-node-control.ts`, `scripts/ordivon_edge_node_control.ts` | A trusted research management process owns one session/root and keeps lease tokens in memory. Runtime may supervise this trusted process but does not acquire Edge lifecycle authority. | Keep as the bounded `ResearchNodeControlSession` plus JSONL session. It is not a production API, scheduler, workspace manager, or general Sandbox service. |
| Provider: Cloudflare Worker production | `src/index.ts`, `src/auth.ts`, `src/contracts.ts`, `src/external-fetch.ts`, `src/browser-run.ts`, `src/idempotency.ts`, `src/execution.ts`, `src/receipts.ts`, `src/artifacts.ts`, `src/cleanup.ts`, `src/policy.ts`, `config/edge-policy.json`, `wrangler.jsonc` | Profile-scoped signed callers authorize bounded executions; Cloudflare bindings realize execution and private Artifact effects; production operators control release and rollback. | Mature, operationally critical production provider; retain and harden. It is one Provider profile, not the whole Edge boundary. |
| Provider: local-unshare research/conformance | `src/local-node-adapter.ts`, `src/node-policy.ts`, `config/edge-node-policy.json` | Only the trusted, credential-free research authority may drive the adapter. The evaluated action has no management, observation, evidence-export, production, or Link authority. | Implemented narrow conformance/reference provider for lifecycle, lease fencing, evidence, reconstruction, and isolation checks. Scope is frozen: no generic images, package management, writable workspaces, daemon supervision, multi-tenancy, or scheduling. |
| Ops: Cloudflare capability client | `scripts/ordivon_edge_client.py`, `scripts/install-edge-client`, `scripts/install-edge-operations`, `scripts/check-operations` | The configured service identity signs bounded data-plane requests; it has no Provider lifecycle authority. | Retain as the production operations client and contract check. |
| Ops: release, GC, and R2 lifecycle | `scripts/ordivon_edge_release.py`, `scripts/ordivon_edge_gc.py`, `scripts/configure_r2_lifecycle.py`, `scripts/configure-r2-lifecycle`, `deploy/systemd/ordivon-edge-gc.service`, `deploy/systemd/ordivon-edge-gc.timer` | Explicit production operator credentials authorize Cloudflare control-plane effects. Release authority remains in `ordivon_edge_release.py`; GC may delete only policy-approved matching-generation Artifacts. | Retain as Cloudflare production operations. These scripts do not define Agent-native lifecycle semantics. |
| Boundary and conformance checks | `scripts/check-boundary.mjs`, `scripts/check-node-policy.mjs`, `test/node-lifecycle.test.ts`, `test/research-node-control.test.ts`, `test/worker.test.ts`, `test/transactions.test.ts` | CI verifies contracts and repository boundaries; tests hold no runtime authority. | Keep independently testable and continue rejecting Link/network code and authority drift. |

The table lists key files rather than every helper. Files imported only by the
Cloudflare Worker inherit the Cloudflare production provider classification;
provider-neutral Node files do not inherit Cloudflare authority.

## Ownership boundary

- Edge owns Body/Sandbox semantics, Node lifecycle, lease fencing, evidence,
  reconstruction, and destruction.
- Runtime supervises trusted supervisor/control processes and owns its own Task,
  process, workspace, and recovery lifecycle. Starting or monitoring a trusted
  Edge process does not transfer Node or Sandbox authority to Runtime.
- Link may in the future consume an explicit, generation-bound attachment
  handle to provide approved connectivity. It neither creates nor destroys a
  Sandbox and cannot advance, restore, or retire its lifecycle. No such handle
  is implemented in Phase 0.
- The evaluated Agent may perform an authorized Execution but cannot control
  authoritative lifecycle, observer state, or destruction evidence.

## Explicit non-goals

Phase 0 does not build a container runtime, VM orchestrator, network stack,
scheduler, or workspace runtime. The local-unshare provider must remain a
narrow conformance/reference implementation, not expand into any of those
systems.

OCI/runc-backed isolation is future Provider direction only. There is no
OCI unpacker, runc integration, or general container Provider in the current
implementation, and this direction does not authorize adding one in Phase 0.
