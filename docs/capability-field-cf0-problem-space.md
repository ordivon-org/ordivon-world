# CF0 — Actor × Environment × Institution Capability Problem Space

Status: **frozen problem-space / competing-model baseline**
Owner: `ordivon-world` research
Scope: descriptive and causal structure only; no normative institution optimizer, production schema, service, registry, or new World authority.

## 1. Root question

The motivating question — “are institutional/environmental differences often more important than individual differences?” — is too compressed to answer directly.

The descriptive problem is instead:

```text
Actor state
+ owner-native Reality / Resources
+ realized Environment / exposure
+ institutional rules / authority / incentives / ownership / recovery
+ Demand / target transition
+ History
        ↓
current ResourceFor / ActionableResourceFor projections
        ↓
Requirements + Assignments + native Constraints
        ↓
Options / boundary-relative Capability
        ↓
Decision / Action
        ↓
Effect
        ↓
Outcome
        ↓
Attribution
        ↓
possible Actor / Resource / Knowledge / institutional change
```

This is an **analytical causal topology**, not a proposed persisted graph.

CF0 asks which distinctions are already expressible by current World/Computer/Human doctrine, which distinctions are genuinely missing, and what incremental failure is required before a richer model is allowed to exist.

---

## 2. Existing Ordivon baseline is already strongly relational

Current World doctrine already defines:

```text
ResourceFor(actor, aspect, transition, as_of)
ActionableResourceFor(... demand ...)
Capability = supported ability of a system boundary to cause or obtain a class of state transition under bounded conditions
```

and keeps `Requirements + Assignments + native Constraints` contextual rather than building one global composition engine.

Therefore CF0 **does not start from “capability is an intrinsic scalar.”** The existing Ordivon baseline already includes:

- actor/system boundary;
- exact Reality aspect identity;
- transition/demand scope;
- authority and currentness;
- composition/compatibility constraints;
- native capacity/load where decision-relevant;
- Decision / Action / Effect / Outcome / Attribution separation;
- signed Resource/Capability feedback;
- Human joint-system capability distinct from retained individual capability.

Any new `Capability Field` concept must beat this baseline rather than merely rename it.

---

## 3. Frozen causal-role definitions

These definitions are intentionally role-based. They do not require universal entity classes.

### Actor state

The actor-internal or actor-bound state relevant to a named transition and horizon: retained skill/knowledge, health, model weights, commitments, preferences, embodied constraints, current internal memory, or other owner-native properties.

`Actor state` does **not** mean intrinsic essence. Some current actor state may itself be the accumulated result of prior environments and institutions.

### Environment

The **realized external conditions and exposures faced by an actor for the question being asked**, excluding conditions already deliberately represented as actor state. Examples include physical conditions, available tools, network state, peers, information exposure, local infrastructure, workload, and relevant exogenous shocks.

Environment is query-relative and incomplete by design. CF0 rejects a universal complete `EnvironmentSnapshot`.

### Institution

A **durable rule/process relation that structures recurrent action situations** by changing such things as allocation, access, authority, admissible transitions, incentives, enforcement, ownership/appropriation, coordination, information rights, recovery, or exit.

Institutional state may be part of the actor's realized environment, but the role remains separately useful when deleting the rule/process structure changes a prediction about what actions are permitted, rewarded, enforced, owned, recoverable, or repeatedly selected.

CF0 does not claim that every institution has one owner or one schema.

### Realized performance

An observed task/domain outcome under a particular actor, environment, institution, support system, demand, horizon, and evidence surface.

```text
realized performance != intrinsic actor capability
```

### Effective capability

Current Ordivon definition survives CF0 as the strong baseline:

> the supported ability of a declared system boundary to cause or obtain a class of state transition under bounded conditions.

This is already relational and boundary-relative.

### Capability production

A process in which experience, investment, feedback, practice, tools, environment or institutions change a later actor/system capability state.

### Capability expression

A change in realized performance or current feasible transition set while the relevant retained actor capability need not have changed.

`production` and `expression` may coexist and require evidence to distinguish.

### Selection / sorting

Any process by which actor state affects assignment into environments/institutions, environments/institutions select actors, or both respond to common causes. Selection is an identification role, not a generic World object.

### Institutional coevolution

A long-horizon causal hypothesis in which actor/population behavior, resource distribution/power and institutional rules update one another. CF0 keeps this as research-only; temporal adjacency is not enough for causal admission.

---

## 4. Ten root question families

| ID | Question family | What must be distinguished | Primary later round |
|---|---|---|---|
| Q1 | Outcome attribution | observed Outcome vs causal credit/blame | CF2 / CF8 |
| Q2 | Capability identification | actor state vs effective capability vs realized performance | CF2 |
| Q3 | Capability production | state change vs immediate assistance | CF4 |
| Q4 | Capability expression / masking | latent/retained substrate vs current exercisability | CF2 / CF4 |
| Q5 | Resource/access allocation | existence vs access/authority/actionability | CF1 / CF3 |
| Q6 | Learning/capitalization | feedback/investment history → later actor state | CF4 |
| Q7 | Selection/sorting | causal exposure vs endogenous assignment | CF5 / CF8 |
| Q8 | Institutional mechanism | rules/authority/incentives/ownership/recovery → transitions | CF3 |
| Q9 | Coevolution | actors/resources/power ↔ institutions across time | CF6 |
| Q10 | Normative design | which plural outcomes should an institution optimize? | **separate ND series only after CF9** |

Q10 is deliberately outside the descriptive CF programme. A descriptive model does not acquire one universal welfare, fairness, autonomy, option-value, or output objective merely because it can represent institutions.

---

## 5. Strong competing model families

The models are nested only approximately; CF0 gives each its strongest plausible form rather than a strawman.

### M0 — Actor-only / intrinsic-capability model

```text
Y_t = f(X_t, demand)
```

Environment/institution may create measurement noise but do not materially change the actor's transition capability.

**Existence test:** survives only if environment/institution changes can be absorbed into ordinary noise or actor state without changing action predictions.

### M1 — Additive context model

```text
Y_t = f(X_t) + g(E_t) + h(I_t) + error
```

Environment and institutions have independent main effects, but no material interactions, state transitions, or endogenous sorting are needed.

**Existence test:** a richer model is unnecessary if additive main effects preserve relevant counterfactual rankings and action decisions.

### M2 — Static interaction / production-function model

```text
Y_t = F(X_t, E_t, I_t, R_t, demand_t)
```

Interactions and complements are allowed; same actor/resource may perform differently under different conditions. Actor/institution states are fixed during the decision horizon.

**CF0 strong baseline:** M2 is the minimum serious rival to all richer models. M3–M6 must predict something M2 cannot represent without hiding the missing responsibility inside a generic interaction term.

### M3 — Transition-topology mechanism candidate

Institutional/rule state can be decomposed as changing the **feasible transition relation**, not only output level:

```text
A_feasible(s, actor, institution)
P(s' | s, action, institution)
authority / ownership / recovery / enforcement
```

**CF0 competition result: NOT independently earned as a predictive model family.** Across the 40 frozen discriminators, M3 has **zero** cases that it represents as `ENOUGH` while the strong M2 baseline is not already `ENOUGH`. Generic M2 can in principle encode the same static mapping. Therefore transition topology remains a mechanism/causal-decomposition candidate only. CF3 may rescue it if exposing rule/authority/ownership/recovery structure improves intervention choice, causal identification, owner placement, recovery, or deletion decisions beyond a generic interaction model.

### M4 — Dynamic capitalization / skill-production model

```text
X_{t+1} = L(X_t, E_t, I_t, action_t, feedback_t, investment_t)
```

Current environment/institution can write into later actor state; path and stage matter.

**Incremental existence test:** retain M4 only where two histories with similar current conditions predict different later capability or where exposure duration/timing changes later outcomes.

### M5 — Endogenous selection / sorting model

```text
P(E_t, I_t | X_t, history, constraints) != exogenous
```

Actors choose environments; institutions select actors; common causes affect both assignment and outcome.

**Incremental existence test:** retain M5 when observational environment/institution differences cannot identify exposure effects without modeling assignment/selection.

### M6 — Actor–institution coevolution model

```text
X_{t+1}, ResourceDistribution_{t+1}, Institution_{t+1}
    = G(X_t, actions_t, outcomes_t, power_t, Institution_t, shocks_t)
```

Institutions are not fixed background; actor/resource/power distributions can change future rules and rules change future actor/resource distributions.

**Incremental existence test:** retain M6 only when an intervention or prediction depends on institution feedback rather than treating institutional state as an externally supplied trajectory.

### M7 — Normative institutional design

M7 is **not admitted into CF0 competition**. It asks what should be optimized under plural objectives and belongs to a later ND series if the descriptive model earns it.

---

## 6. Existing Ordivon responsibility map

| Needed distinction | Existing owner/surface | CF0 status |
|---|---|---|
| actor/system boundary | World `ResourceFor`, Core participant/boundary | **already owned** |
| boundary-relative capability | World R10 Capability | **already owned** |
| resource vs actionability vs option | World R10 | **already owned** |
| authority / permission | owner-native authority + World projection | **already owned** |
| conjunctive complements / requirements | World R5/R10 + domain owners | **already owned** |
| currentness / history | owner-native Events/Claims + World projection | **already owned** |
| effect vs outcome vs attribution | World R6/R10 | **already owned** |
| signed capability/resource feedback | World R7 | **research evidence already exists** |
| joint-system vs retained Human capability | Human + World R2/R7 | **already distinguished** |
| task-specific Context / externalized capability | Computing | **already owned** |
| causal environment exposure | no single universal owner | **research role; owner-native evidence required** |
| institutional rule mechanism | distributed across authority/domain owners | **research role; no global Institution object** |
| actor-state update from exposure | Human/domain-specific today | **open research role** |
| selection/sorting into exposure | Human methods / external causal literature | **open identification role** |
| institution endogeneity / coevolution | no generic current owner | **open research role** |

The immediate implication is strong:

> **CF0 does not earn a new `Capability` primitive.** Current World capability is already relational enough to serve as the baseline.

---

## 7. Vocabulary deletion tests

| Mutation | CF0 verdict | Why prediction changes / does not change |
|---|---|---|
| delete actor/system boundary | **FAIL** | same resource/tool/relationship may be a Resource/Capability for one actor and not another; joint-system capability would collapse into individual capability |
| collapse effective capability into realized performance | **FAIL** | fatigue, temporary path loss, assistance and lucky/exogenous outcomes would be misidentified as retained capability state |
| delete transition/demand scope | **FAIL** | same bytes/tool/skill can support one transition and fail another |
| delete environment as a causal role | **FAIL** | physical/tool/peer/information/exposure changes can alter current performance and later actor state without being actor-intrinsic |
| collapse institution into undifferentiated environment | **FAIL FOR SOME QUESTIONS** | loses rule/authority/ownership/enforcement/recovery counterfactuals; however institution need not be a separate persisted entity |
| delete history/time | **FAIL** | cannot distinguish production from expression, exposure duration, decay/relearning, or currentness from historical truth |
| delete selection/sorting | **FAIL FOR CAUSAL IDENTIFICATION** | observed high performers may select high-opportunity environments and institutions may select actors; exposure effect becomes confounded |
| delete Effect/Outcome/Attribution distinction | **FAIL** | observed outcome would automatically assign causal credit to actor/environment/institution |
| add universal `CapabilityField` object | **REJECT_ADD AT CF0** | current `ResourceFor` + requirements/assignments/constraints + boundary-relative Capability can already project current feasible transitions; no repeated unowned executable responsibility is shown |
| add universal `Institution` object/schema | **REJECT_ADD AT CF0** | relevant rules, rights, authority, ownership, incentives and recovery have different owners/units/clocks; CF0 needs a causal role, not a second source of truth |
| add complete `EnvironmentSnapshot` | **REJECT_ADD** | environment closure is unbounded and question-relative; current World already rejects pretending partial dependencies are complete environment state |
| add universal capability/institution quality scalar | **REJECT_ADD** | output, autonomy, resilience, distribution, option value, maintenance and recovery can move differently |
| treat “capability unmasking” as a new state type | **DEFER / likely derived** | expression can currently be represented as retained actor evidence + changed Actionability/Option under environment/institution; new primitive needs a residual failure |

---

## 8. Discriminator families frozen for CF1–CF8

The machine-readable companion matrix freezes concrete cases. They are grouped to prevent one domain from establishing a universal law by analogy alone:

1. **World/owner-native systems** — permission without bytes; authority-specific malware action; technical debt shrinking safe Options; path/currentness changes without actor-state change; lower-owner capability exported upward.
2. **Human capability** — joint-system output vs retained skill; fatigue vs skill deletion; role-specific vs transferable capability; AI assistance and later independent performance; recovery after support removal.
3. **Controlled Agent systems** — same model with different Tool grants, Context, Runtime/recovery and support availability; these are structurally clean intervention laboratories but do not prove human mechanisms.
4. **External causal evidence** — randomized neighborhood exposure, randomized search assistance, dynamic skill production, institution×biology interaction, and explicit cautions about selection/heredity inference.
5. **Institutional dynamics** — recurrent rules/norms/strategies; resource/political-power feedback; competing claims about institutions versus human capital.

CF0 uses external findings as **pressure and identification constraints**, not as authority over Ordivon owner facts.

---

## 9. External theory/evidence triangulation

CF0 adds several primary-source families to World's existing R1 resource triangulation.

### Institutional rules and recurrence

Crawford & Ostrom's institutional grammar treats institutions as enduring regularities of action structured by rules, norms, shared strategies and the physical world, and explicitly allows those structures to be reconstituted through repeated interaction.

**Transfer:** institution should be modeled by the action-structuring role of rules/norms/strategies, not by one institution-quality score.

**Do not transfer:** CF0 does not import the IAD grammar as a World schema.

### Institutions, incentives and endogenous power

Acemoglu, Johnson & Robinson model economic institutions as shaping incentives/constraints while political institutions and resource distributions jointly determine political power and change over time.

**Transfer:** M6 deserves a serious coevolution rival; institutions need not be exogenous background.

**Do not transfer:** their growth objective and country-level institutional categories are not universal Ordivon objectives/entities.

A strong opposing institutional-growth baseline also exists: Glaeser et al. argue that common institutional measures and identification strategies can misattribute growth and that human capital/policy may be more basic in some comparisons. CF0 therefore refuses to freeze “institutions are the fundamental cause” as a prior conclusion.

### Environment exposure versus sorting

The Moving to Opportunity experiment shows that age/duration of exposure to lower-poverty neighborhoods can change long-run outcomes, supporting M4-style history/exposure dynamics. Creating Moves to Opportunity shows that customized search assistance can dramatically change which neighborhoods households enter, directly demonstrating that environment assignment itself can be changed by search/bandwidth frictions.

**Transfer:** environment effects and environment selection are separate causal questions.

### Dynamic skill production

Cunha & Heckman's skill-formation model is stage-specific and includes self-productivity and dynamic complementarity.

**Transfer:** current actor capability need not be fixed; history and timing can alter future capability.

### Variance decomposition is not intervention identification

Manski argues that traditional cross-sectional heritability decomposition is fundamentally uninformative for social-policy analysis.

**Transfer:** explaining observed variance is not the same problem as estimating the effect of changing environment/institution.

### Interaction claims need stronger identification than visual heterogeneity

Pongou et al. provide one natural-experiment/twin-based example in which institutional quality changes the expression of biological/preconception effects. Conley & Rauscher provide useful negative pressure: several famous gene×environment claims can disappear under stronger endogeneity/multiple-testing controls.

**Transfer:** M2 interaction is plausible but interaction claims require explicit identification and falsification; do not infer `person × institution` from subgroup patterns alone.

---

## 10. CF0 dispositions on candidate new concepts

### Relational Capability

**Disposition: `EXISTING_DOCTRINE`, not a new primitive.**

World R10 already defines Capability relative to a system boundary, transition and bounded conditions. CF1/CF2 may sharpen identification, but CF0 finds no ontology gap.

### Capability Field

**Disposition: `RESEARCH_SHORTHAND_ONLY / REJECT_AS_PERSISTED_PRIMITIVE_AT_CF0`.**

Useful shorthand:

```text
CapabilityProjection(actor, target_transition, demand, as_of)
    := feasible supported transitions under current owner-native resources,
       authority/currentness, requirements, assignments and constraints
```

This is currently derivable from existing World semantics. A new object/service would duplicate state and authority unless CF1+ finds a repeated query/decision that cannot be represented or computed without it.

### Institutional Conversion Topology

**Disposition: `MECHANISM_DECOMPOSITION_CANDIDATE_NOT_MODEL_FAMILY`.**

The frozen anti-strawman competition gives it **0 incremental predictive cases over M2**. It earns continued study only if separating rule/authority/ownership/recovery structure changes causal identification, intervention, owner-placement, recovery, or deletion decisions. Descriptive decomposability or conceptual elegance is insufficient.

### Environmental Capitalization

**Disposition: `RESEARCH_DISTINCTION`, strong enough for CF4.**

It names a real question that static M2 cannot answer: whether prior exposures change later actor state rather than merely current performance. Human research, World R7 and external skill/neighborhood evidence supply independent pressure, but no generic update law is admitted.

### Capability Unmasking

**Disposition: `DERIVED_CANDIDATE`, not primitive.**

CF2/CF4 should test production versus expression. Existing actor-state evidence plus Actionability/Option projections may already express the required distinction.

### Selection / Sorting

**Disposition: `REQUIRED_RESEARCH/IDENTIFICATION ROLE`.**

Not a World entity. CF5/CF8 must prevent environment/institution comparisons from becoming causal claims when assignment is endogenous.

### Capability–Institution Coevolution

**Disposition: `OPEN RESEARCH HYPOTHESIS`.**

The structure appears in institutional economics and World's signed feedback logic, but generic persistence or machinery is not earned. CF6 must determine whether it transports beyond political-economy/domain-specific models.

---

## 11. Frozen model-competition audit

The 40-case matrix deliberately contains simple controls and stronger contextual/dynamic/selection cases. `ENOUGH` means the model family can represent the decision-changing distinction without hiding a required responsibility; `BOUNDARY` means it may fit the observation descriptively but cannot by itself answer the causal/operational question.

| Family | ENOUGH | FAIL | BOUNDARY | Incremental cases over immediate simpler family |
|---|---:|---:|---:|---:|
| M0 actor-only | 1 | 29 | 9 | — |
| M1 additive context | 4 | 12 | 23 | 3 |
| M2 static interaction | 22 | 0 | 18 | 18 |
| M3 transition-topology decomposition | 22 | 0 | 18 | 0 |
| M4 dynamic capitalization | 31 | 0 | 9 | 9 |
| M5 selection/sorting | 37 | 0 | 3 | 6 |
| M6 coevolution | 39 | 0 | 1 | 2 |

The count is **not a model score**; later families contain earlier representational capacity. Its purpose is only to detect whether a richer family has any frozen discriminator that actually needs its additional distinction.

The strongest CF0 negative result is M3: it currently has none. This prevents `Institutional Conversion Topology` from being promoted merely because it sounds more mechanistic than `F(X,E,I)`.

---

## 12. CF0 anti-collapse laws

CF0 freezes these as **research constraints**, not new Core laws:

```text
Observed Performance != Intrinsic Actor Capability

Current Effective Capability
    != Retained Individual Capability
    != Joint-System Capability

Environment Effect
    != Environment Selection Effect

Institutional State
    may be part of Environment
    but Rule/Authority/Ownership counterfactuals can require a distinct causal role

Current Performance Change
    != Capability Production

Variance Explained
    != Intervention Effect

Interaction Pattern
    != Identified Interaction Mechanism

Shared Structural Analogy
    != Shared Mechanism
```

Most are already generated by existing Core/World/Human doctrine; CF0 does not promote them again.

---

## 13. What CF0 rejects

1. No `Individual 30% / Environment 70%` universal decomposition.
2. No intrinsic scalar Human/Agent capability score.
3. No `InstitutionQuality` scalar.
4. No complete Environment object/snapshot.
5. No universal persisted `CapabilityField`.
6. No universal `Institution` entity/schema/service.
7. No inference from cross-sectional outcome gaps to intrinsic ability or causal environment effect.
8. No automatic causal credit from temporal sequence.
9. No assumption that better institutions always compress outcome variance; relaxing constraints can expose/amplify actor heterogeneity.
10. No assumption that more support always builds retained individual capability; support can raise joint output while changing internal practice in either direction.
11. No Human↔Agent Harness mechanistic equivalence. Agent systems are controlled structural falsifiers only.
12. No normative “best institution” optimization inside CF0–CF9.

---

## 14. CF1 handoff

CF0 leaves a much smaller question than the raw `10^5–10^6` research geometry:

> **What is the minimum static causal topology needed to distinguish actor state, environment/exposure, institutional rule relations, Resources, Demand, Options, effective Capability and observed Outcome without duplicating current World semantics?**

CF1 must compare:

```text
M0 actor-only
M1 additive context
M2 static interaction
```

and carry transition topology only as a **mechanism decomposition treatment**, not as an independently earned predictive family.

against the frozen discriminator matrix.

M4–M6 should not be activated in CF1 except as explicit counterexamples showing why the static model has a declared scope boundary.

CF1 promotion gate:

- every retained distinction changes at least one frozen prediction/action;
- every new term has a deletion consequence;
- existing `ResourceFor / ActionableResourceFor / Option / Capability / Attribution` semantics are reused where sufficient;
- no persisted schema/service/registry is created;
- institution/environment remain causal roles unless a real owner responsibility proves otherwise.

CF0 therefore closes with a **smaller ontology than the opening intuition**: relational Capability already exists; the likely new research burden is not capability representation but **causal identification across exposure, rules, history and selection**.
