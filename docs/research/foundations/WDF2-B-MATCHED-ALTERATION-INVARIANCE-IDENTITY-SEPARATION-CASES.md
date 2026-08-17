# WDF2-B — Matched Alteration / Invariance / Identity Separation Cases

Status: **complete for WDF2-B**. WDF0 Meta-Foundation v1 and WDF1 Modal Foundation v1 remain frozen. WDF2-A remains closed. No FoundationReopenCondition fires. No production engineering change is admitted.

Exact next round derived from the residuals of this case suite:

```text
WDF2-C — Counterfactual Alternative Generation / Selection Architectures
```

Canonical numbering remains exactly `WDF<number>-<letter>`.

---

# 1. Objective

WDF2-A showed that `counterfactual` is not one primitive operation. It exposed a semantics-neutral diagnostic signature:

```text
Anchor
+ AntecedentAlteration
+ Target/Consequent
+ PreservationProfile
+ AlternativeGeneratorOrSelector
+ ModalForce
+ Identity/CorrespondenceCriterion
+ TruthRole/ModelProvenance
+ Probability/CouplingRole when relevant
```

WDF2-B now attacks that decomposition with **matched cases**.

The method is deliberately stricter than collecting colorful examples. Each family holds most coordinates constant and changes one coordinate at a time. A candidate counterfactual architecture fails if it cannot represent the difference without changing the meaning of some hidden parameter.

The aim is not yet to decide whether Lewis, Stalnaker, SCM/Pearl, premise semantics, backtracking semantics, powers/dispositions, law-relative or plural accounts are correct. The aim is to create a falsifier suite strong enough that those candidates can later be compared fairly.

---

# 2. Matched-case protocol

Each case is normalized to:

```text
CF = <Anchor, Alteration, Preservation, Correspondence, Selection, Evaluation>
```

with optional:

```text
ProbabilityCoupling
BacktrackingPolicy
Normality/Default
TruthRole
Scale/Grain
```

A pair/triple is considered a valid matched discriminator only when:

1. the surface question remains as similar as possible;
2. exactly one intended coordinate changes, or the dependency between two coordinates is itself the target;
3. a real difference in verdict, interpretation or admissibility follows;
4. the difference cannot be eliminated merely by renaming variables;
5. no WDF0/WDF1 firewall is violated to manufacture the case.

The suite therefore tests **semantic structure**, not linguistic intuitions alone.

---

# 3. Master result before details

Across the suite, four conclusions appear repeatedly:

```text
1. Alteration locus and preservation profile are coupled, not freely independent.
2. Identity/correspondence can change the truth conditions even when alteration and preservation are fixed.
3. A valid counterfactual may have multiple admissible/relevant alternatives; uniqueness cannot be universalized.
4. Population/interventional marginals do not determine token counterfactuals without an across-alternative coupling.
```

The largest remaining residual after WDF2-B is therefore:

> **Given a typed alteration, preservation profile and correspondence criterion, how should the relevant alternative set be generated, ordered, selected, tied, weighted or left plural?**

That is the exact admission basis for WDF2-C.

---

# PART I — ALTERATION MATCHED CASES

# 4. A-family — same target, different alteration locus

## A1 — physical value change

Anchor:

```text
mass m
initial velocity v
fixed dynamics D
fixed boundary B
```

Query:

```text
If initial velocity had been v', where would the projectile land?
```

Intended alteration:

```text
v := v'
```

Intended preservation:

```text
D fixed
B fixed
object correspondence fixed
```

This is the cleanest value/state case.

---

## A2 — same surface variable, mechanism replacement

Anchor is identical to A1.

Query:

```text
If the velocity-setting mechanism had produced v' under a different calibration rule, where would the projectile land?
```

The realized value `v'` matches A1, but the alteration is now:

```text
F_v -> F'_v
```

rather than direct value replacement.

Why the difference matters:

- upstream causes may differ;
- neighboring contexts may differ;
- policy/mechanism robustness claims differ;
- backtracking accommodation differs;
- attribution differs.

### Falsifier A-F1

Any architecture that identifies counterfactuals solely by the resulting antecedent value fails A1/A2.

```text
SameAntecedentValue != SameAlterationSemantics
```

---

## A3 — same action token, different policy

Anchor:

```text
Agent policy π
state s
π(s)=a
```

Pair:

```text
A3a: If the Agent had taken a' at s, what would follow?
A3b: If the Agent had used policy π' where π'(s)=a', what would follow?
```

At the first step both produce `a'`.

But later states can diverge because:

```text
one-token override != policy replacement
```

### Falsifier A-F2

A counterfactual language that represents only action values but not action-generation/policy alteration cannot preserve A3a/A3b.

---

## A4 — software input vs code patch

Anchor:

```text
program P version V
input x
runtime R
```

Pair:

```text
A4a: same P,V,R; input x -> x'
A4b: same x,R; implementation V -> V'
```

Both may produce the same output on one input while differing on neighboring inputs.

Therefore observational equality on the target token does not collapse the counterfactual distinction.

```text
InputIntervention != ProgramMechanismChange
```

---

## A5 — configuration vs implementation

Pair:

```text
change config flag c
change code so c no longer controls behavior
```

The first preserves the implementation-level mapping and changes one parameter. The second changes the mapping itself.

### Falsifier A-F3

A universal `set variable` semantics survives only if it can type the variable as **object-level value** versus **mechanism-defining parameter** and preserve that distinction under model revision. Merely encoding both as nodes does not solve the semantic problem.

---

## A6 — institutional credential vs rule change

Anchor:

```text
rule set K:
credential C -> authorization A
Actor lacks C
```

Pair:

```text
A6a: Actor has C; K unchanged.
A6b: K changes so C is no longer required; Actor remains without C.
```

Both can yield `authorized=true`.

But they differ in:

- why authorization exists;
- who else becomes authorized;
- what evidence is relevant;
- what remediation is required;
- whether the constitutive rule changed.

### Falsifier A-F4

```text
SameInstitutionalOutcome != SameInstitutionalCounterfactual
```

A semantics that treats `authorization=true` as the complete antecedent alteration loses the distinction.

---

## A7 — rule change vs convention change

Pair:

```text
A7a: institution changes its operative permission rule.
A7b: language/schema renames the status while operative permissions stay the same.
```

Both can change a representation field named `authorization`.

Only A7a changes institutional Reality.

### Falsifier A-F5

```text
Representation/SemanticChange != ConstitutiveRuleChange
```

This directly preserves the WDF0 Reality/model firewall.

---

## A8 — model boundary change vs world change

Pair:

```text
A8a: external service becomes available in Reality.
A8b: same Reality; model boundary is expanded so the already-existing service is represented.
```

Both can make a planning model report a new reachable path.

### Falsifier A-F6

A counterfactual architecture fails if changing the model's represented domain is indistinguishable from changing Reality.

---

# 5. Alteration-family conclusion

The A-family forces a typed `surgery locus`.

Minimum distinction currently required:

```text
value/state
one action token
policy/strategy
mechanism/function
rule/constitution
boundary/interface
representation/model
nomological/semantic convention
```

This does **not** prove these are universal Reality primitives. It proves that counterfactual semantics must not erase their differences when the target query depends on them.

---

# PART II — INVARIANCE MATCHED CASES

# 6. I-family — same antecedent, different preservation profile

## I1 — match striking with oxygen fixed vs not fixed

Anchor:

```text
match unstruck
oxygen present
normal ignition mechanism
```

Surface antecedent:

```text
If the match had been struck ...
```

Pair:

```text
I1a: preserve oxygen/normal background -> ignition.
I1b: add/preserve no-oxygen condition -> no ignition.
```

This is not merely antecedent strengthening. It demonstrates that the preservation/background profile is part of truth conditions.

### Falsifier I-F1

```text
AntecedentSyntaxAloneDoesNotDetermineCounterfactual
```

---

## I2 — server healthy: local override vs repaired history

Anchor:

```text
server unhealthy at t2
cause: failed deployment at t1
```

Same surface query:

```text
If the server had been healthy at t2, would request r have succeeded?
```

Two counterfactual frames:

```text
I2a forward/local:
  override health at t2;
  preserve earlier failure/history as far as possible.

I2b backtracking:
  preserve server mechanisms;
  alter earlier deployment/configuration state so health at t2 arises normally.
```

Downstream side effects may differ because I2b modifies the upstream history.

Recent SCM work explicitly formalizes this contrast: interventionist counterfactuals alter local causal mechanisms while sharing exogenous background; backtracking counterfactuals instead preserve causal laws and alter upstream/exogenous conditions.

### Falsifier I-F2

```text
BacktrackingPolicy is semantically material.
```

No universal forward-only default is earned.

---

## I3 — same price antecedent, market mechanism fixed vs regime changed

Surface query:

```text
If price P had been lower at t ...
```

Frames:

```text
I3a: same market mechanism/order flow regime, local/exogenous shock changes P.
I3b: lower P because exchange rule/market mechanism changed.
```

A strategy's downstream response can differ because liquidity, fees, matching or participant adaptation differ.

### Falsifier I-F3

Price equality does not determine the counterfactual regime.

---

## I4 — same authorization antecedent, rules fixed vs changed

Surface:

```text
If Actor had been authorized ...
```

Frames:

```text
I4a: current rules fixed; Actor credential/status differs.
I4b: Actor facts fixed; authorization rules differ.
```

This repeats A6 from the preservation side and proves alteration/invariance are coupled.

### Strong result

You cannot freely specify:

```text
alter rule K
AND preserve K
```

The preservation profile must be **compatible with the alteration locus**.

---

## I5 — program output under same code vs same specification

Surface:

```text
If output had been y' ...
```

Two preservation choices:

```text
I5a preserve exact implementation/version.
I5b preserve only external specification/contract; implementation may differ.
```

These are different counterfactuals even if the target output is identical.

This shows invariance can be imposed at different abstraction levels.

---

## I6 — same Agent answer with provider seed fixed vs latent behavior fixed

Suppose provider/model M is stochastic.

Query:

```text
If prompt p had contained one extra fact, what would the Agent have answered?
```

Possible preservation policies:

```text
same provider request seed/token RNG state, where meaningful
same latent user/task facts but fresh stochastic draw
same deterministic decoding configuration only
same sampled reasoning trajectory, if such correspondence is even definable
```

These produce different counterfactual distributions.

### Falsifier I-F4

`same randomness` is not a universal invariant. Its meaning is model/provider-specific.

---

# 7. Invariance-family conclusion

The I-family yields a deeper law than WDF2-A's simple `typed preservation` claim:

```text
PreservationProfile must be jointly admissible with AlterationType.
```

So the counterfactual frame is not a Cartesian product where any alteration can combine with any invariant set.

A candidate architecture needs some compatibility relation:

```text
Compatible(Alteration, Preservation, Anchor, Model/Domain)
```

or an equivalent mechanism.

This is a **semantic admissibility condition**, not a claim that Reality contains a `Compatible` primitive.

---

# PART III — IDENTITY / CORRESPONDENCE MATCHED CASES

# 8. X-family — same alteration, different subject tracking

## X1 — software version identity

Anchor:

```text
service S implemented by binary V1
```

Counterfactual:

```text
If implementation were V2 ...
```

Two correspondence criteria:

```text
X1a service identity = continuity of deployment role/API/ownership.
X1b program identity = exact code/version identity.
```

Under X1a, `same service under different implementation` is coherent.
Under X1b, `same program under different code` is false or requires counterpart language.

### Falsifier X-F1

A universal identity criterion fails.

---

## X2 — institution after constitutional change

Anchor:

```text
institution I under charter K
```

Counterfactual:

```text
If charter K had been radically replaced by K' ...
```

Criteria:

```text
organizational continuity
legal continuity
membership continuity
functional continuity
historical lineage
```

Different domains can disagree whether the counterfactual subject remains `the same institution`.

This is not merely epistemic uncertainty; it can be criterion-relative objective disagreement.

---

## X3 — same physical object vs same functional system

A machine's every component is gradually replaced.

Counterfactual query about a future failure can track:

```text
material continuity
causal/process continuity
functional role
serial/legal identity
```

WDF0 already rejected a universal persistence rule. WDF2-B confirms that counterfactual semantics must inherit the relevant criterion rather than manufacture one.

---

## X4 — same person / same decision situation

Suppose a counterfactual alters a person's memories, beliefs or preferences.

At some point the question:

```text
What would this same person have chosen?
```

becomes dependent on the identity/correspondence theory.

A query may still be meaningful through counterpart/tracking rather than strict identity.

### Falsifier X-F2

```text
SameSurfaceName != SufficientCounterfactualCorrespondence
```

---

## X5 — token-level treatment outcome

Question:

```text
For this same patient/unit, what would Y have been under treatment x1 instead of x0?
```

The `same unit` requirement is not just a label. It defines which latent background features are paired across alternatives.

This becomes critical in the probability family below.

---

# 9. Identity-family conclusion

WDF2-B strengthens WDF2-A:

```text
Identity/Correspondence is not always an independent metadata field.
```

For constitutive alterations, the alteration itself may pressure the criterion used to preserve the subject.

Therefore a valid architecture must permit:

```text
strict identity
criterion-relative continuity
counterpart/correspondence
no valid subject-preserving comparison
```

as distinct outcomes.

`No valid correspondence` must remain representable rather than forcing every antecedent into a world containing `the same X`.

---

# PART IV — SELECTION / TIES / NONDETERMINISM

# 10. S-family — same frame, multiple relevant alternatives

## S1 — two equally small upstream repairs

Anchor:

```text
server failure can be prevented by either:
A. rollback deployment
B. restore dependency
```

Surface antecedent:

```text
If the service had been healthy ...
```

Both A and B can be equally minimal under one change metric while producing different side effects.

### Falsifier S-F1

A universal semantics requiring a unique nearest alternative must either:

- justify a tie-breaker;
- admit multiple minima;
- or expose the selection function as additional structure.

Uniqueness is not derivable from the antecedent alone.

---

## S2 — same number of changed facts, different kinds of change

To make `door opens` true:

```text
Alternative A: unlock door.
Alternative B: destroy door.
```

Both may alter one Boolean predicate in a coarse model.

A fine model differentiates:

```text
authorization/security mechanism
physical destruction
```

### Falsifier S-F2

Minimal Hamming distance over a chosen variable vector is not semantics-neutral.

Variable/grain choice can create or destroy ties.

---

## S3 — law violation vs many ordinary fact changes

A classic similarity pressure:

```text
one small law-breaking miracle
vs
large divergence in ordinary history while laws remain intact
```

Different similarity orderings can rank these differently.

The case does not select Lewisian priorities; it proves that `minimal change` requires a priority policy over **types of difference**.

---

## S4 — nondeterministic transition

Anchor model permits:

```text
same state + same action -> outcome y1 or y2
```

Counterfactual:

```text
If action a' were taken ...
```

There may be several admissible outcomes even after alteration and background are fixed.

Recent nondeterministic causal-model work explicitly rejects the assumption that one actual world plus one intervention must determine a unique counterfactual world.

### Falsifier S-F3

```text
CounterfactualAlternativeSet may be plural even after complete declared surgery.
```

---

## S5 — context changes relevance ordering

Question 1:

```text
Would the service have remained available?
```

Question 2:

```text
Would the service have remained compliant?
```

Same antecedent alteration can prioritize different background similarities because availability and compliance care about different mechanisms/rules.

### Falsifier S-F4

```text
Selection relevance can be target/query-sensitive.
```

A single global similarity metric is not earned.

---

# 11. Selection-family conclusion

The S-family creates the largest post-WDF2-B residual.

Even after we know:

```text
what changed
what is preserved
what subject corresponds
```

we still need to know:

```text
which compatible alternatives count?
how are they generated?
is there one, all minima, a ranked set, a measure, or a premise closure?
what happens under ties/non-limit cases?
how does query relevance affect the ordering?
```

This is precisely the territory where Stalnaker-style selection, Lewis-style orderings, premise semantics, structural generation and plural/domain-specific accounts become directly comparable.

---

# PART V — BACKTRACKING MATCHED CASES

# 12. B-family — forward surgery vs upstream accommodation

## B1 — alarm state

Anchor:

```text
smoke -> alarm
smoke present
alarm sounds
```

Counterfactual:

```text
If alarm had not sounded ...
```

Forward/local frame:

```text
break/override alarm mechanism/output
smoke remains
```

Backtracking frame:

```text
infer a world with no smoke or altered upstream condition
alarm mechanism remains intact
```

Consequent:

```text
Would there still have been smoke?
```

Verdicts can reverse.

### Falsifier B-F1

Backtracking is not stylistic. It changes substantive counterfactual consequences.

---

## B2 — failed API request

Anchor:

```text
credential invalid -> request rejected
```

Counterfactual:

```text
If request had succeeded ...
```

Frames:

```text
local override of response/result
vs
backtrack to valid credential / different authority state
```

Downstream authorization claims differ sharply.

This matters for Ordivon because an observed successful effect is not equivalent to a valid authorized path.

---

## B3 — Agent answer

Anchor:

```text
context omitted fact f
Agent answered y
```

Counterfactual:

```text
If Agent had answered y' ...
```

Local frame:

```text
force output y'
```

Backtracking frame:

```text
alter context/model/latent reasoning antecedents that could naturally produce y'
```

The first is useful for downstream consequence analysis; the second for explanation/diagnosis.

### Strong result

Counterfactual purpose can determine whether backtracking is admissible:

```text
consequence-of-output query
!=
why-could-output-have-differed query
```

---

# PART VI — PROBABILITY / COUPLING MATCHED CASES

# 13. P-family — identical marginals, incompatible token counterfactuals

This is one of WDF2-B's strongest falsifiers.

Consider binary treatment `X` and binary outcome `Y`.

Population experiments show:

```text
P(Y=1 | do(X=0)) = 0.5
P(Y=1 | do(X=1)) = 0.5
```

Now compare two latent cross-alternative models.

## P1 — stable-response coupling

Half the population has:

```text
Y0=0, Y1=0
```

Half has:

```text
Y0=1, Y1=1
```

Treatment changes nobody's outcome.

---

## P2 — flip-response coupling

Half has:

```text
Y0=0, Y1=1
```

Half has:

```text
Y0=1, Y1=0
```

Treatment flips everyone's outcome.

---

## P1/P2 matched result

Both have exactly the same interventional marginals:

```text
0.5 vs 0.5
```

but radically different token counterfactuals and probabilities of benefit/harm.

Therefore:

```text
InterventionalMarginals do not identify Joint(Y0,Y1).
```

and:

```text
PopulationEffectDistribution != TokenCounterfactualCoupling
```

Counterfactual-probability work by Balke/Pearl and Tian/Pearl explicitly shows that attributional/counterfactual quantities can require assumptions beyond observational/interventional distributions and may only be bounded rather than point-identified.

### Falsifier P-F1

Any architecture that computes token counterfactual probability solely from `P(Y|do(X))` fails.

---

## P3 — observational conditional vs intervention

Construct confounding:

```text
latent U influences X and Y
```

Then:

```text
P(Y|X=x) != P(Y|do(X=x))
```

in general.

### Falsifier P-F2

Observation, intervention and counterfactual distributions remain distinct truth roles.

---

## P4 — deterministic SCM vs nondeterministic causal model

In a deterministic SCM, a sufficiently specified exogenous context plus intervention typically determines a unique solution/counterfactual world under standard acyclic assumptions.

A nondeterministic model can preserve the same factual solution while allowing several counterfactual solutions after intervention.

### Falsifier P-F3

A World-level architecture cannot require deterministic coupling as the definition of counterfactuality.

---

## P5 — same random seed across changed mechanism

Suppose policy/provider mechanism changes from M to M'.

A seed `u` in M may have no semantically corresponding seed in M'.

Therefore:

```text
hold random seed fixed
```

can be meaningful for value interventions within one mechanism and meaningless for cross-mechanism counterfactuals.

### Falsifier P-F4

Coupling criteria are alteration-dependent.

---

# 14. Probability-family conclusion

Counterfactual probability requires a distinction among:

```text
measure over alternatives
selection/generation of alternatives
coupling/correspondence across factual and altered alternatives
identification from evidence
```

These are four different problems.

A probability distribution does not automatically solve the counterfactual correspondence problem.

---

# PART VII — PREEMPTION / PREVENTION / OMISSION

# 15. C-family — stress cases reserved for WDF3 but required now

WDF2 must not solve causation, but its architecture must be capable of representing the contrasts later causal theories need.

## C1 — simple but-for

```text
C occurs -> E occurs
if not C -> not E
```

Simple dependence is representable.

---

## C2 — early preemption

```text
Suzy throws rock.
Billy also throws.
Suzy's rock shatters bottle first.
Billy's trajectory would have shattered it if Suzy had not.
```

Then:

```text
if not SuzyThrow -> bottle still shatters
```

while ordinary causal judgment still distinguishes Suzy's active process.

Structural-model actual-causation work uses contingencies/structural information precisely because simple but-for dependence is inadequate for such cases.

### Falsifier C-F1

A counterfactual architecture that exposes only one `remove candidate cause` comparison cannot support later preemption analysis.

It must allow alternative contingencies/pathway states without itself deciding causation.

---

## C3 — symmetric overdetermination

Two sufficient causes act simultaneously.

Removing either alone leaves E.

Again, simple dependence is insufficient.

---

## C4 — prevention

```text
threat T would produce harm H
preventer P blocks pathway
```

Relevant comparison may require preserving T while removing P.

If instead the alternative generator removes both P and T because that world is globally `closer`, the prevention relation becomes invisible.

### Falsifier C-F2

Pathway/contrast relevance can outrank generic global similarity for some causal questions.

This is pressure, not yet a causal-theory verdict.

---

## C5 — omission with duty

```text
operator does not apply required patch
failure occurs
```

Physical counterfactual:

```text
if patch applied -> no failure
```

Responsibility counterfactual additionally invokes:

```text
duty
available action
knowledge/authority
normal expectation
```

### Falsifier C-F3

A physical outcome counterfactual and a responsibility counterfactual can share the same alteration while requiring different background/normative coordinates.

```text
Causal/physical contrast != responsibility attribution
```

---

# PART VIII — IMPOSSIBLE / COUNTERCONVENTIONAL CASES

# 16. K-family — same impossible-looking antecedent, different source of impossibility

## K1 — logical contradiction

```text
If P and not-P were both true ...
```

This is logical-impossibility pressure.

---

## K2 — mathematical falsehood

```text
If a mathematical theorem were false ...
```

Depending on the query, this can target:

```text
mathematical truth
proof system
axioms
semantic convention
agent belief
```

These are not one alteration.

---

## K3 — nomologically impossible antecedent

```text
If a body exceeded the theory's physical constraint ...
```

This can mean:

```text
violate actual law locally
alter law
use an alternative physical theory
ask only within a fictional model
```

Each has different invariants.

---

## K4 — constitutively impossible under current rules

```text
If an unauthorized role possessed right R while current constitutive rule K says no such right exists ...
```

Possible readings:

```text
change role facts under K
change K
allow inconsistent institutional description
change semantic meaning of R
```

### Falsifier K-F1

`Impossible antecedent` is not enough to choose a semantics. The source of impossibility and intended alteration locus matter first.

---

## K5 — nonvacuity discriminator

Two counterpossibles with the same impossible antecedent but differently related consequents may be judged differently by nonvacuist theories.

Work on impossible-world semantics explicitly develops this as an alternative to treating all counterpossibles as trivially true.

### Falsifier K-F2

WDF2 must preserve a slot for nontrivial counterpossible evaluation. It must not bake vacuism into the universal grammar.

---

# PART IX — STRUCTURAL MODEL REVISION

# 17. M-family — when the antecedent does not fit the current model

## M1 — existing variable new value

Model contains variable X with domain including x'.

Counterfactual:

```text
X := x'
```

No structural revision required.

---

## M2 — new value outside current domain

Current model says:

```text
X ∈ {a,b}
```

Query asks:

```text
If X were c ...
```

Possibilities:

```text
model domain was incomplete
c changes the meaning/type of X
antecedent is impossible within M but meaningful in a revised model
```

### Falsifier M-F1

Fixed-domain intervention semantics alone cannot decide whether to reject, revise or reinterpret the query.

---

## M3 — new relation/mechanism absent from ontology

Query:

```text
If service S had delegated authority through mechanism D ...
```

but model M lacks any representation of delegation.

Encoding this as an arbitrary new value of an existing variable can hide structural change.

---

## M4 — new institutional status

Current model has no concept corresponding to a novel right/status created by a rule change.

The counterfactual cannot be faithfully asked until the representation changes.

### Falsifier M-F2

```text
ModelRevisionNeededBeforeEvaluation
```

must remain distinguishable from:

```text
CounterfactualFalseWithinCurrentModel
```

---

## M5 — changed grain

A micro model and macro model represent the same system differently.

A counterfactual may be stable at macro grain but underdetermined across micro realizations, or vice versa.

### Falsifier M-F3

Counterfactual validity can be grain/model-relative without becoming subjective.

---

# PART X — CROSS-DOMAIN MATCHED MATRIX

# 18. Compact discriminator matrix

| Case | Fixed | Varied | Failure exposed |
|---|---|---|---|
| A1/A2 | antecedent value, target | value vs mechanism alteration | resulting value does not identify surgery |
| A3 | first action outcome | token action vs policy | local override loses trajectory semantics |
| A4 | program purpose | input vs code | state and mechanism collapse |
| A6 | authorization outcome | credential vs rule | state vs constitution collapse |
| A8 | planning result | Reality vs model boundary | model/Reality collapse |
| I2 | surface antecedent | forward vs backtracking | hidden temporal accommodation |
| I4 | authorization antecedent | preserved rule vs altered rule | alteration/invariance incompatibility |
| I5 | target behavior | implementation vs specification invariant | abstraction-level invariance loss |
| X1 | service referent | service vs code identity | universal identity failure |
| X2 | institutional lineage | continuity criterion | constitutive correspondence failure |
| S1 | antecedent & target | tied repairs | unique-nearest assumption |
| S2 | coarse edit distance | change type/grain | metric representation dependence |
| S4 | surgery | nondeterministic outcomes | unique-counterfactual-world assumption |
| S5 | antecedent | target/query | global similarity metric failure |
| B1 | alarm antecedent | backtracking policy | opposite causal-history consequences |
| P1/P2 | interventional marginals | cross-world coupling | token counterfactual nonidentification |
| P3 | variable values | observation vs do | evidential/interventional collapse |
| P5 | mechanism change | coupling rule | same-seed assumption failure |
| C1/C2 | effect | backup pathway | simple but-for insufficiency |
| C4 | outcome | pathway relevance | generic similarity can erase prevention |
| C5 | physical alteration | normative background | causation/responsibility collapse |
| K1-K4 | counterpossible form | impossibility type | one impossible-antecedent policy failure |
| M1/M2 | variable name | domain membership | fixed-model completeness assumption |
| M3/M4 | target question | ontology availability | evaluation vs model revision collapse |

No candidate family has yet been scored. This matrix is the test suite WDF2-C inherits.

---

# 19. Derived invariants any candidate architecture must preserve

WDF2-B now has enough evidence to promote the following **research requirements**.

## RQ1 — typed alteration locus

A candidate must distinguish value assignment from mechanism, policy, rule, model and nomological alterations whenever the matched suite depends on that distinction.

## RQ2 — explicit preservation semantics

A candidate must expose, derive or otherwise constrain what stays invariant.

## RQ3 — alteration/preservation compatibility

A candidate must reject contradictory frames such as altering and preserving the same structure in the same sense.

## RQ4 — domain-scoped correspondence

A candidate must permit strict identity, criterion-relative continuity, counterpart/correspondence and no-valid-correspondence outcomes.

## RQ5 — plural alternatives

A candidate must not require universal uniqueness unless it can justify selection in tied/nondeterministic cases.

## RQ6 — query-sensitive relevance

A candidate must allow target/question type to affect which differences matter, or explain why a target-independent ordering nevertheless reconstructs those cases.

## RQ7 — backtracking policy

A candidate must state whether/how upstream history can change to accommodate the antecedent.

## RQ8 — probability/coupling separation

A candidate must distinguish alternative weights from factual-counterfactual coupling and from empirical identification.

## RQ9 — structural revision boundary

A candidate must say what happens when the antecedent is not expressible in the current model.

## RQ10 — impossible antecedent typing

A candidate must not silently conflate logical, nomological, constitutive, model-relative and counterconventional impossibility.

## RQ11 — causal-stress compatibility

A candidate need not define causation yet, but it must retain sufficient structure for preemption, prevention, omission and overdetermination analyses later.

## RQ12 — model/Reality truth-role firewall

A formal verdict remains a model-relative counterfactual until evidence/grounding justifies a stronger Reality-facing claim.

---

# 20. Strongest new result — Counterfactual Frame is constrained, not flat

WDF2-A's diagnostic signature looked superficially like a list of independent coordinates.

WDF2-B falsifies that interpretation.

The dependencies are at least:

```text
AlterationType
   constrains
PreservationProfile

AlterationType + PreservationProfile
   constrain
AdmissibleCorrespondence

Alteration + Preservation + Correspondence
   constrain
AlternativeGeneration/Selection

AlternativeGeneration + Coupling/Measure
   constrain
Would/Might/Probability evaluation
```

So the architecture is not:

```text
choose arbitrary values for independent fields
```

but closer to a **typed constraint system over a counterfactual frame**.

This remains a research grammar, not a Reality ontology.

---

# 21. Strongest new result — `minimal change` is downstream, not primitive

The matched cases show that one cannot rank changes until one knows:

```text
what counts as a change
at which grain
which structures are eligible to change
which are protected
what correspondence must survive
what query is being answered
```

Therefore:

```text
MinimalChange
```

is downstream of typed alteration/preservation/correspondence choices.

This weakens any temptation to start WDF2 by installing a universal global distance metric.

---

# 22. Strongest new result — unique nearest alternative is not foundation-safe

S1, S4 and probability cases jointly show three independent sources of plurality:

```text
ties in change ordering
objective/model nondeterminism
probability distributions over alternatives
```

Thus:

```text
UniqueNearestAlternative
```

cannot be a foundation-level requirement.

A Stalnaker-style theory remains a legitimate candidate because selection functions can add structure that chooses one alternative, but WDF2-C must ask **what grounds that selection and how it behaves under ties/nondeterminism** rather than importing uniqueness as a fact of Reality.

---

# 23. Strongest new result — interventionism and backtracking answer different questions

The B-family shows that intervention-style local surgery and backtracking are not mutually exclusive merely because one must globally replace the other.

They can be appropriate for different queries:

```text
What follows if output/action were locally set differently?
```

versus:

```text
What upstream circumstances would have had to differ for this state to arise normally?
```

Recent formal work on backtracking counterfactuals within SCMs reinforces exactly this separation.

Therefore WDF2-C should compare architectures partly by **query role**, not only by which formula they assign true/false.

---

# 24. Strongest new result — counterfactual probability is an identification problem as well as a semantic problem

P1/P2 prove by construction that identical interventional marginals can correspond to opposite individual response structures.

This means a counterfactual architecture needs three separate layers:

```text
semantic quantity
identification assumptions
available evidence
```

A mathematically well-defined token counterfactual may still be empirically unidentified.

This exactly preserves Ordivon's broader doctrine:

```text
TruthRole != EvidenceStrength
FormalDefinability != Identifiability
```

---

# 25. Candidate-family pre-screen without winner selection

WDF2-B can now state what each major family will be pressured by in WDF2-C.

## Stalnaker selection functions

Must explain:

```text
selection grounding
ties/nonuniqueness
query sensitivity
structural/rule changes
counterpossibles
```

## Lewis similarity/orderings

Must explain:

```text
similarity dimensions/priorities
representation/grain dependence
law vs fact divergence
query relevance
non-limit/tied cases
```

## Premise/background semantics

Must explain:

```text
background-premise selection
cotenability
nonmonotonicity
structural revision
```

## SCM / structural counterfactuals

Must explain:

```text
variable/model choice
mechanism vs rule/model change
fixed-model boundary
nondeterminism
backtracking
cross-alternative coupling
institutional constitution
```

Pearl's structural approach remains especially strong for explicit surgery and scientific computation, while recent nondeterministic/backtracking extensions show that even the SCM family contains important alternative semantics rather than one final fixed recipe.

## Law/chance-relative accounts

Must explain:

```text
law-changing antecedents
law metaphysics
chance/coupling distinction
institutional/software domains
```

## Powers/dispositional accounts

Must explain:

```text
rule/software counterfactuals
masks/finks/antidotes
explicit selection under competing manifestations
```

## Impossible-world/nonvacuist accounts

Must explain:

```text
ordering of impossible alternatives
source/type of impossibility
interaction with ordinary possible alternatives
```

## Plural/domain-relative accounts

Must explain:

```text
what is genuinely shared
what licenses domain-specific semantics
how pluralism avoids becoming arbitrary
```

No score is assigned in WDF2-B.

---

# 26. Deletion tests

## Delete typed alteration

**FAIL** — A-family collapses.

## Delete preservation profile

**FAIL** — I/B-family collapses.

## Treat alteration and preservation as independent

**FAIL** — I4 and mechanism/rule-change cases permit contradictory frames.

## Delete identity/correspondence

**FAIL** — X/P token cases become undefined or falsely identified.

## Require one nearest alternative

**FAIL as universal rule** — S1/S4 and nondeterministic cases require extra selection structure or plurality.

## Delete backtracking policy

**FAIL** — B1-B3 conflate upstream-accommodation and local-surgery questions.

## Delete coupling from probabilistic token counterfactuals

**FAIL** — P1/P2 become indistinguishable despite opposite individual effects.

## Delete structural model revision distinction

**FAIL** — M1-M4 confuse false-within-model with not-expressible-without-revision.

## Delete impossible antecedent support

**FAIL as universal research grammar** — K-family becomes unavailable before vacuism/nonvacuism is even tested.

## Delete one universal Counterfactual entity/object

**PASS** — the suite is fully expressible through typed query/frame structure.

---

# 27. WDF0 / WDF1 reopen audit

## WDF0

No FoundationReopenCondition fires.

The new cases strengthen rather than falsify:

```text
Reality != Model
IdentifierEquality != OntologicalIdentity
Cause != Constraint != Constitution
WithinModelUpdate != StructuralModelRevision
InstitutionRelative != ObserverOpinionRelative
```

WDF0 remains frozen.

## WDF1

No FoundationReopenCondition fires.

WDF1's TMCG was explicitly a typed modal claim grammar, not a complete counterfactual semantics. The B-suite fits its open alternative-generator/background interface.

Plural alternatives, probability/coupling and structural revision do not falsify TMCG because WDF1 never required a unique enumerable domain or fixed model completeness.

WDF1 remains frozen.

---

# 28. Production disposition

No production changes are admitted.

In particular do **not** add:

```text
CounterfactualFrame schema
SimilarityMetric service
CounterfactualSolver
CausalGraph registry
CrossWorldIdentity service
Global random-seed coupling
```

because research necessity does not imply consumer necessity.

Current production boundary remains intentionally narrower:

```text
Bind -> Observe -> Act -> Reconcile
```

and remains compatible with the foundations.

---

# 29. Residual ranking after WDF2-B

```text
1. Alternative generation / selection architecture          CRITICAL
2. Similarity / ordering / premise relevance grounding      CRITICAL
3. Structural surgery composition across levels             CRITICAL
4. Cross-alternative coupling / nondeterminism               CRITICAL
5. Backtracking vs forward accommodation semantics           HIGH/CRITICAL
6. Counterpossible / impossible-alternative semantics        HIGH
7. Structural model revision under counterfactual queries    HIGH
8. Would/might modal-force logic                              HIGH
9. Counterfactual probability identification                 HIGH
10. Prevention/omission/preemption bridge to causation        HIGH
```

The first residual is now clearly upstream of the rest: once alteration, preservation and correspondence are typed, **which alternatives actually count and how are they selected/evaluated?**

---

# 30. Exact next round

The next canonical round is therefore:

# **WDF2-C — Counterfactual Alternative Generation / Selection Architectures**

WDF2-C should formally compare at least:

```text
Stalnaker selection-function architecture
Lewis sphere/order architecture
premise/background/cotenability architecture
SCM forward-surgery architecture
SCM backtracking architecture
nondeterministic structural alternatives
law/chance-relative generation
powers/dispositional grounding
impossible-world/nonvacuist extension
plural/domain-relative architecture
```

against the WDF2-B falsifier suite.

It must not ask only:

```text
which theory reproduces ordinary-language intuitions?
```

It must also test:

```text
cross-domain alteration typing
preservation compatibility
identity/correspondence
multiple minima
nondeterminism
model revision
probability coupling
institutional constitution
preemption-readiness
```

Only WDF2-C residuals may determine WDF2-D.

---

# 31. Primary-source pressure used in this round

The case suite was built from Ordivon foundations plus primary research pressure including:

- Stalnaker's selection-function family and Lewis's comparative-similarity/order family as the canonical competing possible-world architectures.
- David Lewis, `Counterfactual Dependence and Time's Arrow` — backtracking and similarity-priority pressure.
- Judea Pearl, `Structural Counterfactuals: A Brief Introduction` — structural-surgery counterfactual semantics and scientific applications.
- Joseph Y. Halpern & Judea Pearl, `Causes and Explanations: A Structural-Model Approach. Part I` — preemption/contingency pressure on simple counterfactual dependence.
- Alexander Balke & Judea Pearl, `Counterfactual Probabilities: Computational Methods, Bounds and Applications` — counterfactual probabilities may require mechanism priors/assumptions and otherwise admit only bounds.
- Jin Tian & Judea Pearl, `Probabilities of Causation: Bounds and Identification` — attributional counterfactual quantities and identification bounds.
- Julius von Kügelgen, Abdirisak Mohamed & Sander Beckers, `Backtracking Counterfactuals` — formal separation of interventionist forward surgery from backtracking counterfactuals inside an SCM setting.
- Sander Beckers, `Nondeterministic Causal Models` — removal of deterministic unique-counterfactual-world assumptions and extension toward probabilistic cases.
- Francesco Berto, Rohan French, Graham Priest & David Ripley, `Williamson on Counterpossibles`, plus impossible-world work — explicit nonvacuist pressure for impossible antecedents.

These sources constrain the falsifier suite. None is treated as authority for a preselected Ordivon World ontology.

---

# 32. Closeout

```text
WDF2-B: COMPLETE
WDF0 reopen: NO
WDF1 reopen: NO
WDF2-A reopen: NO
Production refactor: NO

Alteration typing: REQUIRED
Alteration/Preservation compatibility: REQUIRED
Identity/Correspondence pluralism: REQUIRED
Unique-nearest-world as universal rule: REJECTED
Backtracking policy: REQUIRED TO BE EXPLICIT/DERIVED WHEN RELEVANT
Probability/Coupling separation: REQUIRED
Structural model revision boundary: REQUIRED
Impossible antecedent uniform treatment: REJECTED

Exact next round:
WDF2-C — Counterfactual Alternative Generation / Selection Architectures
```

Compressed result:

> **WDF2-B shows that counterfactual reasoning cannot be reduced to “make the antecedent true and inspect the nearest alternative.” The antecedent has a typed surgery locus; the preserved background must be compatible with that surgery; the subject must be tracked by a domain-appropriate identity or correspondence criterion; and even after all of those are fixed, several relevant alternatives may remain because of ties, nondeterminism or probability. Population/interventional distributions can still leave token counterfactuals underidentified because factual and altered outcomes require an additional coupling. The next irreducible problem is therefore alternative generation and selection itself: how relevant alternatives are produced, ordered, tied, weighted or left plural without smuggling the desired answer into similarity, causal structure or background assumptions.**
