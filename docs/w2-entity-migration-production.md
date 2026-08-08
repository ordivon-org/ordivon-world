---
schema_version: 1
id: world.w2-entity-migration
title: W2 Production Entity Migration
type: decision
profile: engineering
lifecycle: active
source_role: supporting
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
evidence_status: cross-repository-verified
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.authority
  - world.boundaries
  - world.w2-resource-transfer
  - world.w2-message-delivery
---
# W2 Production Entity Migration

## Purpose

W2 promotes Entity Migration only after a real Game departure, Host durable recovery and a Security-owned Windows KVM destination exercised both sides of the uncertainty boundary.

```text
Game / source World
  verified local Presence departure
        ↓
EntityDepartureReceipt
        ↓
World / Host
  exact migration commitment + opaque continuity
        ↓
Security / destination World
  durable pre-body KVM fence
        ↓
Windows KVM continuity carrier
        ↓
EntityMigrationReceipt
```

The promoted contract preserves Entity continuity across World-local materializations. It does not claim that a Guest has consumed the Agent's cognition, that destination Presence remains live forever, or that World owns a global Presence database.

## Identity, cognition, Presence and body remain separate

The production trajectory keeps the W0 distinction:

```text
Entity identity
!= cognition / memory state
!= World-local Presence
!= execution body
```

Game owns only the departure of its local Presence. It does not own or sign the Agent's portable cognition. The continuity payload therefore remains opaque to the source and destination boundary contract.

Security materializes a KVM body carrier. The current Guest Runner does not interpret the migration continuity payload and is not used as migration authority.

## Source departure authority

Station Zero `extract` provides the first native source authority. A departure is accepted only when retained Game evidence binds:

- an `actor_life_state_changed` Fact ending in `extracted`;
- the exact retained `extract` Intent;
- an executed `actor_extracted` resolution;
- `verificationPassed=true`;
- retained post-turn actor life state `extracted`.

Game then commits an `EntityDepartureReceipt`.

One departure occurrence may authorize at most one `migrationId`:

```text
one verified departure occurrence
→ one migration identity
```

Attempting to authorize a second migration from the same departure is rejected. This is the source-side fork fence.

The historical Game Actor object is not deleted. Its old position may remain in retained state. Therefore:

```text
source Presence departure
!= deletion of source history
```

## Limbo is a trajectory fact, not a global Presence fact

Before the first destination dispatch, the combination:

```text
source departure committed
+ Host migration = prepared
+ destination never invoked
```

is enough to express known limbo: source Presence has departed and destination materialization has not begun.

After an ambiguous destination dispatch that statement is no longer justified. A falsifier produced two opposite native realities with identical Host evidence:

```text
branch A: no destination body exists
branch B: destination body exists but response/receipt is unavailable
```

Both appeared as the same Host `UNKNOWN` trajectory.

Therefore Host and World cannot infer `Presence nowhere` from migration UNKNOWN. The destination must supply native materialization evidence.

## Migration `not_committed` is stronger than admission absence

Entity Migration cannot reuse a Message-style rule that treats a missing semantic admission record as proof of non-materialization.

A real native process was allowed to survive after its controller exited while no semantic admission record existed. An admission-only reconciler would have returned `not_committed` and authorized a second body.

For Migration:

```text
semantic receipt absent
!= native body absent
```

A production `EntityMigrationNotCommitted` proof must bind the exact migration, plan, entity, destination, source departure and continuity payload and must include:

```text
exactOriginalRetrySafe = true
nativeSubstrateChecked = true
```

World persists that proof before releasing Host `UNKNOWN -> PREPARED`.

## KVM pre-body fence

The Security destination uses the existing `WindowsKvmMachineProvider` Run ledger as the destination-local pre-body fence.

Before swtpm or QEMU starts, the ledger durably binds:

- `migrationId`;
- `entityId`;
- source and destination World identity;
- exact plan digest;
- source departure digest;
- continuity payload digest.

The opaque continuity payload is written to a separate removable FAT volume labeled `ORDIVON_MIG` and read back before native launch. It deliberately does not reuse the current Guest Runner `ORDIVON_RUN` contract.

This proves transport and binding of continuity to one physical carrier. It does not claim Guest cognition activation.

## Native launch crash windows fail closed

KVM experiments exposed a lower-level recovery bug. QEMU can exist during the narrow interval:

```text
Popen(QEMU) succeeded
→ native body exists
→ qemuPid/startTime not yet persisted
```

The old orphan reconciler trusted only persisted PIDs and could incorrectly report `qemuClosed=true`, remove the Run and ledger, and leave the unregistered process alive.

Security now treats launch artifacts with missing persisted process identity as:

```text
attention-required
reason = unpersisted-native-launch
```

The Run and ledger remain retained. No retry is authorized.

This is deliberately a fail-closed repair, not an invented recovery success.

## Fresh-controller recovery is Provider-owned

A second experiment persisted only `migration-staged`, then replaced the controller before any native process started.

The KVM Provider now exposes thin recovery primitives:

```text
load_state(...)
claim_existing_state(...)
```

They reconstruct the ledger path, validate deterministic Run/instance/generation/base-image identity, reject takeover from a different live owner, and transfer controller ownership only from a dead owner.

A fresh controller resumed the same Run and same instance into one QEMU carrier. No new migration store was required.

## Destination materialization authority

The first production destination is Security `WorldEntityKvmDestination`.

Its authority comes from host-owned KVM state and QMP, not Guest self-report:

```text
guestClaimAuthority = not-used
materializationRole = entity-continuity-carrier
networkDevicePresent = false
```

The first physical trajectory materialized a real Windows KVM VM with the exact Game departure and continuity binding, QMP `running`, and no NIC.

Security writes a durable `EntityMigrationReceipt` only after the contained KVM carrier is externally observed.

## Historical materialization is not current Presence

A later experiment allowed the QEMU process to disappear after the materialization receipt had already been committed.

Fresh reconciliation returned the same historical receipt and did not start another body.

Therefore:

```text
historical EntityMigrationReceipt
!= current live Presence
```

A future request to reacquire or reactivate Presence must be a new destination-local action with its own authority. It cannot be inferred from an old Migration receipt.

## The two UNKNOWN branches

### Destination materialized, response lost

A real Game departure was prepared through Host, Security materialized the KVM carrier, and the transport deliberately discarded the response.

```text
Security materialized
→ ACK lost
→ Host UNKNOWN
→ Game export deleted
→ fresh Host reconcile(plan only)
→ same retained Security receipt
→ zero rematerialization
```

Source departure and continuity were not resent during reconciliation.

### Destination was never invoked

A separate trajectory deliberately reported an ambiguous transport failure before Security was called.

```text
Host UNKNOWN
→ fresh Security reconcile(plan only)
→ deterministic native Run absent
→ nativeSubstrateChecked=true
→ not_committed
→ Host persists proof
→ UNKNOWN -> PREPARED
→ exact original retry
→ one KVM body
```

A second Host `materialize()` used the retained receipt and did not call the destination again.

## Host ownership and current addressing

Host owns the durable migration commitment and uncertainty state. It does not own destination Presence truth.

The migration remains semantically identified by `migrationId`, but 0.4.0 intentionally retains one Entity Migration per Host Task. Unlike Resource, Message and provider Dispatch, no real workload has yet reproduced a need for multiple concurrent migrations inside one Task.

No `worldEntityMigrations[migrationId]` map or universal `WorldTrajectory` is promoted without that failure.

## Trust boundary

The first Security consumer structurally binds `EntityDepartureReceipt` but declares:

```text
sourceAuthorityAuthentication = caller-trust-boundary
```

An untrusted relay requires independent source-authority authentication. Existing Message experiments show cryptographic peer binding is feasible, but 0.4.0 does not prescribe a universal PKI or first-class `WorldLink`.

## What 0.4.0 does not claim

The production Entity Migration contract does not add:

- a global Presence database;
- a universal Migration manager;
- automatic Guest cognition bootstrap;
- current-Presence liveness inside a historical receipt;
- copied source-local position, capability, inventory or authority;
- a universal Entity or Actor grammar;
- multi-migration Task orchestration;
- a first-class `WorldLink`;
- mandatory PKI;
- implicit body resurrection.

The stable responsibility is narrower: source departure authority, exact continuity binding, Host uncertainty continuity, destination pre-body fencing, native materialization evidence and safe reconciliation.
