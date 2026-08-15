# CF5 — Selection, Sorting and Exposure Assignment

Status: **COMPLETE**

## 1. Environment is partly an outcome

CF4 asks what exposure does to later capability. CF5 asks a logically prior question:

> Why did this Actor receive, enter, remain in, or leave this Environment/Institution?

A useful causal sketch is:

```text
Actor state ───────→ environment choice
     │                    │
     │                    ▼
     └──────────────→ later Outcome

Institution rules ─→ admission / exclusion / exit
Search / information / cost ─→ assignment
Common causes ─────→ assignment + Outcome
```

Therefore observed exposure is not automatically exogenous.

## 2. Three different causal questions

CF5 separates:

1. **Exposure effect** — what would happen if comparable actors experienced another environment/institution?
2. **Assignment-mechanism effect** — what happens if search, information, admission, eligibility or matching rules change who enters?
3. **Composition effect** — how does changing who enters alter aggregate observed outcomes even if the within-environment treatment is unchanged?

These questions can point to different interventions.

## 3. Creating Moves to Opportunity is a clean selection example

The randomized CMTO intervention changed the search/brokerage process and substantially increased entry into high-opportunity neighborhoods in that study.

The important CF lesson is not the exact housing policy. It is structural:

```text
Environment opportunity exists
!= Actor enters it
```

and the assignment mechanism can itself be causally intervened on.

## 4. Selection is not merely “bias”

Sometimes selection is a nuisance that prevents identification.

Sometimes selection **is the mechanism we want to change**:

- lower search friction;
- alter school/job admission;
- change provider eligibility;
- improve matching;
- make exit safer;
- expose hidden capability to buyers/reviewers.

Calling all selection “bias” would hide a real policy/action surface.

## 5. Evidence classes are query-specific, not one quality ladder

Randomization can strongly identify an assigned intervention but may still leave:

- noncompliance/uptake questions;
- mechanism uncertainty;
- target-population transport;
- long-horizon feedback;
- selection after the initial treatment.

Likewise, a strong natural experiment or longitudinal design can answer a narrower query that a small RCT does not.

CF5 therefore records the assignment mechanism and assumptions rather than computing a universal causal-evidence score.

## 6. Hard rule

> **Observed environment/institution outcome differences are descriptive until the assignment process and comparison justify a causal exposure claim.**

If the assignment mechanism is unknown and no design resolves it, preserve the effect as `UNKNOWN`, not “mostly environmental” or “mostly individual.”

## 7. No new World object

Selection/sorting remains an identification role. CF5 does not create:

```text
SelectionEntity
SelectionScore
GlobalAssignmentGraph
DeconfounderService
```

The relevant admission, search, eligibility, exit and owner facts stay native.
