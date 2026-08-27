---
schema_version: 1
id: world.start
title: Ordivon World
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - builder
  - operator
  - agent
updated: 2026-08-12
summary: Public entry to owner-preserving external observation, recoverable effects, cross-World transfers, temporal provenance, and reconciliation without a global World authority.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.authority
  - world.boundaries
---
# Ordivon World

An Agent sends a request to an external provider. The provider may have committed the effect, but the response disappears before the caller receives it.

What is true now?

- the caller intended one external operation;
- Host may have retained one durable Effect/Dispatch identity;
- World may know the exact provider request identity and the condition under which it was admitted;
- the provider may or may not have committed the operation;
- a local process result cannot answer that provider-owned question;
- issuing a fresh request merely because the response was lost may duplicate the consequence.

**Ordivon World is the narrow boundary that connects Ordivon work to independently authoritative environments without pretending to own those environments.** It binds exact external identities, preserves the evidence needed to reconcile uncertain effects, and carries selected Resource, Message, and Entity trajectories between owners while leaving native truth with those owners.

```text
Host work / domain intent
        ↓
World binds one owner-native external operation
        ↓
provider or destination owner
        ↓
Receipt / native observation / Artifact
        ↓
World maps exact evidence and uncertainty
        ↓
Host/domain verification decides what the result means
```

World is not a daemon, workflow engine, provider broker, global capability registry, network control plane, universal connector platform, Sandbox, Task database, or completion authority.

## Who owns what

| Responsibility | Owner |
| --- | --- |
| Task, Effect, Dispatch, revision fencing, Task-level UNKNOWN, Verification and completion | Host |
| local Workspace/Job/Attempt/process execution | Runtime |
| bounded Agent Run and Provider/Tool cognition | Harness |
| provider-native request state, occurrence, Receipt, remote Artifact and current provider capability | provider |
| source-domain egress/issuance/departure fact | source domain |
| destination-domain ingress/materialization/current state | destination domain |
| exact cross-owner binding, trajectory identity, retained uncertainty, reconciliation and evidence mapping | World |

World may persist or project an owner's evidence. That does not transfer semantic or factual ownership to World.

## One recoverable external effect

The direct provider path is deliberately small:

```text
observe current provider capability
→ bind exact request + condition digest
→ derive deterministic provider request identity
→ persist PreparedWorldDispatch before delivery
→ deliver once
→ Receipt | UNKNOWN
→ if UNKNOWN, query the original provider request
→ map exact provider evidence
→ Host/domain verifies the consequence
```

If the provider response is lost after commitment, World keeps `UNKNOWN` until the original request is reconciled. A missing Receipt is not proof that nothing happened. A new controller, process, machine, or Runtime Workspace does not create authority to redispatch an old consequence under a new identity.

## Three cross-World trajectories

World also carries three production trajectory families. They share a recovery skeleton but intentionally keep different domain meanings.

### Resource Transfer

```text
source owner proves egress
→ World binds transferId + payload/provenance
→ destination independently admits/materializes
→ receipt or UNKNOWN
→ reconcile the exact transfer
```

The first production path is Station Zero Game → Security SampleVault. Source truth remains Game-owned; destination materialization remains Security-owned.

### Message Delivery

```text
source owner proves issuance
→ World binds messageId + exact payload/provenance
→ destination independently admits delivery
→ receipt or UNKNOWN
→ reconcile the exact message
```

**Delivery does not mean knowledge.** A destination inbox can prove that a Message was admitted without proving that an Agent read it, believed it, understood it, or promoted it into world truth.

### Entity Migration

```text
source owner proves departure
→ World binds migrationId + opaque continuity
→ destination binds/materializes the carrier
→ native evidence proves or leaves uncertainty
→ reconcile without rewriting predecessor history
```

A historical migration receipt proves a historical trajectory. It does not prove that the Entity is currently present at the destination. Current Presence remains owner- and scope-bound.

## Current release boundary

The current package line is `0.6.0`. Its retained production boundary includes:

- Host-facing Cloudflare Fetch and Browser Snapshot binding/reconciliation;
- exact Browser bundle integrity across screenshot, rendered HTML and Manifest;
- provider-native `started_at` / `completed_at` plus World-owned observation `availableAt` without merging their clocks or meanings;
- Resource Transfer, Message Delivery, and Entity Migration contracts with durable Host-backed trajectory state;
- per-trajectory addressing where real multi-trajectory failures justified it;
- `WorldTaskInspector`, a bounded read-only projection over retained World commitments that grants neither action authority nor external currentness;
- owner-native World doctor aggregation;
- Workstation-projected local network capabilities when an external World operation needs them; local Surfshark/WireGuard provider, key-materialization, namespace, route, discovery, and recovery mechanics remain Workstation-owned rather than a second World actuator.

The Cloudflare Worker/operations subtree is co-located but provider-owned and independently extractable. World can pass its Python/wheel boundary with that subtree absent; the provider can pass its own CI independently.

Detailed current capability state and known limits live in [`STATUS.md`](STATUS.md).

## Seven boundaries that prevent wrong external claims

### Provider success is not Task completion

A provider Receipt can prove a provider-native occurrence. Host/domain verification still decides whether that occurrence satisfies the Task or product objective.

### Historical occurrence is not current Presence

Yesterday's observed resource, path, Entity, or provider state remains historical evidence. A current decision that depends on present state must re-observe or reconcile through the owner that can establish currentness.

### Delivery is not cognition

Message transport occurrence does not prove destination knowledge, understanding, acceptance, or belief.

### Reconciliation precedes redispatch

Response loss creates uncertainty, not permission to issue a new effect. Query the original request/trajectory identity first.

### Observation time sources stay separate

Provider execution time, World observation availability, and Host admission time describe different events under different owners. `availableAt` is not occurrence time, freshness, currentness, action authority, or completion.

### Structural receipts do not create trust

A receipt can preserve exact identity and provenance without authenticating an untrusted relay. Current Resource/Message/Entity production integrations state their trust profile explicitly instead of claiming a universal PKI.

### Task identity is not trajectory identity

A Host Task may contain multiple provider/resource/message trajectories. Their native identities (`dispatchId`, `transferId`, `messageId`, `migrationId`) remain separate so one uncertain trajectory does not silently redefine another.

## What World deliberately does not persist

Not every observation or Agent choice deserves durable World state.

Before owner admission, discovery, capability observation, path comparison, and Agent selection are normally recomputable planning state. If the controller disappears, observe current owner reality again and let the Agent choose again.

```text
Observe → Query → Select       recomputable
                 │
                 ▼
      owner admits exact consequence
                 │
          durability fence
                 ▼
Prepared / Bound / Dispatched
                 │
          Receipt | UNKNOWN
                 │
              Reconcile
```

This is why World does not have a generic CapabilityManager, selection journal, Presence database, relationship manager, or universal commitment registry.

## Research that was deliberately not promoted

World's research corpus is much larger than the current product. Closed W4/W5/Sense–Connect–Act and W-X/HP studies established useful laws about path evidence, Presence, discovery, connection, interaction, temporal provenance, execution mobility, and deletion pressure. Several plausible shared APIs were removed after they failed to improve fresh-Agent decisions or could remain owner-local.

Those results remain reproducible evidence under [`docs/research-closeouts.md`](docs/research-closeouts.md), [`docs/high-pressure-survival-hp6-hp8.md`](docs/high-pressure-survival-hp6-hp8.md), and `docs/archive/research/`. Their phase numbering is not required to understand or use the current product.

A new shared World abstraction requires a named current workload, a reproduced failure, and evidence that direct Host + owner/provider composition cannot hold the residual responsibility cleanly.

## Start according to your job

| Need | Read |
| --- | --- |
| understand why World exists and where truth stays | this README |
| inspect current release capability and limits | [`STATUS.md`](STATUS.md) |
| understand exact ownership and execution flow | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| inspect which source owns each current fact | [`docs/authority.md`](docs/authority.md) |
| inspect request/trajectory identities and JSON contracts | [`docs/contracts.md`](docs/contracts.md) |
| operate, deploy, diagnose, GC or recover | [`docs/operations.md`](docs/operations.md) |
| determine what evidence actually proves | [`docs/verification.md`](docs/verification.md) |
| turn broad resource discovery into bounded owner/transport verification and consumption | [`docs/resource-opportunity-flywheel.md`](docs/resource-opportunity-flywheel.md) |
| understand how resources become options, redundancy and capability without a global registry | [`docs/resource-option-capability-model.md`](docs/resource-option-capability-model.md) |
| reason about Actor capability, environment exposure, institutional rules, selection and causal attribution without a global context ontology | [`docs/capability-context-doctrine.md`](docs/capability-context-doctrine.md) |
| understand why the retained boundary is narrow | [`docs/retained-boundaries.md`](docs/retained-boundaries.md) |
| navigate the World / Reality research owner, Foundations, deep history, coverage and provenance | [`docs/research/world/README.md`](docs/research/world/README.md) |
| inspect closed operational research and reopening conditions | [`docs/research-closeouts.md`](docs/research-closeouts.md) |

## Development

```bash
scripts/owner-environment bootstrap
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
scripts/local-acceptance
```

Repository-only health:

```bash
uv run ordivon-world-doctor --repo . --offline
```

Live machine/provider health must be queried from the owning systems. See [`docs/operations.md`](docs/operations.md).

## Security and data

World crosses external authority boundaries. External actions therefore require exact identity, current condition binding, explicit trust assumptions, durable uncertainty, and owner-native evidence. Telemetry correlation is not evidence. A route being reachable is not permission to use it. A successful transport is not semantic acceptance.

Read [`SECURITY.md`](SECURITY.md) and [`docs/data-and-privacy.md`](docs/data-and-privacy.md) before exposing adapters or transporting sensitive material.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
