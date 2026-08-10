---
schema_version: 1
id: world.w5.external-commitment-continuity
title: W5-E External Commitment Continuity Research Boundary
type: research
profile: engineering
lifecycle: historical
source_role: historical-research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: W5-E separates recomputable Agent planning from durable owner-admitted external commitments and tests capability-reference expiry and re-establishment without a World commitment manager.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.w5.interaction
  - world.sense-connect-act
  - world.authority
---
# W5-E External Commitment Continuity Research Boundary

## Starting question

W5-D showed that a fresh Agent needs a bounded owner-authored view of outstanding external work after controller replacement. W5-E asks a narrower question before adding another durable layer:

> Which state actually has to survive because an external consequence may already have occurred, and which state may safely be recomputed from current owner observations?

The tempting design is a persistent `CapabilityManager`, `EffectPathSelectionJournal` or generic `ExternalCommitment` registry. W5-E tries to falsify that need first.

## E0: historical capability reference expires without disappearing

The W-X2 Surfpath reference remained physically present long after its successful OpenAI reachability experiment:

```text
capabilityDigest  sha256:4c070368181602b2cf88d39ca18c48f23ca5a7b6fa8571fbb625f20506e998f8
observationDigest sha256:327472b0046df888da2e573c6a59e9c8334d72212298f38885313e28dee77e4d
pathDigest        sha256:ad19ae221df2a3028e8a16b554cf152194c6f383ab7a9a3f8c45d82adee6f5eb
freshUntil        2026-08-10T04:40:13.650844Z
```

When P3 resumed, the Workstation owner reported that saved observation at about 14,106 seconds old against its 180-second execution horizon. An exact `surfpath run` using the historical observation/path was rejected with `Surfshark path observation is stale`; a marker proved the requested child executable never ran.

This establishes:

```text
reference still exists
!= current applicability
!= action authority
```

The owner rejected the stale relationship before external application execution. World did not need to revoke or delete the historical reference.

## E1: re-establishment creates a new relationship identity

A bounded fresh rediscovery used the same logical `jp-tok / openvpn-udp` intent. The old physical path did not reappear. Two newly qualified paths were observed, both reaching the OpenAI target with HTTP 401 during qualification. The Agent explicitly selected the lower observed-latency qualified path rather than granting authority to `recommendedPathDigest`.

The resulting World projection was:

```text
observationDigest sha256:5fb097c35f0e3766dcad956eea622ae2ca6978d01451d9f3cf56f64f32317797
pathDigest        sha256:7b5b389043f18ed76661332a167cccbd8c6f4eda83e8feea74cd97258b1acaf5
capabilityDigest  sha256:31602e5d485b3fc2529f3f611f46f5dc92c896c43fd0901dc04e568767b9da5a
observedAt        2026-08-10T08:33:11.176427Z
freshUntil        2026-08-10T08:36:11.176427Z
```

The exact fresh owner reference was then activated. Workstation revalidated the observation/path/destination and a keyless GET to `https://api.openai.com/v1/models` returned HTTP 401. The owner status immediately after execution still reported `fresh=true`, `executableNow=true`.

Therefore re-establishment is not mutation of history:

```text
old historical reference
        remains old historical reference

fresh owner observation
        ↓
new capability identity
        ↓
new reference
        ↓
new owner revalidation
```

A reconnect does not make an expired reference young again, and a logically similar destination does not preserve physical path identity.

## E2: selection is planning, not yet an external commitment

P1 deliberately made Effect Path selection Agent-owned. P3 tested whether that selection itself needs a durable World journal. The evidence says no.

Before an owner admits consequence-capable work, these objects are informational or planning state:

```text
owner observation
ForeignEgressCapability
EffectPathCandidate
EffectPathQuery
Agent candidate selection
capability handoff reference
```

If the controller disappears at this point, current reality can be observed again and the Agent can re-query/re-select. Persisting the old selection as a commitment would be actively dangerous because P3 proved its owner observation may expire and its physical path may disappear.

The durability fence begins only when an owner has admitted an exact operation whose consequence cannot safely be inferred from controller memory:

```text
recomputable planning
Observe → Query → Select
                   │
                   ▼
        owner admits exact effect/transfer
                   │
          DURABILITY FENCE
                   │
                   ▼
       Prepared / Dispatched / Bound
                   │
             Receipt | UNKNOWN
                   │
                Reconcile
```

For World-owned durable families, that state already exists in the typed Provider, Resource, Message and Entity journals and is projected by `WorldTaskInspector`. No separate selection or capability journal is needed to discover those commitments after controller replacement.

For a physical owner such as Workstation Surfpath, World retains the scoped reference and requires that owner to revalidate before action. If a future Surfpath operation itself becomes non-idempotent or response-loss-sensitive, its durable effect admission/reconciliation belongs with the owner or an existing Host/Runtime effect boundary; that possibility does not turn the preceding Agent path selection into a World commitment.

## E3: fresh-controller continuity does not require one Runtime Workspace

During P3 the initial Runtime workspace/control path became unusable while Host semantic continuity and owner state remained independently available. The experiment resumed from the same canonical World revision in fresh disposable Runtime workspaces and completed stale-reference rejection, fresh owner rediscovery, new capability projection and successful reactivation.

This control-plane incident is not used as proof of a specific Runtime failure mode. It is useful as a boundary check: World semantics did not require reconstruction of an old workspace in order to re-observe owner reality and continue the experiment.

## Retained laws

```text
Historical capability evidence != current applicability.

Expired reference != revoked/deleted history.

Re-observation creates new applicability evidence; it does not rewrite old evidence.

Agent path selection before owner effect admission is recomputable planning state,
not automatically a durable external commitment.

Durability begins at the first owner-admitted consequence boundary.

After that boundary, UNKNOWN requires owner-native reconciliation before retry.

Fresh-Agent commitment discovery should project existing typed owner journals,
not create a second generic commitment database.
```

## Product decision

W5-E does **not** justify:

```text
CapabilityManager
CapabilityRegistry
EffectPathSelectionJournal
ExternalCommitmentManager
GlobalCommitmentRegistry
automatic path resurrection
```

Keep `ForeignEgressCapability` and `EffectPathQuery` informational and reference-based. Keep actual durable consequence state in the owner-native Provider/Resource/Message/Entity trajectories already discoverable through `WorldTaskInspector`.

[`../evidence/acceptance/w5e-external-commitment-continuity-20260810.json`](../../../evidence/acceptance/w5e-external-commitment-continuity-20260810.json) records the live owner evidence.

## W5-E stopping condition

The P3 experiment reproduced expiry, pre-effect rejection, owner re-observation, physical path replacement, new capability/reference identity and successful reactivation. Existing typed commitment journals already cover the post-admission recovery side. No new public persistence primitive was forced.

W5-E therefore stops here. The next materially different question was execution mobility: whether one durable Host Task and exact Runtime input/artifact lineage can survive movement between execution worlds while World revalidates the external capability and reconciles effects. That W-X4 question is now closed at the World layer in [`w5-execution-mobility.md`](w5-execution-mobility.md): canonical source and Runtime lineage cross Linux/Windows, already-admitted effects reconcile across fresh controllers, and exact Windows-native external-input portability remains a Runtime-owned substrate gap rather than a new World abstraction.
