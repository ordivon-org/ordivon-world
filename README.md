# Ordivon World

Ordivon World is the external-interaction boundary of the Ordivon stack. It
studies and supplies the narrow semantics through which an open Task discovers,
connects to, invokes, observes, and recovers work in the external world without
reimplementing cloud providers, network stacks, Sandboxes, browsers, queues,
identity systems, or transports.

```text
Host Goal / Task / Attempt / Effect
                 │
                 ▼
       World Interaction intent
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 target and   path and     provider and
 identity     transport    capability
     └───────────┼───────────┘
                 ▼
       exact Interaction Binding
                 ▼
 mature API / Browser / Sandbox / service / Agent / device
                 ▼
 Receipt / Artifact / Observation / callback / residual evidence
                 ▼
 reconciliation, invalidation, rebinding, continued Task
```

The repository replaces the former top-level `ordivon-edge` and
`ordivon-link` prototypes. Their implementation histories are preserved in this
Git graph and their useful code is retained as internal modules.

## Why one project

A real external action cannot be cleanly split into “connect first” and “act
later.” The intended Effect determines the required endpoint, identity,
transport, locality, session, and provider. The selected path and provider can
change the observation or consequence. A timeout may mean that the path failed,
the response failed, or the remote Effect succeeded and only its acknowledgement
was lost.

The atomic research object is therefore one **World Interaction**:

```text
Task intent
→ external target and capability resolution
→ connectivity and execution binding
→ dispatch or handoff
→ remote work and data movement
→ evidence and uncertain outcome
→ reconcile, invalidate, rebind, or continue
```

## Current implementation truth

### `providers/cloudflare/`

The former Edge production plane:

- signed bounded HTTPS Fetch and Browser Run;
- private R2 Artifacts;
- authoritative pending/committed request state;
- generation fencing, deterministic Receipts, response-loss reconciliation;
- release, rollback, cleanup, policy, and operational tooling;
- a narrow local body/lifecycle research adapter.

This is a real external capability provider. It is not a universal World
resolver, general Sandbox, scheduler, proxy, or permanent Agent body.

### `modules/network-observation/`

The former Link prototype:

- route, DNS, endpoint, HTTP/TLS, QUIC, transfer, and lifetime observations;
- reduced sanitized history and a read-only local console;
- deterministic Network World and Security research fixtures;
- bounded reference wire/QUIC experiments;
- explicit private WireGuard namespace and provider-specific measurement tools.

This is an observation and research module. It is not a new network stack,
VPN, CNI, Service Mesh, automatic route controller, or production World data
plane.

## Unified responsibility

Ordivon World may eventually own only the cross-workload semantics that survive
strong-baseline and deletion tests:

- **Interaction intent** — external relation, capability, consequence,
  evidence, locality, data, and continuity needs;
- **candidate observation** — versioned facts about providers, endpoints,
  paths, identities, cost, availability, and limitations;
- **Interaction Binding** — exact Task/Attempt/Effect/Dispatch references bound
  to target, identity, path, transport, provider, execution, policy, and
  observation revisions;
- **remote uncertainty** — accepted, delivered, running, succeeded, failed, or
  unknown without blind retry;
- **conditioned provenance** — body, provider, path, identity, time, and policy
  conditions under which an Artifact or Observation was produced;
- **invalidation and reconciliation** — which conclusions and pending work
  become stale after external change;
- **rebinding and continuation** — replacement of path, provider, body,
  transport, or participant while preserving the parent Task;
- **residual closure** — what remains after sessions, bodies, callbacks, or
  external effects end.

These are research candidates, not frozen schemas or implemented universal
control-plane objects.

## Topology

World Interactions are graph-shaped, not a single local-to-cloud pipeline:

```text
local → remote       API, Browser, Sandbox, storage, Agent
remote → local       callback, webhook, stream, approval, result delivery
remote → remote      direct Artifact transfer, provider chaining
one → many           parallel research, verification, execution fan-out
many → one           Artifact join, consensus, review, aggregation
many ↔ many          multi-Agent and multi-provider work graphs
```

Ordivon should preserve why these transfers and actions occur, their authority,
identity, evidence, and outcome. It should not proxy every byte through Host.

## Ownership boundary

- **Host / semantic Kernel** owns Goal, Task, Attempt, Effect, participant
  commitments, strategy, completion, and the decision to replan.
- **Runtime** owns trusted-local Workspace, Job, process, cancellation, local
  Artifact, and recovery lifecycle.
- **World** owns external candidate facts, exact external binding, provider and
  communication correlation, remote uncertainty, conditioned evidence, and
  rebinding evidence when those responsibilities prove reusable.
- **Providers and classical infrastructure** own physical network, endpoint,
  Browser, Sandbox, VM, queue, storage, identity, and native lifecycle.
- **Security or the domain system** owns consequence authorization and final
  validity.

## Repository layout

```text
providers/cloudflare/             external Fetch/Browser/R2 provider
modules/network-observation/      network observations and research fixtures
docs/                             unified model, architecture, route, boundaries
migration/                        exact source and retirement provenance
scripts/check-repository-layout.py
```

The inherited module-local names and operational commands remain temporarily
compatible. Their presence records implementation history; it does not restore
separate Edge or Link ownership.

## Verification

```bash
python3 scripts/check-repository-layout.py

cd providers/cloudflare
corepack enable
pnpm install --frozen-lockfile
pnpm run ci

cd ../../modules/network-observation
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
```

## Active research route

The first unified experiment should prove one complete Host-to-World trajectory:

```text
Host Task
→ current path/target Observation
→ existing Cloudflare Browser or Fetch provider
→ exact request / provider execution / path conditions
→ Receipt and Artifact
→ injected response loss or Host restart
→ reconciliation through the original Interaction identity
→ Host Verification and continued Task
```

Only after that trajectory should the project derive a shared Interaction field
set, test a second provider or asynchronous participant, or add automatic
resolution. See [`docs/research-route.md`](docs/research-route.md).
