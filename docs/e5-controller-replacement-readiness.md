# E5 — Controller Replacement Readiness

World now exposes `WorldTaskInspector.inspect_replacement_readiness()` as a bounded, revision-fenced read-only projection over existing owner-native commitments.

The projection answers one question only: would replacing the current cognition/controller orphan an unresolved reconciliation obligation?

A commitment blocks clean replacement only when its current `nextOwnerOperation` is an owner reconciliation operation. A merely `prepared` but unambiguous commitment does not block replacement: the successor controller inherits the exact retained commitment and the physical owner still controls any later dispatch. Terminal receipts likewise do not block replacement.

The projection explicitly returns `actionAuthority=not-granted-by-inspection` and `externalCurrentness=not-claimed`. `replaceable=true` therefore does not authorize retry, dispatch, reconciliation or any external effect. An `UNKNOWN` relation remains blocked until the original owner reconciles it or produces an exact owner-native `not_committed` release.

No quiescence database, global transaction manager or second World truth owner is introduced.