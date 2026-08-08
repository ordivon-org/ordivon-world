---
schema_version: 1
id: world.w2-host-trajectory-addressing
title: W2 Host Trajectory Addressing
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
evidence_status: executable
readiness: READY
applies_to:
  - ordivon-world
related:
  - world.w2-resource-transfer
  - world.authority
---
# W2 Host Trajectory Addressing

## Finding

Two independent production paths reproduced the same failure:

```text
Host Task identity != external trajectory identity
```

The first failure appeared in Resource Transfer: after Resource A completed, a distinct Resource B on the same Task was rejected because the extension stored one flat `worldResourceTransfer*` record.

The second appeared in the Cloudflare provider path: after Dispatch A succeeded, a distinct sequential Dispatch B on the same Task was rejected because `HostWorldExtension` stored one flat `worldPreparedDispatch*` record.

Artificially splitting one higher-level Task into child Tasks made both cases work, but only as a workaround.

## Stable private addressing rule

World now retains trajectory state by the semantic identity already owned by that trajectory:

```text
Host Task
  ├── worldResourceTransfers
  │     ├── transfer:A -> independent Resource trajectory
  │     └── transfer:B -> independent Resource trajectory
  │
  └── worldDispatches
        ├── dispatch:A -> independent provider trajectory
        └── dispatch:B -> independent provider trajectory
```

Resource uses `transferId`; provider correlation uses Host `dispatchId`. There is no new public `WorldTrajectoryId` because no third identity is needed.

When exactly one instance exists, the public helpers retain the convenient implicit lookup. When more than one exists, callers must supply the semantic identity. Ambiguous implicit selection fails closed.

## Partial uncertainty remains local to one trajectory

Both paths were pressure-tested with partial state:

```text
trajectory A = succeeded/materialized
trajectory B = unknown
```

Reconciliation of B does not rewrite A. Host restart recovers the original B identity and performs no redispatch when the native/provider receipt already exists.

## Durable upgrade law

0.2.0 persisted Resource and provider extension state in flat Task fields. A direct multi-instance rewrite initially stranded those durable Tasks.

The corrected upgrade behavior is:

```text
read legacy flat state
    -> expose one virtual trajectory instance

first later mutation
    -> write the instance map atomically
    -> preserve the legacy trajectory
    -> remove legacy flat fields
```

This is verified for:

- pre-P4 flat Resource state;
- pre-P5 flat provider `prepared` state;
- pre-P5 flat provider `unknown` state recovered from the original provider Receipt without another POST.

New writes use only the instance maps.

## Addressing is not authority

A discriminator intentionally kept Dispatch A at `unknown` and then inserted/delivered Dispatch B. `HostWorldExtension` can store both trajectories.

That behavior does **not** mean World authorizes B.

Host owns Effect/Binding/Dispatch authority and exposes unresolved Dispatches to its cognition/engine. World receives a `PreparedWorldDispatch` and retains its provider correlation/evidence. Therefore:

```text
World can address a trajectory
!=
World may authorize that trajectory
```

World must not invent a blanket Task-level rule such as “one UNKNOWN blocks every other trajectory”; that would steal Host authority and could reject already-authorized independent work. Conversely, callers must not treat `HostWorldExtension.prepare()` as Effect admission.

## What this does not justify

The two-consumer result justifies a private Host-extension addressing invariant. It does not justify:

- a universal public `WorldTrajectory` object;
- a global World head or revision;
- a global Effect/Dispatch authority layer in World;
- automatic cross-domain concurrency policy;
- migrating experimental Entity/Message storage before production pressure forces it.
