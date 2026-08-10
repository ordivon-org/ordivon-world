---
schema_version: 1
id: world.w4-agency-authority
title: W4 Agency and Authority Boundaries
type: decision
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
evidence_status: cross-repository-verified
readiness: ARCHIVED
applies_to:
  - ordivon-world
related:
  - world.authority
  - world.boundaries
  - world.w2-entity-migration
---
# W4 Agency and Authority Boundaries

## Decision

W4 tested whether Entity continuity and current Presence imply Agency, and whether the repeated cross-repository authority problems justify a World-owned capability or delegation layer.

They do not.

The experiments used the native authority surfaces already owned by Game, Harness and Security:

```text
Game Actor capabilities / Authority Grants
Harness Tool Grants
Security AuthorityManifest
World Entity Migration evidence carriers
```

The retained result is:

```text
Identity != Presence != Authority
```

and authority semantics remain owner-specific unless a repeated production failure proves a smaller shared contract is necessary.

W4 therefore does not introduce:

```text
WorldCapabilityManager
WorldDelegationRegistry
global capability epoch
global revocation service
universal authority translator
universal operator identity service
```

## Presence does not mint authority

W4 supplied valid current Presence evidence to a Security action whose destination-owned authority did not permit the requested operation. Security rejected before backend execution.

```text
current Presence
+ no action authority
= no action
```

Presence answers a current embodiment/location question. It does not answer whether the observed entity may perform an action.

The reverse shortcut is also false: an action may be legitimate without Presence when the domain defines it as a remote/control-plane operation. Security `observe-only` execution demonstrated this with a valid `AuthorityManifest` and no Presence requirement.

The general law is:

```text
action admission
= destination validation of the prerequisites required by that action
```

Presence, locality, current World state, Actor capability, Run authority or operator authority may be prerequisites for a particular action, but no single prerequisite is universal.

## Body replacement is not universal revocation

Security authority scoped to the same Sample/Environment/action remained meaningful across replacement bodies. A Harness Tool Grant scoped to one durable Harness Run likewise survived execution-body/workspace replacement while its execution binding changed.

Therefore:

```text
body replacement
!= automatic authority revocation
```

Validity follows the native authority owner's declared scope. A body-local grant may end with that body; an Actor-, Run-, Sample- or Environment-scoped authority need not.

## Planning eligibility is not final authority admission

W4 found a real Game defect: Station Zero planning filtered interaction candidates by Actor capabilities, but final Turn admission did not re-check all of those capabilities. Protocol objects constructed outside the planner could therefore reach mutation with authority the Actor did not own.

The repair moved the native Game authority check to the final mutation boundary. No World capability manager was added.

The original experimental repair commit was:

```text
d6ac05bf6d7e526be6d849d4bbab4e7b29e336d1
```

The canonical Game integration is the patch-equivalent commit:

```text
f34b66ef0319ca37456fd91be03aa75ea6bf2cd3
```

Their stable Git patch IDs are equal. Current Game full acceptance after Entity integration passes 255 tests.

The retained rule is:

```text
planning eligibility
!= final authority admission
```

Prompt-visible Candidates, UI controls and planning filters help cognition. They cannot replace authority checks at the boundary where the World is actually mutated.

## Claims and evidence can travel; authority does not automatically travel

W4 carried source-domain authority/capability claims through an Entity continuity path and showed that Security did not treat them as destination authority. Current production Entity Migration reinforces the same boundary more narrowly:

```text
source departure authority
→ transported as exact evidence

opaque continuity
→ transported by digest

source-local authority
→ not copied into destination authority
```

The accepted Game → World → Security Entity trajectory records:

```text
worldAuthorityTranslation = false
globalWorldPki            = false
guestClaimAuthority        = not-used
```

Security independently owns destination admission/materialization. World binds and carries source evidence; it does not promote that evidence into Security authority.

Thus:

```text
portable claim/evidence
!= destination authority
```

A destination may inspect source evidence and issue its own authority. That is a regrant unless the new authority explicitly retains a dependency on the parent authority.

## Regrant and delegation are different

W4 made the distinction observable with a real Game parent grant.

A destination Security regrant that used the Game parent only as decision evidence remained independently executable after the parent expired. That is correct:

```text
regrant
= parent is decision evidence
```

Later invalidation of the source evidence does not retroactively revoke an already-issued independent destination authority unless the destination contract says it does.

By contrast, a child that claims to be delegated authority must retain the parent as an authority dependency:

```text
true delegated child
= parent remains an authority dependency
```

Merely storing `parentGrantDigest` or provenance metadata did not create delegation semantics. A test-only verifier that actually checked parent currentness rejected the child after the parent expired.

Therefore:

```text
digest/provenance binding alone
!= delegation
```

## Live delegation has an availability cost

When the parent authority owner could not be queried, W4 could not establish parent currentness and rejected the delegated action.

```text
parent owner unavailable
→ parent currentness UNKNOWN
→ dependent delegated authority cannot be upgraded to valid
```

Online revocation/currentness therefore creates cross-owner availability coupling. Avoiding that coupling requires an explicit different authority contract, such as bounded self-contained authority whose revocation semantics are delayed until expiry.

World may transport an opaque parent-authority reference if a future workload requires it. World may not silently choose the revocation/availability tradeoff.

## Cross-domain attenuation is not generically World-decidable

The W4 Game parent grant and Security child authority used different vocabularies:

```text
Game:
operationKind = contain_hazard
targetId      = maintenance-breach

Security:
requestedActions = [observe-only]
environment      = environment:w4-p3-security
```

No structural subset relation can prove that one is narrower than the other. Different destination policies can legitimately reject the source evidence or translate it into a bounded destination action.

If World chose that semantic translation itself, World would absorb Game and Security policy.

Within one authority schema the situation is different. Security can mechanically compare two `AuthorityManifest` values because Security owns the vocabulary and knows which dimensions narrow actions, environments, runtime/network rights and prohibitions.

Therefore:

```text
attenuation semantics belong with the authority schema/domain owner
```

## Authority creation itself requires authority

W4 also found a separate Game control-plane gap that remains unresolved in the current canonical Game surface.

A supervised Proposal correctly stops at:

```text
authority_required
```

but Mission Control approval still accepts caller-provided `issuedBy`, and the default `player:mission-control` value is a label rather than an independently established principal fact.

Current Game still has the shape:

```text
approve {
  proposalId,
  issuedBy?: string
}
```

and the server passes caller-provided `issuedBy` into the command path.

Therefore:

```text
require-human
!= verified human principal
```

A string-prefix rule such as `player:*` would not solve this because the prefix itself is only a claim.

If `require-human` is intended to be a security authority boundary, the control plane that owns operator ingress must establish caller/operator authority before approval-command admission.

W4 does **not** assign operator identity to World.

## Entity Migration integration changed the implementation, not the W4 law

The original W4 work depended on the earlier Entity Migration experiment. During integration, later Security C1-E through C1-N evidence superseded part of the old KVM recovery implementation.

The obsolete model allowed a fresh controller to claim old Provider state and rewrite predecessor ownership. The current production law is instead:

```text
historical predecessor owner
!= current recovery authority
```

and:

```text
stable/re-observed completion
→ repair publication without body replay

provably body-free abandoned preparation
+ zero-residual compensation
→ NOT_COMMITTED / exact retry-safe

ambiguous QEMU launch evidence
→ UNKNOWN
```

This evolution strengthens rather than weakens the W4 authority boundary: current physical recovery state does not mint domain action authority, and durable provenance is not silently rewritten into current ownership.

The accepted production trajectory is documented in [`w2-entity-migration-production.md`](../../w2-entity-migration-production.md) and its World receipt is:

```text
evidence/acceptance/world-entity-production-0c91b25.json
sha256:36bec36f354fce7b4a2bfecfcad6f5ce7a44bc2d9455ea956d64c84e44bc0a2d
```

## Current integration status

The W4 research conclusions are now represented by canonical product boundaries rather than a detached experimental stack:

```text
Game
  final Actor authority admission        canonical
  durable Entity Departure authority     canonical

World
  Resource Transfer                      production
  Message Delivery                       production
  Entity Migration                       production
  global capability/delegation layer     absent by decision

Security
  Resource / Message destination          canonical
  Entity KVM destination                 canonical
  current-law recovery / compensation    canonical

Harness
  Run-scoped Tool Grant semantics        retained
```

This does not mean every authority problem is solved. It means the unresolved problems now have explicit owners rather than being hidden inside a generic World layer.

## Retained W4 laws

```text
Identity != Presence != Authority
Presence does not mint authority
body replacement does not universally revoke authority
planning eligibility != final authority admission
action prerequisites are action-specific
claims/evidence may travel without authority travelling
regrant != delegation
true delegation retains a parent-authority dependency
digest/provenance binding alone != delegation
cross-domain attenuation requires domain semantics
unknown parent currentness cannot be upgraded to valid
minting authority requires issuer authority
```

A future cross-World delegation workload may justify an opaque parent-authority dependency reference. A future untrusted-relay Entity deployment may justify source authentication. A future operator control plane must resolve authenticated principal ingress if `require-human` is to carry security meaning.

None of those pressures currently justify a universal World authority service.
