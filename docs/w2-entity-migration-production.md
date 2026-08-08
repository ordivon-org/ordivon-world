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

## Decision

Entity Migration is promoted as the third production inter-World trajectory for the first verified deployment profile:

```text
trusted local owner-originated caller

Game source authority
  retained verified extract
        ↓
EntityDepartureReceipt
        ↓
World / Host
  exact migration + opaque continuity
        ↓
Security destination authority
  contained Windows KVM materialization
        ↓
EntityMigrationReceipt
```

This promotion does **not** make World an Entity authority, Presence database, authentication service or migration runtime. Game owns source departure. Host owns durable work and uncertainty continuity. Security owns destination materialization and recovery facts.

The accepted physical cross-repository receipt is:

```text
evidence/acceptance/world-entity-production-0c91b25.json
sha256:36bec36f354fce7b4a2bfecfcad6f5ce7a44bc2d9455ea956d64c84e44bc0a2d

Game     8d89410e24ba486173ae6f3474962bb26433a6f5
World    0c91b25944cf88b8d27e4f21f1b6a89c0051a65d
Security ca8d89ef349adeb4d507bf54a2143ada37657ae1
```

The trajectory created a real Station Zero extraction, reopened Game in a fresh process and recovered the exact departure authority, prepared the migration through a real Host journal, materialized a real Security Windows KVM continuity carrier, reopened Host without redispatching, and closed the destination with zero residuals.

## Identity, cognition, Presence and body remain separate

The production contract retains the W0/W3 distinction:

```text
Entity identity
!= cognition / memory state
!= World-local Presence
!= execution body
```

Game owns only its local departure occurrence. The continuity payload is an opaque payload bound by digest; it does not copy Game-local position, inventory, capabilities or authority into Security.

Security materializes a contained KVM carrier. Guest self-report is not destination authority and the current Guest does not need to interpret the continuity payload for the migration to be admitted.

## Source departure authority

Station Zero `extract` is the first production source authority. Game issues `EntityDepartureReceipt` only when retained native evidence binds:

- `actor_life_state_changed` ending in `extracted`;
- the exact retained `extract` Intent;
- an executed `actor_extracted` resolution;
- `verificationPassed=true`;
- retained post-turn actor state `extracted`.

The source occurrence also carries record, state, Fact and Intent digests. A single departure occurrence can authorize only one `migrationId`; changing the destination or reusing the occurrence for another migration fails closed.

The production acceptance then closed and reopened Game in another process and recovered the exact same durable departure receipt before World accepted it.

That proves native owner persistence. It is deliberately **not** presented as cryptographic proof to an arbitrary remote recipient.

## World binds; it does not translate authority

World validates the typed `EntityDepartureReceipt`, commits an exact `PreparedEntityMigration`, retains the opaque continuity payload and dispatches the exact destination request through `EntityMigrationWireDestination`.

The Host journal owns:

```text
migration plan
source departure object
continuity object
UNKNOWN state
not_committed proof
historical destination receipt
```

These are durable work/evidence bindings, not a new World authority system.

The production trajectory required:

```text
worldAuthorityTranslation = false
globalWorldPki            = false
```

Therefore the experiment does not justify a `WorldCapabilityManager`, global Entity authority registry or universal authority translator.

## Destination materialization authority

Security `WorldEntityKvmDestination` owns destination materialization. Its accepted execution identity is based on the current Security recovery law:

```text
recoveryMode = reobserve-publish-or-prebody-compensate-no-owner-rewrite
unpublishedNativeState = unknown-unless-completion-or-safe-abandonment-observed
sourceAuthorityAuthentication = caller-trust-boundary
```

For a fresh materialization, Security:

1. durably binds the migration before native launch;
2. stages the opaque continuity payload on an `ORDIVON_MIG` FAT carrier and reads it back;
3. starts the contained KVM substrate with no NIC;
4. uses Host/QMP/native evidence rather than Guest claims;
5. writes one historical `EntityMigrationReceipt` only after materialization is externally established.

The accepted cross-repository run recorded:

```text
materializationRole  = entity-continuity-carrier
guestClaimAuthority  = not-used
networkDevicePresent = false
cleanupClean         = true
```

## Recovery follows observed physical facts, not old ownership takeover

Earlier W2 experiments temporarily used a fresh controller that claimed an old Provider state and rewrote controller ownership. Later Security C1-E through C1-G disproved that model.

The retained law is:

```text
historical predecessor owner
!=
current recovery authority
```

and:

```text
same durable ledger digest
!=
same physical World progress
```

Production Entity Migration therefore does **not** depend on `claim_existing_state()` takeover or rewriting `ownerPid` / `ownerStartTime`.

Current single-host recovery distinguishes three classes.

### Stable or independently re-observed completion

If the destination has a stable publication, or current physical observation independently proves the completed contained carrier, recovery may repair only the missing publication/receipt. It does not replay the Entity body.

### Provably body-free abandoned preparation

If the predecessor controller is dead and independent observation proves that no QEMU body launched, reversible preparatory consequences may be compensated to zero residuals.

The physically accepted cases are:

```text
migration-staged
swtpm-started with exact TPM-only process
```

Only after exact cleanup reaches zero residuals may Security issue:

```text
nativeSubstrateChecked = true
exactOriginalRetrySafe = true
```

and allow World/Host to move `UNKNOWN -> PREPARED` for the exact original retry.

### Ambiguous QEMU launch evidence

A missing published QEMU PID is not proof that no launch occurred. A physical SIGKILL experiment created QEMU stdout/stderr launch evidence while the durable ledger still had no QEMU PID.

That state remains:

```text
UNKNOWN
reason = unresolved-native-materialization:qemu
```

It is not compensated by the Entity reconciler and does not authorize retry.

Thus:

```text
no published QEMU PID
!= proof of no QEMU launch
```

and:

```text
provably body-free + zero-residual compensation
→ NOT_COMMITTED / exact retry-safe

ambiguous launch evidence
→ UNKNOWN
```

The underlying Security acceptance evidence is retained by the Security owner; World relies only on the destination contract and the physical cross-repository result, not on copied recovery authority.

## UNKNOWN and no blind redispatch

A destination response loss remains UNKNOWN. Host must reconcile the original migration identity before any second body can be considered.

A `not_committed` proof is stronger than receipt absence. It must bind the exact migration, plan, entity, destination, source departure and continuity payload and must include:

```text
nativeSubstrateChecked = true
exactOriginalRetrySafe = true
```

World persists that proof before releasing the exact migration for retry.

Conversely, a retained historical materialization receipt prevents a second body. The accepted cross-repository run reopened Host after materialization and returned the exact same receipt with:

```text
destinationExchangeCalls = 1
blindRedispatch           = false
```

## Historical materialization is not current Presence

`EntityMigrationReceipt` proves a historical destination materialization. It does not prove that the body or Presence remains live later.

```text
historical materialization
!= current Presence
```

Reacquiring, replacing or reactivating a body is a new destination-local action with new authority. World does not infer it from the old migration receipt.

## Trust profile

The first accepted production profile is explicitly:

```text
trusted-local-owner-originated-caller
```

The Game producer created authority from its own retained state and a fresh Game process re-read the same durable receipt. World then carried that exact document to a local Security destination.

Security still declares:

```text
sourceAuthorityAuthentication = caller-trust-boundary
```

Therefore:

```text
Game owner verification
→ proven locally

arbitrary JSON through an untrusted relay
→ not authenticated by this profile
```

An untrusted-relay deployment needs independent source-authority authentication. This release does not prescribe a universal PKI, first-class `WorldLink`, global identity provider or World-owned authority translator merely to satisfy a deployment profile that has not yet been required by the accepted local trajectory.

## Current addressing

Entity Migration is semantically identified by `migrationId`, but 0.4.0 still retains one Entity Migration per Host Task. Resource, Message and provider Dispatch moved to per-ID maps only after real multi-trajectory failures reproduced the need.

No multi-migration Task failure has yet justified another map or a universal `WorldTrajectory` abstraction.

## What 0.4.0 does not claim

The production Entity Migration contract does not add or prove:

- a global Presence database;
- a universal Migration manager;
- automatic Guest cognition bootstrap;
- current-Presence liveness from a historical receipt;
- copied source-local position, capability, inventory or authority;
- untrusted-relay source authentication;
- a universal Entity/Actor authority grammar;
- multi-migration Task orchestration;
- a first-class `WorldLink`;
- mandatory PKI;
- implicit body resurrection.

The production responsibility is narrower:

```text
source-owned departure
→ exact continuity binding
→ Host-owned uncertainty
→ destination-owned materialization / recovery evidence
→ safe reconciliation
```

That boundary has now survived deterministic tests, real controller-loss and pre-body fault experiments, current Security recovery-law evolution, and one fresh-process Game → World → Security physical production trajectory.
