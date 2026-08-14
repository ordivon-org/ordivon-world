# AM3 — Morphology Relation Continuity

Status: empirical World challenger for the cross-owner Agent Morphology program.

## Question

Can the acting cognition/controller/process morphology be replaced while the same World consequence identity remains authoritative, without duplicate Resource transfer, Message delivery, or Entity materialization?

## Experiment

`tests/test_am3_morphology_relation_continuity.py` deliberately uses distinct Host owner identities (`morphology:loop-a` then `morphology:loop-b`) around one durable World trajectory. The owner-id change is not claimed to be a real LoopDriver implementation; it is a hard process/controller replacement that removes in-process continuity and therefore supplies the consequence-boundary falsifier AM3 needs.

For each trajectory:

1. first controller prepares the exact World consequence;
2. destination commits the effect but drops the response;
3. World retains `unknown`;
4. first Host/controller closes;
5. a fresh replacement controller reopens the same owner-native trajectory;
6. direct redelivery/rematerialization is rejected;
7. reconciliation of the original identity recovers the retained destination receipt;
8. destination effect count remains one.

The three tested trajectories are:

- Resource Transfer — no second destination materialization;
- Message Delivery — no second inbox delivery, and delivery still does not promote destination knowledge;
- Entity Migration — no second destination body/materialization.

A fourth test exercises the release case: after replacement, an exact owner-native Resource `not_committed` proof with `exactOriginalRetrySafe=true` moves the original trajectory from `unknown` back to `prepared`; only then may the same original transfer be retried and materialize once.

Targeted result: 4/4 tests pass.

## Result

Morphology/process replacement is **orthogonal** to World consequence identity. Replacement neither grants retry authority nor invalidates the original relation. The surviving law is:

```text
controller/loop/process replacement
              !=
World consequence replacement
```

and:

```text
UNKNOWN + new morphology != safe retry
UNKNOWN + exact owner-native not_committed proof = original retry may become admissible
```

This is stronger than a same-process hot-reload guarantee: the process may disappear completely and relation continuity still survives because the relation is owner-native durable evidence rather than plugin memory.

## Implication for Agent identity

The result supports AM0's distinction between cognitive morphology and relational identity. A different model/loop/controller may continue the same Agent/Task only by inheriting the exact outstanding World relations. It cannot silently create fresh Resource/Message/Entity identities to escape uncertainty.

For Entity Migration the destination relation is especially strong: continuity does not imply destination-local Presence/capability/authority, and an eventual `not_committed` release requires the destination-native substrate check already enforced by the Entity owner.

## Relational Quiescence update

AM3 confirms the candidate predicate:

A morphology transition is consequence-quiescent for a given owner only when that owner has no outstanding admitted consequence, or every consequence is terminal with an exact receipt, or an exact owner-native `not_committed` proof has explicitly released the original retry path.

`UNKNOWN` is not quiescent.

No global quiescence database or World transaction manager is implied. AM4 must determine how an Agent/caller can mechanically intersect owner-native projections without creating a second truth owner.
