---
schema_version: 1
id: world.resource-ontology-r2-definition-falsification
title: Resource Ontology R2 — Competing Definition Falsification
profile: research
lifecycle: active
source_role: research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - researcher
  - agent
updated: 2026-08-15
summary: Four competing Resource definitions and one falsifier-derived minimal hybrid are tested against all 48 R0 episodes, 20 adversarial boundary cases, ten post-freeze fresh falsifiers and coordinate deletion tests without promoting production doctrine.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-ontology-r0-census
  - world.resource-ontology-r1-theory-triangulation
  - world.resource-option-capability-model
---
# Resource Ontology R2 — Competing Definition Falsification

## 1. Question

R0 established the empirical case base. R1 established competing theoretical pressures and left one central contradiction unresolved:

> Must `Resource` itself be demand-scoped and relational, or can Resource exist more broadly before a concrete workload becomes an Option?

R2 attacks this directly.

The objective is **not** to maximize definition coverage. A definition can pass many cases because it is vacuous. R2 therefore combines:

1. full 48-case historical classification;
2. adversarial boundary cases;
3. explicit PASS / FAIL / AMBIGUOUS semantics;
4. deletion tests for candidate coordinates;
5. complexity/ontology-debt analysis;
6. fresh falsifiers authored only after any hybrid survivor is frozen.

No result in R2 is a production World law.

---

# 2. Frozen evaluation semantics

For every definition/case pair:

- **PASS** — the frozen wording preserves the case's required distinction without being amended.
- **FAIL** — the case materially misclassifies or contradicts the frozen definition.
- **AMBIGUOUS** — the result depends on a coordinate the definition left materially underspecified.

The numerical PASS count is diagnostic only. It is not a score and does not outweigh semantic failure.

R2's machine-readable matrix is:

```text
evidence/acceptance/resource-ontology-r2-definition-matrix-20260815.json
```

It is bound to the R0 census digest `sha256:572091ddafbd79e6c95d584a16b753ac96b6f94493bbf9721a690aa464b1b3a9` and World base `a2ea5f7527dcfae686600e0a386543bee7f20dc8`.

---

# 3. The four definitions frozen before classification

## A — Broad Potential

> An identifiable aspect of Reality is a Resource when there is credible evidence of a non-negligible feasible path by which it could contribute to at least one bounded future state transition inside the relevant system boundary. Current possessed authority, current workload and immediate access are downstream Actionability/Option conditions.

A intentionally keeps current authority/workload downstream. Its primary risk is vacuity: if “credible feasible potential” has no independent content, almost all Reality can become Resource.

## B — Current Relational Affordance

> A Resource exists only as a current relation between a specific actor/system boundary with presently possessed abilities/authority and a Reality feature that affords a class of state transitions. No current workload is required, but the enabling relation must exist now.

B is the strongest interpretation of R0 relationality. It intentionally requires the enabling relation now, so failures cannot later be excused by adding deferred acquisition.

## C — Conversion-Theoretic

> Given an explicit transformation regime and composition rules, a Resource is a nontrivial element whose presence changes the reachable convertibility/composition preorder under the transformations admitted by that regime.

C is the strongest transport from formal resource theory. Its main risk is regime elasticity: if the transformation regime can be chosen after seeing the case, C becomes unfalsifiable.

## D — Option-Set

> Relative to a specific actor/system boundary and authority/cost/risk constraints, a Resource is anything whose presence credibly enlarges that actor’s reachable future option set.

D directly makes Resource depend on future choices. Its main risks are circularity with World's existing `Resource → Option` chain and portfolio-marginal identity drift.

---

# 4. First-pass result across 48 historical + 20 adversarial cases

| Definition | PASS | FAIL | AMBIGUOUS |
| --- | ---: | ---: | ---: |
| A — Broad Potential | 61 | 5 | 2 |
| B — Current Relational Affordance | 51 | 14 | 3 |
| C — Conversion-Theoretic | 46 | 4 | 18 |
| D — Option-Set | 49 | 13 | 6 |

These counts do **not** select A. They expose different failure surfaces.

## 4.1 A's failure surface — breadth without actor/direction

A survives 61/68 first-pass cases, but that success is suspiciously broad.

Its decisive attacks are:

- `X18`: hostile capability changes possible states but is controlled by an adversary, exposing **resource-for-whom**;
- `H01`: a generic resource category can lose explanatory compression;
- `X09`: technical debt changes the future but should not become a positive Resource merely because it participates causally;
- `X16/X17`: logical possible use without a credible bounded path must remain outside Resource.

A's core intuition survives, but not its actor-light wording.

## 4.2 B's failure surface — Resource collapses toward Actionable Resource

B's failures cluster strongly around missing **current** authority/capacity:

```text
W02 / W03 / W04
N03 / N04
F02
S05 / S06
X01
```

These are not random counterexamples. They are exactly the cases where Ordivon needs to represent a verified, valuable or option-bearing external resource **before** current consuming authority exists.

Therefore B's relationality is useful, but the word `current` is placed too early.

If B is retained unchanged, the model must invent another category to hold all deferred/gated resources. That duplicates the existing Candidate/Actionable split rather than explaining it.

## 4.3 C's failure surface — conversion algebra is strong, ontology is regime-relative

C has relatively few direct FAILs but 18 first-pass ambiguities.

Typical question:

```text
Is the missing credential an unavailable Resource,
or simply outside this transformation regime?

Does HTTP error production count as a nontrivial conversion,
or is semantic usefulness part of the regime?

Does a shared failure domain make two paths equivalent,
or does the regime distinguish physical failure state?
```

If `regime` is authored after the answer is known, C can explain almost anything. That makes C highly useful for **R5 composition/convertibility**, but insufficient as World's standalone Resource noun.

Two stronger failures remain:

- `W06`: a nontrivial mechanical conversion can exist despite zero semantic utility;
- `X09`: a harmful constraint can change the conversion preorder without becoming a positive Resource.

## 4.4 D's failure surface — option circularity and portfolio-dependent identity

D fails cases such as:

```text
N01 / X06   correlated duplicate resources
S07         available but dominated tool
G05         similar but still real content resource
Q05         mature tool with negative marginal acquisition value
```

The problem is structural. If Resource exists only when it **adds** an Option, then a resource can cease being a Resource merely because another substitute appears.

```text
one VPN path       → Resource
add equivalent path
first path now adds no marginal option
→ did the first path stop being a Resource?
```

That is a poor identity law.

`X13` exposes the second problem: a contractual option/right is itself a plausible resource. D then approaches:

```text
Resource = whatever adds Options
Option right = Resource
Resource → Option → Resource
```

Option-set enlargement is therefore better treated as a **derived value/optionality relation**, not the definition of Resource itself.

---

# 5. Complete 48-case historical matrix

Reason codes identify the primary discriminator; full case facts remain frozen in R0.

| ID | Case | A | B | C | D | E | Pressure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F01 | SEC EDGAR public data | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-AUTH` | public information resource != unrestricted use != effect authority |
| F02 | FRED high-value but gated | PASS `A-POT` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | known high-value resource != actionable resource |
| F03 | Source bytes versus research evidence | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-KNOW` | observation bytes != research-grade evidence |
| F04 | Large resource universe collapses through research | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-SEM` | information abundance != hypothesis quality != capital capability; null outcomes are knowledge |
| F05 | Workstation egress as Finance resource | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | lower-layer capability becomes a higher-layer resource; implementation should sink below consumer |
| G01 | CC0 catalog still needs exact asset identity | PASS `A-POT` | AMBIG `B-NOAUTH` | AMBIG `C-REGIME` | AMBIG `D-ACQUIRE` | PASS `E-CAND` | source/catalog label != exact resource authority/license |
| G02 | Freesound is not one legal resource class | PASS `A-POT` | PASS `B-REL` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-AUTH` | shared source != homogeneous resource semantics |
| G03 | Live Agent cognition is operational but value-unproven | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-SEM` | expensive capability difference != outcome/value difference |
| G04 | Cheaper fixture remains a meaningful substitute | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-COUNT` | resources can be partially substitutable; marginal value must be measured |
| G05 | Two Scenario Cases did not equal two broad experiences | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-MARGINAL` | PASS `E-COUNT` | resource/content count != diversity of reachable experience states |
| G06 | Existing content levers generated new research archetypes without new core | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-COMP` | complementarity/composition can create capability/option value from existing resources |
| H01 | Generic `resource` role was deleted from Human's minimum model | AMBIG `A-BROAD-RISK` | PASS `B-META` | AMBIG `C-REGIME` | AMBIG `D-CIRCULAR` | PASS `E-REL` | over-broad Resource ontology can reduce explanatory power |
| H02 | The same tool changes role with the question | PASS `A-POT` | PASS `B-META` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-REL` | resource role is relational/question-dependent rather than intrinsic |
| H03 | Model output, joint-system capability and retained Human capability diverge | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | resource-assisted effect != internal capability transfer |
| H04 | Not all generated knowledge should consume Human attention | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-CAP` | attention is scarce conversion capacity; maximum knowledge internalization/utilization is not optimal |
| N01 | 415 Surfshark transport variants | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-MARGINAL` | PASS `E-COUNT` | catalog cardinality != current option count != capability |
| N02 | `native-a` and `native-b` can converge | PASS `A-POT` | PASS `B-REL` | AMBIG `C-REGIME` | AMBIG `D-MARGINAL` | PASS `E-REL` | nominal alternatives != failure-domain-independent redundancy |
| N03 | 98 public VPN candidates versus one admitted root | PASS `A-POT` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | AMBIG `D-ACQUIRE` | PASS `E-CAND` | candidate universe != executable resource stock |
| N04 | Snowflake broker success but no shared capacity | PASS `A-POT` | FAIL `B-NOCAP` | AMBIG `C-REGIME` | FAIL `D-NOOPT` | PASS `E-DEFER` | executable client != available shared resource; capacity is separate |
| N05 | Same public mechanism, different parent relation | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-REL` | actionability is relation/path/context dependent, not intrinsic to the nominal resource |
| N06 | Different roots but shared physical access | PASS `A-POT` | PASS `B-REL` | AMBIG `C-REGIME` | AMBIG `D-MARGINAL` | PASS `E-REL` | diversity has dimensions; redundancy depends on relevant disturbance class |
| N07 | Public observation expansion without capability expansion | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-KNOW` | resource abundance can improve evidence robustness without increasing effect capability |
| N08 | Large public datasets left indexed | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-NONUSE` | acquisition/storage/utilization can be irrational when marginal capability is zero |
| N09 | Historical child resource invalidated by parent change | PASS `A-KNOW` | PASS `B-HIST` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-HIST` | dependency currentness; historical truth survives while current option dies |
| N10 | Failed WARP experiment becomes search memory | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-KNOW` | failed consumption can become Knowledge Resource; retirement can be conditional |
| N11 | Stable consumer resource over replaceable physical members | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | abstraction boundary; stable resource contract can sit over renewable physical options |
| N12 | Installed capability deliberately excluded from ambient authority | PASS `A-POT` | PASS `B-REL` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-AUTH` | possession != ambient authority; retirement depends on dependencies, not age alone |
| Q01 | Public vulnerability intelligence is read-only resource, not exploit authority | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-AUTH` | information resource != action authority |
| Q02 | Provider claim and Security truth remain separate | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-KNOW` | evidence resource has provenance/truth-role; ingestion != belief/knowledge promotion |
| Q03 | Sample metadata/materialization never grants execution authority | PASS `A-POT` | PASS `B-REL` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-AUTH` | possession of dangerous resource != authority to consume it through execution |
| Q04 | Large retained sample need not be duplicated into every research store | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-HIST` | local materialization/storage count != knowledge availability; references can preserve option value |
| Q05 | libvirt was available but intentionally deferred | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-MARGINAL` | PASS `E-NONUSE` | mature available tool can reduce net capability through coordination/authority cost |
| Q06 | Remote entitlement and remote capability are different resources | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | authority carrier != capability location; superficially similar resources have different causal roles |
| S01 | REAPER crossed from installed tool to proven production resource | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-SEM` | installation != capability; native editable state + reproducible effect matters |
| S02 | OBS capability without permanent listener | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-NONUSE` | useful capability need not imply permanent utilization/presence; dormant resources can be safer |
| S03 | Blender exit code zero with failed work | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-SEM` | process success != semantic effect; resource consumption needs outcome evidence |
| S04 | One successful equipment encounter produced only provisional medium status | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-SEM` | tool capability != domain mastery/value capability |
| S05 | Figma installed/configured but OAuth consent absent | PASS `A-POT` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | installed/configured != possessed authority != actionable capability |
| S06 | TouchDesigner remains a high-information candidate | PASS `A-NONUSE` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | option value can exist before acquisition; authority is a separate relation |
| S07 | Inkscape deliberately not acquired | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-MARGINAL` | PASS `E-NONUSE` | available resource can have negative/zero marginal acquisition value |
| W01 | Discovery source versus owner truth | PASS `A-POT` | AMBIG `B-NOAUTH` | AMBIG `C-REGIME` | AMBIG `D-ACQUIRE` | PASS `E-CAND` | discovery != authority; candidate != actionable resource |
| W02 | Required authority versus possessed authority | PASS `A-POT` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | requirement != acquisition decision != possession |
| W03 | Parent entitlement unlocks children | PASS `A-POT` | FAIL `B-NOAUTH` | PASS `C-CONV` | PASS `D-ACQUIRE` | PASS `E-COMP` | prerequisite resource; complementarity; human-work compression |
| W04 | Provider-specific acquisition failure | PASS `A-KNOW` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | FAIL `D-NOOPT` | PASS `E-KNOW` | acquirable-in-theory != eligible-now; negative evidence; non-generalization |
| W05 | Signup transport versus resource value | PASS `A-POT` | PASS `B-REL` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | access relation is time/path scoped; discovery/acquisition and machine consumption are different stages |
| W06 | HTTP success versus semantic utility | PASS `A-POT` | PASS `B-REL` | FAIL `C-SEM` | PASS `D-SEM` | PASS `E-SEM` | reachable != useful; resource value is consumer-relative |
| W07 | Historical admission versus current presence | PASS `A-KNOW` | AMBIG `B-HIST` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-HIST` | historical evidence != current resource state; persistence has multiple meanings |
| W08 | Capability becomes a higher-layer resource | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | Resource/Capability role is system-boundary relative |

---

# 6. First adversarial boundary set

The 20 boundary cases were frozen before the fifth definition was authored.

| ID | Case | A | B | C | D | E | Pressure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| X01 | Official high-value API is known and documented, but the actor has no current credential. | PASS `A-POT` | FAIL `B-NOAUTH` | AMBIG `C-REGIME` | PASS `D-ACQUIRE` | PASS `E-DEFER` | pre-authority potential |
| X02 | A credential that used to work has expired and cannot authenticate; renewal is a separate process. | FAIL `A-CRED-FAIL` | FAIL `B-NOREL` | FAIL `C-NOOBJ` | FAIL `D-NOOPT` | PASS `E-STALE` | stale artifact |
| X03 | A public mechanism-rich research paper is accessible, but there is no current project asking for it. | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-KNOW` | general-purpose information before demand |
| X04 | A private dataset is only rumored to exist; there is no inspectable provenance, owner confirmation or access path. | FAIL `A-CRED-FAIL` | FAIL `B-NOREL` | FAIL `C-NOOBJ` | FAIL `D-NOOPT` | PASS `E-CRED` | logical possibility without credible evidence |
| X05 | A healthy owned GPU is powered off and idle; no current workload needs it. | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-NONUSE` | dormant general-purpose compute |
| X06 | There are 415 nominal transport variants whose relevant outage mode is the same physical access/provider domain. | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-MARGINAL` | PASS `E-COUNT` | correlated abundance |
| X07 | One hour of current Human attention is available. | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-CAP` | scarce flow/budget resource |
| X08 | A trusted collaborator relationship/reputation reliably enables introductions and review, but is not an owned object. | PASS `A-POT` | PASS `B-REL` | AMBIG `C-REGIME` | PASS `D-OPT` | PASS `E-REL` | social/institutional relation |
| X09 | A legacy dependency creates recurring failures and maintenance burden; its presence shrinks feasible safe changes. | FAIL `A-LIAB` | FAIL `B-NOREL` | FAIL `C-DIRECTION` | FAIL `D-LIAB` | PASS `E-LIAB` | liability / negative contribution |
| X10 | A malware sample is locally materialized; static analysis is authorized but execution is not. | PASS `A-POT` | PASS `B-REL` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-AUTH` | same object, bounded authority by transition class |
| X11 | A model API is operational and changes actions, but no consuming domain has shown better Outcome. | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-SEM` | Capability input without value proof |
| X12 | A valid legal/license permission exists, but the corresponding tool/data bytes are not currently present. | PASS `A-POT` | PASS `B-REL` | PASS `C-REGIME` | PASS `D-OPT` | PASS `E-AUTH` | institutional authority as enabling relation |
| X13 | An explicit contractual option/right can be exercised later before expiry but is currently unexercised. | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | FAIL `D-CIRCULAR` | PASS `E-NONUSE` | Option as candidate Resource |
| X14 | A failed experiment leaves exact negative evidence and a reconsideration trigger. | PASS `A-KNOW` | PASS `B-REL` | PASS `C-CONV` | PASS `D-HIST` | PASS `E-KNOW` | Knowledge from failed consumption |
| X15 | A lower owner exports a stable bounded Capability that a higher owner can consume without knowing its mechanism. | PASS `A-BOUND` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-BOUND` | Capability-as-Resource recursion |
| X16 | An arbitrary pebble on the desk has no known Ordivon use or plausible bounded transition mechanism. | FAIL `A-CRED-FAIL` | FAIL `B-NOREL` | AMBIG `C-REGIME` | FAIL `D-NOOPT` | PASS `E-CRED` | everything-is-a-resource attack |
| X17 | A distant asteroid contains useful minerals in principle, but Ordivon has no plausible bounded acquisition path or horizon. | FAIL `A-CRED-FAIL` | FAIL `B-NOREL` | AMBIG `C-REGIME` | FAIL `D-NOOPT` | PASS `E-CRED` | theoretical usefulness without feasible path |
| X18 | A hostile botnet capability is controlled by an adversary; it can change Ordivon states only against the owner’s interests. | AMBIG `A-ACTOR-GAP` | PASS `B-REL` | AMBIG `C-DIRECTION` | PASS `D-LIAB` | PASS `E-HAZARD` | actor/control/directionality attack |
| X19 | An unrestricted cash reserve is idle and can be allocated later across multiple domains. | PASS `A-NONUSE` | PASS `B-REL` | PASS `C-CONV` | PASS `D-OPT` | PASS `E-NONUSE` | rival stock with option value |
| X20 | Open-source tool code is available but incompatible with the current stack; adaptation is feasible with bounded work. | PASS `A-POT` | PASS `B-REL` | PASS `C-CONV` | PASS `D-ACQUIRE` | PASS `E-DEFER` | conversion cost before actionability |

---

# 7. Why a fifth definition is admissible

R2 allows a hybrid only **after** A–D are exposed to the same test set.

The observed correction is small and specific:

- A does not need current workload/current authority;
- A **does** need actor/system boundary and directionality;
- B proves actor-relative relation matters but puts currentness too early;
- C proves an evidenced conversion mechanism matters but a full arbitrary regime is too elastic;
- D proves future-option effect matters for valuation but should not define identity.

Therefore the fifth candidate adds only coordinates independently demanded by falsifiers.

---

# 8. E — Evidenced Enrollable Potential

E is frozen as:

> **Relative to a declared actor/system boundary, a Resource is an identifiable aspect of Reality for which sufficient current evidence supports that the actor can intentionally enroll it, either now or through a bounded feasible acquisition/conversion path, as a means, input, or enabling relation for at least one admissible class of future state transitions. A current workload, current access, and possessed authority for the eventual consuming action are not required; those belong to downstream Actionable Resource/Option qualification. A mere target of action, hazard, rumor, stale artifact, or logically possible but unbounded distant usefulness is not sufficient.**

The compact form is:

```text
Resource(actor/system)
=
an identifiable aspect of Reality
+
current evidence
+
a credible transition mechanism
+
bounded feasible enrollment/acquisition/conversion
+
intentional owner-admissible direction
```

while explicitly **not requiring**:

```text
current concrete workload
current materialization/access
already-possessed consuming authority
proven consumer Outcome/value
```

This resolves R1 C2 provisionally:

> **Resource is actor/system-relative, but not necessarily current-demand-relative.**

It is neither intrinsic object ontology nor current-Goal affordance ontology.

---

# 9. E and the Candidate / Actionable / Option boundary

R2's most useful compression is not a larger lifecycle. It is a separation of epistemic and operational roles.

## 9.1 Resource Candidate is an epistemic hypothesis

A **Resource Candidate** should not mean “a weak Resource”.

It means:

> a claim/observation that some identifiable aspect of Reality may satisfy E, but the evidence needed to establish that relation is incomplete.

Examples:

- aggregator listing before owner verification (`W01`);
- exact game asset before exact license truth (`G01`);
- unqualified public VPN row (`N03`);
- rumored dataset (`X04`) — a particularly weak candidate that may be rejected immediately.

This keeps Candidate in the epistemic plane rather than inventing `Potential Resource`, `Proto Resource`, `Latent Resource`, etc.

## 9.2 Resource

Once E is established, the Resource may still be inaccessible or gated now.

Examples:

- FRED before a user-held key, when a bounded legitimate acquisition path exists (`F02`);
- TouchDesigner before account/license acquisition (`S06`);
- an idle GPU with no current workload (`X05`);
- an expiring contractual right that remains exercisable (`X13`).

## 9.3 Actionable Resource

Actionability adds current demand-specific evidence such as:

```text
owner truth / terms
possessed authority
current access / transport
current capacity
semantic interface
workload fit
freshness where material
```

This preserves the strongest R0/R1 relational finding without forcing all those coordinates into Resource existence.

## 9.4 Option

An Option is then a **demand-scoped admissible use/composition** available to selection from current Actionable Resources and other current conditions.

This avoids defining Resource in terms of the Option set that Resource later helps construct.

Provisional layering:

```text
Observation / Claim
      ↓ evidence
Resource Candidate       # epistemic hypothesis, not weaker ontology
      ↓ E established
Resource                 # actor-relative evidenced enrollable potential
      ↓ current qualification for a demand
Actionable Resource
      ↓ demand-scoped admissible use/composition
Option
      ↓ selection / composition
Capability
```

---

# 10. E deletion tests

E is only useful if its coordinates survive deletion.

| Coordinate | Counterfactual deletion/addition | Discriminators | Result | Why |
| --- | --- | --- | --- | --- |
| actor/system boundary | Remove actor/system boundary and ask only whether the aspect can contribute to some transition somewhere. | X18, X21, H02 | **REQUIRED** | Without the actor/boundary coordinate, adversary-controlled capability and out-of-boundary utility become indistinguishable from resources available to Ordivon. |
| current evidence / credibility | Replace sufficient current evidence with mere logical possibility. | X04, X16 | **REQUIRED** | Rumored datasets and arbitrary objects become Resources merely because an imaginable use can be invented. |
| bounded feasible acquisition/conversion path | Permit any theoretically possible future conversion regardless of horizon/cost/prerequisites. | X17, X26, X29, X30 | **REQUIRED** | Irretrievable, temporally impossible and economically unreachable objects collapse into the same class as realistic deferred resources. |
| intentional enrollability / directionality | Count anything that changes reachable states, including hazards and burdens. | X09, X18, X25 | **REQUIRED** | Liabilities, hostile capabilities and known-degrading inputs become positive Resources rather than constraints/hazards. |
| identifiable aspect of Reality | Allow vague source/category claims without identifying what object/relation the evidence is about. | W01, G01, G02, X04 | **REQUIRED** | Catalog-level claims silently transfer authority/license/currentness to heterogeneous underlying items. |
| class of future state transitions / mechanism | Remove the requirement for an evidenced transition class or mechanism. | X16, H01 | **REQUIRED** | Resource becomes an uninformative synonym for background Reality. |
| current workload / concrete goal | Require an active workload or current concrete goal for Resource existence. | S06, X03, X05, X13, X19 | **REJECT_ADD** | Dormant general-purpose resources and option-bearing rights lose Resource status despite credible bounded future use. |
| current access | Require immediate current access/materialization. | F02, S06, Q04, X01, X12 | **REJECT_ADD** | Gated but credibly acquirable resources, references and enabling rights are confused with non-resources. |
| possessed consuming authority | Require the authority needed for eventual consumption to already be possessed. | W02, F02, S05, S06, X01 | **REJECT_ADD** | Resource collapses toward Actionable Resource and cannot represent acquisition optionality. |
| proven consumer Outcome/value | Require evidence that use improves the final domain Outcome before something qualifies as Resource. | G03, S04, X11 | **REJECT_ADD** | Inputs with real transition potential are confused with proven value; Resource would collapse toward validated Capability/Outcome. |
| global scalar value | Require every Resource to have one total-order scalar value. | S07, Q05, N07, X08 | **REJECT_ADD** | Context-dependent, incomparable and option-bearing resources cannot be truthfully totally ordered. |


## 10.1 Coordinates that are actually required

The deletion tests retain six pieces:

```text
actor/system boundary
identifiable Reality aspect
current evidence / credibility
bounded feasible path
transition class / mechanism
intentional enrollability / directionality
```

They are not equivalent:

- actor boundary separates resource from adversary-owned hazard;
- identity/provenance separates an exact resource claim from a heterogeneous catalog label;
- evidence prevents pure imagination from creating Resources;
- bounded feasibility excludes inaccessible-in-practice theoretical utility;
- mechanism prevents all background Reality becoming Resource;
- directionality separates means/enabling relation from liability/target/hazard.

## 10.2 Coordinates that should **not** be added to Resource existence

The deletion/addition tests reject requiring:

```text
current workload
current access
currently possessed consuming authority
proven final Outcome
one global scalar value
```

These belong downstream or in decision-local valuation.

This is the main R2 compression result.

---

# 11. Fresh post-freeze falsifiers for E

To reduce obvious overfitting, E was frozen **before** a second set of ten falsifiers was authored.

| ID | Case | E | Pressure |
| --- | --- | --- | --- |
| X21 | GPU waste heat can warm a room, but room heating is outside the declared Ordivon system boundary. | PASS `E-BOUND` | boundary-relative relevance |
| X22 | A stolen third-party credential technically works but its use is not owner-authorized or legally admissible. | PASS `E-AUTH` | technical feasibility without admissibility |
| X23 | A free API is reachable now, but provider terms prohibit the intended commercial transition while permitting unrelated personal use. | PASS `E-AUTH` | transition-class-specific permission |
| X24 | A dataset is ten years stale: valid for historical analysis but invalid for a current-state claim. | PASS `E-HIST` | resource existence versus claim-specific actionability/currentness |
| X25 | A random data corpus is accessible and can mechanically enter model training, but there is no evidence it helps any admissible capability and known tests show degradation. | PASS `E-LIAB` | mechanical input versus evidenced directional contribution |
| X26 | An encrypted backup exists, but its key is irretrievably lost and no bounded recovery path is known. | PASS `E-CRED` | identified object without feasible conversion path |
| X27 | A formerly learned Human skill has decayed below current usable proficiency, but retained priors make bounded refresh materially cheaper than learning from zero. | PASS `E-DEFER` | latent reacquisition advantage versus current capability |
| X28 | A component has no standalone use and only becomes useful with a complement that is not held but is cheaply and credibly acquirable. | PASS `E-COMP` | complementarity before current bundle possession |
| X29 | A theoretically useful external asset is purchasable only at a cost beyond every bounded Ordivon resource envelope. | PASS `E-CRED` | technical market availability without bounded feasibility |
| X30 | A formal option exists but will expire before the actor can satisfy its prerequisites, making exercise infeasible in time. | PASS `E-STALE` | nominal right without bounded temporal exercise path |

E survives all ten without changing wording.

The important cases include:

- `X21`: usefulness outside the declared system boundary does not create an Ordivon Resource;
- `X22`: stolen credentials are technically effective but not owner-admissible resources;
- `X24`: stale data can remain a Resource for historical analysis while failing current claim actionability;
- `X25`: mechanically trainable but known-degrading data does not qualify merely because it can enter a pipeline;
- `X27`: decayed skill can leave a real bounded reacquisition advantage without pretending current proficiency exists;
- `X28`: complementarity can support Resource status before the complete bundle is currently held;
- `X30`: a nominal option that cannot be exercised before expiry fails bounded feasibility.

This is evidence for E, not proof of universality.

---

# 12. Resource is a role/relation, not an intrinsic substance

E changes how the word should be interpreted.

The same underlying entity can expose different aspects/relations:

```text
malware sample bytes
├─ Resource for authorized static analysis
└─ not authorized execution Resource

hostile botnet
├─ Resource for its controller/adversary
├─ Hazard / disturbance to Ordivon
└─ observed telemetry about it may become Ordivon Evidence Resource

legacy codebase
├─ software Resource
└─ technical-debt relation may simultaneously be Liability
```

Therefore `Resource` is not a metaphysical type attached permanently to an object.

It is a **World role grounded in an actor/system-relative relation to an identifiable aspect of Reality**.

This does not require a global Resource registry; the role can be projected demand-locally from owner-native facts.

---

# 13. What happened to R1's four families

## A — survives as the base intuition, but not unchanged

A was closest to the survivor. Its `credible bounded potential` survives, but actor/boundary/directionality are required. E is therefore not “A wins”; it is **A after its actual falsifiers are repaired with the smallest proven additions**.

## B — moves downstream into Actionability

B's relation/currentness structure is valuable, but `presently possessed authority` is too strong for Resource existence.

The strongest part of B becomes:

```text
Actionable Resource
=
Resource
+ current actor relation
+ current authority/access/fit/capacity
```

## C — retained for R5 conversion/composition research

C's convertibility preorder and composition structure remain highly valuable, especially for:

```text
substitution
complementarity
catalysts / prerequisites
bundles
partial order / incomparability
```

But C does not independently settle authority, semantic direction or regime choice.

## D — retained as optionality / marginal-value reasoning

D is useful for asking:

```text
How much does this Resource expand current/future choice?
Does another substitute make its marginal value small?
What option value is lost by consuming it now?
```

But it should not decide whether the underlying thing is a Resource.

---

# 14. R2 findings about authority

R2 makes one subtle distinction clearer.

### Current consuming authority is not required for Resource existence

Otherwise `F02`, `S05`, `S06`, `X01` disappear into a separate ontology despite having bounded legitimate acquisition paths.

### But admissibility still matters

`X22` demonstrates why technical feasibility is insufficient. A stolen credential is not made an Ordivon Resource simply because it works.

So E needs:

```text
credible owner-admissible enrollment path
```

not:

```text
already possess every authority needed for final consumption
```

This is compatible with current World law:

```text
Resource
!= Actionable Resource
```

and should not be interpreted as minting authority from future intention.

---

# 15. R2 findings about currentness

R2 rejects one universal Resource-current bit.

A Resource relation can remain established while one actionability coordinate goes stale:

```text
stale historical dataset
→ still Resource for historical analysis
→ not Actionable for current-state claim

expired credential
→ credential itself no longer Resource for authentication
→ account/renewal path may remain a separate Resource

historical transfer receipt
→ Evidence Resource for past admission
→ does not prove current native bytes
```

Currentness therefore attaches to **claims/relations/uses**, not to a monolithic Resource object.

R3 must model this carefully without introducing a global freshness service.

---

# 16. R2 findings about liabilities and negative resources

R2 does **not** adopt `negative Resource` as a root concept.

`X09`, `X18`, `X25` show why direction matters. A thing that shrinks safe options, creates burden or acts against the owner is better modeled as:

```text
Constraint
Liability
Hazard / Disturbance
Cost / Dependency
```

The same underlying object may also expose a separate Resource aspect.

Example:

```text
technical debt
= Liability relation

knowledge of the debt + exact reproducer
= Evidence/Knowledge Resource
```

Calling both “positive and negative Resources” would save vocabulary at the cost of losing causal direction.

R2 therefore rejects negative-Resource unification for now.

---

# 17. R2 findings about Resource Candidate

R2 does **not** justify three nouns:

```text
Potential Resource
Resource Candidate
Resource
```

`Potential Resource` is redundant with E's own future-potential semantics.

The minimal distinction is:

```text
Resource Candidate  = epistemic claim not yet established
Resource            = established E relation
```

Candidate can later resolve to:

```text
Resource
Rejected / non-resource
Expired / no longer feasible
Different resource than originally believed
```

This is cleaner than treating Candidate as the first persisted state in a universal resource lifecycle.

---

# 18. R2 findings about identity and marginal value

Resource identity should not be destroyed merely because a substitute appears.

This is the major lesson from D.

```text
Resource existence
!= marginal contribution to current portfolio
```

Thus 415 correlated paths can remain 415 identified Resources/candidates while:

```text
effective redundancy ≈ 1 failure domain
marginal value of path 416 ≈ 0
```

Likewise Inkscape can remain a real available Resource while rational acquisition value is near zero.

Therefore:

```text
Resource
→ later derive substitutability / redundancy / marginal value / Option contribution
```

not the reverse.

---

# 19. R2 provisional Resource definition

R2's provisional survivor is E:

> **Relative to a declared actor/system boundary, a Resource is an identifiable aspect of Reality for which sufficient current evidence supports that the actor can intentionally enroll it, either now or through a bounded feasible acquisition/conversion path, as a means, input, or enabling relation for at least one admissible class of future state transitions.**

And explicitly:

> **A Resource does not need to be currently demanded, immediately accessible, already authorized for final consumption, scarce, unique, valuable on one global scale, or proven to improve final Outcome.**

The definition's compact conceptual coordinates are:

```text
Resource
=
Actor/System-relative
× Identifiable Reality Aspect
× Evidence
× Enrollable Direction
× Transition Mechanism
× Bounded Feasibility
```

This is a reasoning model, **not** a persisted schema and **not** a scalar product.

---

# 20. What R2 has and has not resolved

## Resolved provisionally enough to enter R3

1. Resource is **not object-intrinsic**.
2. Resource is **actor/system-relative**.
3. Resource does **not require a current concrete workload**.
4. Resource does **not require current consuming authority/access**.
5. Resource requires evidence stronger than logical possibility.
6. Resource requires a bounded plausible transition/enrollment mechanism.
7. Resource is directional; liabilities/hazards are not automatically negative Resources.
8. Resource identity is separate from marginal portfolio value.
9. Candidate is epistemic, not a weaker ontological Resource state.
10. Actionable Resource is where current relation/authority/access/fit should concentrate.

## Still unresolved

1. exact minimum evidence strength for E — R3 should seek coordinates, not a universal confidence score;
2. how social rights/reputation/relationships are identified without reifying them as owned objects;
3. how resource capacity/stock/flow/budget differ;
4. how dependencies and complementarity affect bounded feasibility;
5. how Resource relations decay and renew;
6. how E interacts with nested owner/system boundaries;
7. how Actionable Resource is projected for different claim types without a universal lifecycle;
8. whether `admissible transition class` belongs in World or should be owner-projected from authority/purpose facts;
9. how Knowledge/Capability recursively become Resources while preserving native ownership;
10. Effect/Outcome/Attribution remains R6 work.

---

# 21. R3 handoff

R2 does **not** authorize updating canonical `resource-option-capability-model.md` yet.

It authorizes R3 to ask:

> What is the **smallest relation model** needed to establish/project E and Actionable Resource across the actual R0 cases?

R3 should begin with candidate coordinates suggested by R2:

```text
actor / system boundary
resource aspect identity
source / provenance
owner
admissible purpose / authority relation
acquisition/enrollment path
access / transport
capacity
transition/interface mechanism
currentness / expiry
cost / risk
complement dependencies
failure domain
substitutability
```

but must delete aggressively.

The fact that E uses six conceptual coordinates does **not** mean World needs six persisted fields.

R3 must preserve the existing rule:

> relation evidence should remain owner-native and demand-scoped wherever possible; no global Resource registry is implied.

---

# 22. R2 conclusion

R2 resolves the central R1 contradiction more narrowly than either side originally proposed.

The evidence does **not** support:

```text
Resource = useful object
Resource = currently usable affordance
Resource = anything convertible
Resource = whatever adds an Option
```

The current best surviving model is:

```text
Reality
   ↓ identify + evidence
Resource Candidate?          # epistemic only when evidence incomplete
   ↓ establish actor-relative enrollable potential
Resource
   ↓ current owner truth + authority + access + fit + capacity
Actionable Resource
   ↓ demand-scoped admissible use/composition
Option
   ↓ selection + composition
Capability
```

The conceptual correction is:

> **Resource is relational enough to answer “resource for whom?”, but broad enough to exist before “what exact workload today?”.**

That is the R2 result carried into R3. It remains a provisional research claim until relation modeling and later cross-domain dogfood survive.
