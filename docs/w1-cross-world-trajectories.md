---
schema_version: 1
id: world.w1-trajectories
title: W1 Durable Cross-World Trajectories
type: decision
profile: engineering
lifecycle: experimental
source_role: supporting
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
evidence_status: locally-verified
readiness: EXPERIMENTAL
applies_to:
  - ordivon-world
related:
  - world.start
  - world.boundaries
  - world.authority
---
# W1 Durable Cross-World Trajectories

## Purpose

W1 tests a broader World responsibility without promoting a universal World model. The question is narrower:

> Can one consequence or entity continuity leave one native World, survive process replacement, and be admitted into a different native World without duplicating the consequence or transferring source-local authority by accident?

The first two durable trajectories are Resource Transfer and Entity Migration. Both use Host's opaque extension port for persistence, while Game and Security remain authoritative for their own state and materialization.

This work is experimental. `resource_transfer.py`, `entity_migration.py`, and the private `_host_trajectory.py` helper are intentionally absent from the package `__all__` surface.

## P0-A — Resource Transfer

The verified trajectory is:

```text
Station Zero Game World
  actual extract Intent
  authoritative Turn Record + item_extracted Fact
        ↓
World Resource Transfer
  exact source-evidence digest
  exact portable-payload digest
        ↓
Host CAS / Journal
  plan + source evidence + payload
  prepared → unknown → materialized
        ↓
Security destination adapter
  source-evidence admission
  destination-local SampleVault materialization
  durable destination receipt
```

The acceptance deliberately dropped the response after the Security destination committed. The source export was then deleted, the Host process was reopened, and a fresh destination adapter reconciled the original transfer from retained evidence. Recovery performed zero additional materializations.

The source Game history remained unchanged: the extracted actor still retained its historical `research-core` inventory claim. Current cross-World custody was therefore not represented by rewriting source World history.

### P0-A invariants

- Resource Transfer has its own semantic identity.
- Source evidence identity and portable payload identity are distinct from Host CAS object identity.
- Host stores both semantic digests and CAS object digests; neither is allowed to impersonate the other.
- A known destination receipt prevents a second materialization.
- UNKNOWN is reconciled by observing the original transfer, not by issuing a new transfer.
- Destination materialization is destination-local Reality.
- Source historical evidence remains source-local evidence.

## P0-B — Entity Migration

The verified trajectory is:

```text
Station Zero Game World
  medic-reyes active → extracted
  replay-verified departure Fact
        ↓
World Entity Migration
  entity identity
  source-departure evidence
  portable continuity payload
        ↓
Host CAS / Journal
  prepared → unknown → materialized
        ↓
Security Windows KVM destination
  departure admission before QEMU start
  one Guest materialization
  Guest continuity claim
  independent QMP / containment / reset / exit / cleanup evidence
  durable destination receipt
```

The continuity payload intentionally omitted Game-local position, `lifeState`, inventory, capabilities and authority. Those values remained in Game history but were not transferred as destination-local state.

The destination did not treat the Guest claim as world truth. It accepted the migration only after binding the claim back to the admitted migration plan and source-departure digest while separately requiring Security-owned QMP and closure evidence.

After the destination receipt committed, the response was deliberately lost. The Game source export was deleted, Host was reopened, and a fresh destination adapter reconciled the retained receipt without launching a second KVM body.

### P0-B invariants

- Entity identity may continue across Worlds; source-local Presence does not travel automatically.
- Source departure must be admitted before destination materialization begins.
- `entityId`, `migrationId`, and source-departure identity must bind the exact destination receipt.
- Guest self-report remains a claim even when its content matches the migration plan.
- Independent destination evidence is required before World records a destination materialization receipt.
- Recovery observes the original destination receipt and does not rematerialize the entity.

## Shared durable mechanism

P0-A and P0-B independently reproduced the same Host-backed mechanics:

```text
semantic plan
  ↓
retain plan + source material in Host CAS
  ↓
prepared
  ↓
external/destination consequence may become uncertain
  ↓
unknown
  ↓
reconcile the original semantic operation
  ↓
exact destination receipt
  ↓
materialized
```

Only after both real trajectories existed was the duplicated mechanism extracted into the private `_host_trajectory.py` helper.

The extraction passed a deletion test:

- duplicated Resource + Entity production source before extraction: 977 lines;
- Resource + Entity + private helper after extraction: 890 lines;
- net production-source deletion: 87 lines;
- domain modules retain zero direct `put_object`, `get_object`, `inspect_object`, `append_preserving`, or `EventKind` Host mechanics.

The helper is a storage/recovery mechanism, not a public ontology. Resource and Entity schemas, destination admission, receipt binding and native-domain evidence remain separate.

## P1 — Failure Semantics

P1 attempted to break the durable P0 trajectories instead of adding a broader protocol.

### UNKNOWN forbids blind execution

A reproduced failure showed that the first P0 implementation could call the destination again while the Host trajectory was already `unknown`. If the destination receipt had also been lost, this could duplicate a Resource materialization or launch a second Entity body.

The private shared journal now fails closed:

```text
prepared
  ↓ destination may commit, response lost
unknown
  ↓
execute/materialize again       → rejected
reconcile original operation    → allowed
```

This invariant is shared because both Resource Transfer and Entity Migration reproduced the same failure. It does not grant the private helper ownership of Resource or Entity semantics.

### Link binding remains dispatch-local

Portable tests and a real Linux network-namespace/TCP acceptance replaced the A↔B endpoint repeatedly around one durable Resource Transfer.

The real trajectory observed three distinct binding digests:

1. binding 1 became stale before dispatch and produced zero destination materializations;
2. the unchanged semantic plan committed once under binding 2;
3. after response loss and Host replacement, binding 3 was used only to reconcile the original receipt.

The retained receipt continued to identify binding 2 as the commit binding. The semantic transfer plan digest remained unchanged across all three bindings.

Therefore Link binding is still a dispatch/admission condition, not part of Resource or Migration semantic identity.

### Destination receipt loss is domain-specific

Resource and Entity trajectories diverged under destination-receipt loss.

For a Resource backed by Security `SampleVault`, the native content-addressed object and manifest were sufficient to reconstruct the lost destination receipt from the already-bound payload identity. Reconciliation performed no new materialization.

For an Entity migration whose disposable KVM execution evidence and destination receipt are both gone, absence is not proof that the body never ran. Reconciliation therefore remains UNKNOWN and the Host trajectory still forbids rematerialization.

This difference is intentional:

```text
shared rule:
  uncertainty cannot authorize a new semantic consequence

destination-specific reconciliation:
  Resource CAS may reconstruct retained materialization evidence
  disposed KVM execution may remain irreducibly unknown
```

A universal reconciler would erase this distinction and is therefore not promoted.

### Historical materialization is not current Presence

P1 also deleted native SampleVault bytes after a valid Host receipt had already been retained. Host correctly preserved the historical materialization receipt, while Security's native `resolve()` returned `FileNotFoundError`.

`materialized` in the trajectory journal means that an admitted destination consequence reached durable historical finality. It does not assert that the resource or entity is currently present, alive, reachable or authoritative in the destination World.

Current Presence remains a native observation problem and is not inferred from a historical receipt.

## P2 — Durable Message Delivery

P2 added a third materially different trajectory to test whether the private Host-backed journal was truly shared infrastructure or merely an accidental similarity between Resource Transfer and Entity Migration.

The third consumer immediately exposed one overfit in the private helper: it had hard-coded `materialized` as the terminal state. Message delivery requires a different terminal vocabulary:

```text
Resource Transfer    → materialized
Entity Migration     → materialized
Message Delivery     → delivered
```

The private helper now owns a configurable terminal state and terminal receipt fields. No public World state machine was introduced.

### Delivery is not knowledge

The verified Message trajectory carries two independently digested objects:

- source provenance;
- message payload.

The semantic plan contains message identity, source and destination World identity, message kind, provenance digest and payload digest. Link binding and destination knowledge are deliberately absent.

A real Linux network-namespace/TCP acceptance delivered a source claim whose confidence was `confirmed-in-source-world`. The destination persisted exactly one inbox receipt while its separate knowledge store remained `{}`. The receipt explicitly recorded `knowledgePromoted=false`.

Therefore:

```text
message delivered
  ≠ claim verified
  ≠ destination knowledge promoted
  ≠ destination Reality changed
```

This is the durable counterpart of the earlier W0 epistemic experiments.

### Binding and recovery

The real Message acceptance replaced the A↔B native endpoints three times around one durable message:

1. binding 1 became stale before send and produced zero deliveries;
2. the unchanged Message plan committed once under binding 2;
3. the response was lost, Host was reopened, and binding 3 was used only to reconcile the original inbox receipt.

The retained receipt continued to identify binding 2 as the commit binding. The message plan digest remained unchanged, and the fresh recovery path performed zero deliveries.

### Third-consumer extraction result

Message Delivery reuses the private `_HostTrajectoryJournal` without direct Host CAS or Journal calls in the Message module. Resource Transfer and Entity Migration also retain zero such direct Host mechanics.

The third consumer did not force a public `WorldTrajectory` protocol. It forced only one internal correction: terminal vocabulary belongs to each trajectory, while prepare/uncertainty/original-operation reconciliation/receipt retention are shared mechanics.

## P3 — Durable Multi-Hop Federation

P3 tested whether A→B→C required a new federation owner. It did not.

Two independent durable Message Delivery trajectories were sufficient:

```text
A → B
  hop message identity AB
  AB receipt
        ↓ upstream receipt digest in provenance
B → C
  hop message identity BC
  BC receipt
```

The same end-to-end message identity was carried as message content/provenance, but it did not replace either hop's semantic identity.

### Partial failure and forward convergence

A three-namespace physical acceptance established two distinct links, A↔B and B↔C, with no A→C route. A→B committed first. B→C was then made unavailable.

The result was intentionally partial:

```text
A→B = delivered
B→C = prepared / unavailable
```

The upstream delivery was not rolled back. After the B↔C endpoints were replaced, the downstream hop committed once and its response was dropped. Host was then reopened and B↔C was replaced again. Recovery reconciled the original C receipt with zero second C deliveries.

A↔B retained the same native binding throughout both B↔C replacements. No global federation revision or global World head was needed.

### Hop authority is not transitive

The C receipt identified B as its native source World. A survived only as relay provenance:

- `originWorldClaim=A`;
- `upstreamReceiptDigest=<A→B receipt digest>`.

Therefore durable federation preserves the W0 authority result:

```text
A ↔ B
B ↔ C

 does not imply

A ↔ C authority
```

The upstream receipt digest correlates evidence across hops, but by itself does not make A's claimed origin authoritative at C. Strong end-to-end provenance is a separate problem.

### No federation module promoted

P3 added only reproducible composition tests. No `Federation`, `WorldGraph`, global routing table, global revision, or cross-hop coordinator was added to production code.

The current evidence favors federation as composition of independently durable hop semantics until a later failure demonstrates a responsibility that no hop can own locally.

## What W1 has not promoted

W1-P0 does **not** establish any of the following as a public shared contract:

- universal `World` or `WorldState`;
- public `WorldLink`;
- public `Presence`;
- global topology or federation revision;
- universal Resource identity;
- automatic inventory transfer;
- automatic capability or authority transfer;
- distributed atomic rollback across Worlds;
- Guest claims as authoritative physical truth;
- Security `ActorPresence` as generic Entity Presence.

The existing Cloudflare adapter path also remains distinct. `PreparedWorldDispatch`, provider request identity and Cloudflare reconciliation are Host/provider integration semantics, not aliases for Resource Transfer or Entity Migration.

## Current ownership

| Fact or responsibility | Owner |
|---|---|
| Station Zero Turn Record and departure/extraction facts | Game |
| Task state, Ready Frontier and Host revision fencing | Host |
| cross-World plan/source/payload/receipt correlation | experimental World trajectory journal |
| Security SampleVault content and resolve truth | Security |
| KVM process, QMP, containment, reset and cleanup truth | Security / machine provider |
| Guest continuity report | Guest claim only |
| destination admission decision | destination-specific adapter |

## Next promotion gate

A W1 mechanism becomes a stable public World contract only if later real consumers require the same semantics and extracting it removes duplicated responsibility rather than adding imports.

Useful next falsifiers include:

1. end-to-end provenance that must survive an untrusted or compromised relay;
2. concurrent independent trajectories whose receipts and recovery paths must not accidentally serialize through one global World head;
3. destination rematerialization where World continuity survives but native body identity changes;
4. a non-Security physical destination that independently forces the same boundary semantics;
5. dynamic federation discovery where a responsibility cannot be owned by pairwise links alone.

Until those tests force a broader contract, the W1 modules remain experimental and non-exported.
