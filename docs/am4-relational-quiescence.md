# AM4 — Relational Quiescence Without a New Truth Owner

Status: empirical projection result; no production mechanism added.

## Correction from AM2/AM3

AM2's first wording was too strict: an `outstanding` World commitment is not automatically a morphology-replacement blocker. A `prepared` consequence has durable identity but may still be pre-dispatch and unambiguous. Replacing the cognition/controller is safe if the next controller inherits the exact commitment and the physical owner revalidates before effect.

The actual blocker is **unresolved reconciliation obligation**.

## Existing sufficient surface

`WorldTaskInspector` already provides a revision-fenced, read-only aggregation of provider/resource/message/entity owner projections. It does not decode owner storage, does not grant authority, and each commitment exposes `state`, `commitmentClass`, `nextOwnerOperation`, `actionAuthority=not-granted-by-inspection`, and `externalCurrentness=not-claimed`.

AM4 therefore tests a research-only derived projection over this existing output rather than creating a `RelationalQuiescence` database/service.

Research predicate:

```text
replacement projection is blocked
iff
any owner commitment requires reconcile-original-*
```

This means:

- initial `prepared` commitment → controller replacement may proceed; exact commitment remains and action authority is still owner-native;
- terminal receipt → replacement may proceed;
- `unknown`/ambiguous state requiring reconciliation → replacement is blocked as a clean morphology transition;
- exact `not_committed` proof → ambiguity is removed and replacement may proceed, but the projection itself still grants no retry authority.

## Experiment

`tests/test_am4_relational_quiescence_projection.py` covers:

1. pre-dispatch Resource `prepared` → replaceable, no action authority;
2. response-loss `unknown` → one reconciliation blocker; after exact original reconciliation to receipt → blocker clears;
3. `unknown` released by exact `not_committed` proof → blocker clears, but derived projection still says `actionAuthority=not-granted-by-derived-projection`.

Targeted result: 3/3 pass.

## Decision

Do not add a global quiescence state owner. The minimum mechanism is already present:

```text
revision-fenced Host Task
      +
owner-native World commitment projections
      +
caller/Agent derived blocker intersection
```

The projection answers only whether a clean cognition/controller replacement would orphan unresolved relational uncertainty. It cannot dispatch, retry, reconcile, change World state, or prove external currentness.

This also means same-process hot reload has no special exemption: if an external relation is ambiguous, keeping the process alive does not make it quiescent.

## Next

AM5 should test generated morphology candidates under the existing Ordivon self-change discipline: candidate generation must remain separate from execution/evaluation/promotion, and a generated Loop candidate must not become executable merely because it can be loaded.
