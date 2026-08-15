---
schema_version: 1
id: world.research.closeouts
title: Research Closeouts
type: decision
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: Compact current index of closed W4/W5/Sense-Connect-Act laws, counterexample evidence and explicit reopening conditions.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-world
---
# Research Closeouts — Minimal Current Index

This is the current compact index for closed World research lines. The long W4/W5/Sense–Connect–Act studies remain historical evidence, not current product authority. Current product truth is README + ARCHITECTURE + STATUS + contracts/source + commit-bound evidence.

## Status

W4, W5-A/B/C/D/E, W-X4 and Sense/Connect/Act are **closed research lines**. None is the current World frontier. Their purpose is to preserve counterexamples that constrain future designs, not to advertise active product work.

## Retained laws

### Agency / authority

- Presence does not mint authority.
- Planning eligibility, UI visibility and model choice do not replace authority checks at the mutation/effect boundary.
- Source claims/evidence may travel; destination authority does not automatically travel with them.
- A true delegation retains a dependency on parent authority; provenance metadata alone is not delegation.
- Unknown parent currentness cannot be upgraded to valid.
- Minting authority requires issuer authority.

Historical study: [`docs/archive/research/w4-agency-authority-boundaries.md`](archive/research/w4-agency-authority-boundaries.md). Evidence includes `evidence/acceptance/world-entity-production-0c91b25.json`.

### Embodiment / Presence

- Continuity Subject, current Cognition instance, domain Body and exact Action/Plan coordinates are distinct.
- A payload digest proves bytes are unchanged, not who owns or semantically admits them.
- A bounded embodiment occurrence does not prove continuing Presence.
- Presence is owner-observed, scope-bound current relation evidence. Historical Presence may remain evidence after currentness expires, but does not remain current.
- Current observation failure yields `UNKNOWN`; historical success must not fill the gap.
- No global Agent identity, Embodiment or Presence registry is justified.

Historical studies: [`docs/archive/research/w5-agent-embodiment.md`](archive/research/w5-agent-embodiment.md), [`docs/archive/research/w5-presence.md`](archive/research/w5-presence.md). Key evidence: `w5a-a3-real-embodiment-083d619.json`, `w5a-a4-presence-888ca4e.json`, `w5b-b0-agent-current-relation-e40842d.json`, `w5b-b1-security-active-destination-e40842d.json`, `w5b-b2-cross-domain-minimum-acceptance-5f5a253.json`.

### Discovery / connection / relation

- Discovery/discovered identity, affordance, reachability/reachable state, protocol/session state and authority are orthogonal dimensions.
- Discovery or reachability never upgrades missing authority.
- A relationship/session object exists only when the owner protocol needs one; traffic through an endpoint/relay does not create universal relationship identity.
- Current owner observations may change an Agent decision, but remain informational and require owner revalidation before effect.

Historical study: [`docs/archive/research/w5-discovery-connection.md`](archive/research/w5-discovery-connection.md). Evidence: `w5c-c0-discovery-connection-d1a65a4.json`, `w5c-c1-agent-contact-decision-c393f19.json`.

### Interaction / partial consequence

- Resource, Message, Entity and direct Provider effects retain distinct semantics even where mechanics look similar.
- Typed trajectories can share private causal/recovery mechanics without a public `GenericInteraction`.
- Success of interaction A does not imply success of B. Partial external chains converge forward; they do not require global rollback.
- Evidence from one family may inform a later decision but does not mint another family's authority.
- Each UNKNOWN trajectory reconciles its exact original identity before retry; exact retry is permitted only after owner-native `NOT_COMMITTED` proof where that family supports it.

Historical study: [`docs/archive/research/w5-interaction.md`](archive/research/w5-interaction.md). Evidence: `w5d-d0-interaction-families-e165cfe.json`, `w5d-d1-mixed-composition-3ce688d.json`.

### External commitment continuity

- Historical capability/reference identity is not current applicability.
- Re-observation creates new applicability evidence; it does not rewrite old evidence.
- Pre-admission Agent selection is recomputable planning state.
- **Durability begins at the first owner-admitted consequence boundary.**
- After that boundary, UNKNOWN requires owner-native reconciliation of the exact original identity before retry.

Historical study: [`docs/archive/research/w5-external-commitment-continuity.md`](archive/research/w5-external-commitment-continuity.md). Evidence: `w5e-external-commitment-continuity-20260810.json`.

### Execution mobility

- Runtime owns Workspace/Job/Attempt/execution-target/input/Artifact lineage. World does not create an execution-migration ontology.
- **Pre-admission** execution mobility: before a new consequence after execution-context change, re-observe current owner reality and re-select/revalidate the path or capability; do not persist an old selection as authority.
- If a consequence was already admitted, preserve the exact World consequence identity and reconcile it before any new dispatch.
- Readable Git/source bytes are not equivalent to Runtime immutable external-input materialization.

Historical study: [`docs/archive/research/w5-execution-mobility.md`](archive/research/w5-execution-mobility.md). Evidence: `wx4-execution-mobility-20260810.json`.

### Sense → Connect → Act

- Sensor/discovery evidence, Connector relation formation/usability and Effect execution are separate proof boundaries.
- A lower-stage success must never be silently promoted to a higher stage.
- Relation/path evidence is path-bound and degradable; `connected=true` is insufficient.
- Workstation/provider owners retain physical network mechanics; World may retain bounded owner evidence without becoming a network control plane.
- W-X1/W-X3 effect-path/capability projections preserve useful historical evidence, but HP4 did not prove fresh-Agent decision advantage and HP8 removes their executable Python APIs and three packaged contracts entirely from the product package.

Historical study: [`docs/archive/research/world-sense-connect-act.md`](archive/research/world-sense-connect-act.md). Related evidence: `world-sensor-discovery-p0-2f96451.json`, `world-connector-p0-78ddb99.json`, `world-connector-p1-effector-p0-c173b8a.json`, `world-foreign-egress-capability-handoff-wx1-wx2-20260810.json`, `hp0-hp4-survival-20260810.json`.

## Current surviving product boundary from the research

The research does **not** imply a World Manager, Presence registry, Capability registry, generic Interaction, automatic router, global relationship/session service or execution migration manager. The current surviving production responsibilities are narrower:

1. exact cross-owner consequence binding and typed transfer semantics;
2. UNKNOWN + exact-original reconciliation after possible external consequence;
3. bounded owner inspection with no action authority;
4. narrow World-owned observation availability where provider time and Host admission cannot reconstruct it;
5. explicit Browser multi-object integrity;
6. owner-native provider/network truth rather than World-owned physical control.

## Reopening rule

A closed research line may **reopen** and return to active status only after a named current workload reproduces a failure that current Host + Runtime + provider/domain owner + retained World contracts cannot own cleanly. Historical prose alone cannot reactivate a component.


## Capability Field CF0 — problem-space phase closeout

CF0 of the Actor × Environment × Institution Capability Foundations programme is **closed as a phase; CF1 remains the active handoff**.

Retained result:

- current World `ResourceFor / ActionableResourceFor / Option / Capability` semantics already provide a relational capability baseline;
- `CapabilityField` is research shorthand only and did not earn a persisted primitive;
- Environment and Institution survive as distinct causal roles where deleting exposure versus durable rule/authority/ownership/recovery structure changes the counterfactual, but neither earns a universal object/schema;
- strong M2 static interaction subsumes every current M3 transition-topology prediction, so `Institutional Conversion Topology` has **0 incremental predictive cases** and remains only a mechanism-decomposition candidate;
- dynamic capitalization, endogenous selection/sorting and long-horizon coevolution remain the genuinely additional research burdens;
- normative institution design remains outside CF0–CF9.

Primary artifacts: [`capability-field-cf0-problem-space.md`](capability-field-cf0-problem-space.md), [`capability-field-cf0-closeout.md`](capability-field-cf0-closeout.md), and `evidence/acceptance/capability-field-cf0-matrix-20260816.json`.

Reopen CF0 only if a new discriminator invalidates the frozen model/problem decomposition or a currently rejected candidate gains a real deletion consequence. Do not create a Capability registry, Institution service, complete Environment snapshot, or scalar quality model from this phase.


## Capability Field CF1–CF9 — causal foundations closeout

CF1–CF9 of the Actor × Environment × Institution Capability Foundations programme is **closed**. The programme did not earn a Capability Field implementation. Its reusable result is the compact [`capability-context-doctrine.md`](capability-context-doctrine.md); detailed phase evidence remains in `capability-field-cf1-*.md` through `capability-field-cf9-*.md` and matching `evidence/acceptance/capability-field-cf*-20260816.json` artifacts.

Retained laws:

- Capability remains the existing boundary-/transition-/condition-relative supported relation; realized performance is not retained Actor capability identity.
- Environment and Institution are query-activated causal roles, not complete World objects or new truth owners.
- M3 transition topology remains rejected as an independent predictive family; its surviving value is intervention/owner localization when mechanism detail changes the next action.
- capability production is different from current expression; joint-system and retained component capability may move differently.
- exposure assignment/sorting is separate from exposure effect; observed environment gaps are not automatically intervention effects.
- causal claims, transport claims and feedback claims are admitted only to the strength identified by their design, assumptions, target boundary and Attribution evidence.
- descriptive causal modeling does not define a universal normative `InstitutionQuality` or `CapabilityValue` objective.

Final promotion: **1 compact doctrine document; 0 production code paths, schemas/contracts, services/registries, or persisted Capability/Environment/Institution/causal state primitives.**

Reopen only when a named current workload shows that owner-native Resource/Capability projections plus the compact doctrine cannot represent or correctly localize a repeated decision, causal-identification, transport or recovery failure. Conceptual completeness alone is not a reopen trigger.
