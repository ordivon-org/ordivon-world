# Resource Opportunity Flywheel

Ordivon should search the external world broadly, acquire legitimate high-value resources aggressively, and keep discovery, acquisition, authority, transport, and actual utility as separate facts.

The governing asymmetry is:

- discovery is cheap, so optimize recall;
- owner verification is selective and current;
- acquisition friction is a cost term, **not a moral veto**;
- willingness to acquire authority is not evidence that the authority is already held;
- human participation is reserved for irreducible identity, MFA, CAPTCHA, payment, or personally binding actions;
- transport is `(resource, path, resolver, time)` rather than a permanent property of a provider;
- only semantic consumption can establish workload value.

```text
broad discovery
      |
      v
ResourceCandidate
      |
      v
OwnerVerification  -- current owner terms + attested capabilities
      |
      +-----------------------------+
      | anonymous                   | gated
      v                             v
 transport                  AcquisitionAssessment
                                    |
                         net opportunity value
                           /        |         \
                          v         v          v
                    acquire-now  human-action  defer
                          |         |
                          +----+----+
                               v
                       AuthorityEvidence
                      -- what we actually hold
                               |
                               v
                  transport + resolver evidence
                               |
                               v
                         consumable-now
                               |
                         Pareto frontier
                               |
                        semantic consumer
                               |
                      ConsumptionOutcome
                               |
                         ranking feedback
```

## 1. Broad recall is not authority

Aggregators, search engines, awesome lists, entitlement catalogs, registries, social discovery, comparison pages, and OpenAPI directories are candidate generators. They may establish that a resource or offer was observed. They do not establish current owner terms, eligibility, quota, payment exposure, license, or permission.

`DiscoveryEvidence.source_kind` keeps `aggregator`, `index`, and `owner` distinct. Candidate capability labels remain discovery hypotheses. A candidate remains `owner-verification-required` until a current matching `OwnerVerification` exists **and attests every required capability used by the demand-fit projection**. Owner identity/terms/interface evidence alone must not turn an aggregator capability label into semantic truth.

## 2. Provider requirement, acquisition decision, and possessed authority are three coordinates

The old model conflated these questions:

1. What authority does the provider require?
2. Is obtaining it worth the cost?
3. Do we actually possess it now?

They are now represented separately:

- `OwnerVerification.authority_class`: required class (`free-key`, `account`, `student`, `payment`, ...).
- `OwnerVerification.verified_capabilities`: current owner-attested capability claims for the exact resource identity; candidate labels not present here cannot establish required demand fit.
- `AcquisitionAssessment`: current eligibility, acquisition mode, benefit, option value, burden, human actions, expiry, and prerequisites.
- `AuthorityEvidence`: current non-secret proof that Ordivon actually holds the required authority.

A demand may be willing to acquire a payment-gated resource and still have no authority. Conversely, once a student/account/key authority is held, the resource is not permanently penalized for the historical friction required to obtain it.

## 3. Maximize lawful net opportunity value

Account creation, student verification, free-tier enrollment, and free API keys are ordinary acquisition costs when the provider permits them. They are not reasons to abstain.

`AcquisitionAssessment` computes an inspectable normalized estimate:

```text
gross opportunity
  = 0.65 * expected benefit
  + 0.35 * option value

burden
  = 0.25 * acquisition cost
  + 0.20 * maintenance cost
  + 0.25 * payment exposure
  + 0.15 * lock-in cost
  + 0.15 * expiry pressure

net opportunity = gross opportunity - burden
```

If eligible and net value clears the workload threshold:

- `agent-self-service` -> `acquire-now`;
- login / student / identity / payment / contract step -> `human-action-required`.

If current eligibility is false -> `not-eligible`. If the net value is weak -> `defer-acquisition`. Those are factual/economic decisions, not moralized authority classes.

Provider rules still bind. Ordivon must not create duplicate free-tier accounts contrary to rules, misrepresent student/identity eligibility, evade quotas, bypass payment controls, or convert someone else's entitlement into its own.

## 4. Parent entitlements compress human work

Many resources are unlocked by one upstream entitlement. `AcquisitionAssessment.prerequisite_resources` captures this explicitly.

Example:

```text
GitHub Student Developer Pack
        | verify once
        v
student entitlement authority
        |
        +-- Codespaces
        +-- Datadog
        +-- Camber
        +-- MongoDB
        +-- Sentry
        +-- partner offers ...
```

Before the parent authority exists, children enter `dependentAcquisitionQueue`; they do not each create duplicate human-verification work. After the parent is proven active, each child can move into its own lowest-cost claim lane.

## 5. Human Action Queue is an execution boundary

The Human Action Queue should contain only actions an Agent cannot correctly complete itself, for example:

- CAPTCHA;
- MFA / SMS / email confirmation in a third-party UI;
- student or legal identity verification;
- payment-card entry;
- personally binding terms or attestations;
- irreversible paid commitments.

Research, comparison, configuration, transport testing, secret-reference design, post-acquisition validation, integration, quota tracking, expiry tracking, and consumption belong to the Agent.

## 6. Verification budget bounds expensive facts, not opportunity breadth

`build_opportunity_board(..., verification_budget=N)` allows a universe to contain thousands of cheap candidates while only `N` expensive missing facts are investigated at once. Budget is spent in dependency order:

1. owner verification;
2. acquisition/eligibility verification;
3. transport verification after authority exists.

This is a work-selection optimization. It is not a reason to suppress high-value gated candidates.

## 7. Transport is downstream of acquisition

A transient DNS or network failure on a signup page must not erase a positive-EV entitlement. Transport becomes a hard requirement when Ordivon is ready to consume the machine interface.

`TransportEvidence` carries `path_id`, `resolver_id`, timestamp, status and latency. Workstation owns these physical facts; World consumes them without becoming route/DNS authority.

## 8. Pareto after authority is held

Among `consumable-now` resources, the Pareto frontier uses benefit dimensions. Historical authority friction is intentionally excluded from dominance: once the authority is legitimately held, a useful student/account resource should not lose forever to an anonymous resource merely because registration happened in the past.

Scalar `potential_score` remains an ordering hint, never authority or truth.

## 9. Semantic consumption closes the loop

TCP/TLS/HTTP success is not utility. The consumer must validate the expected semantic object before emitting `ConsumptionOutcome(useful=true)`. This prevents error pages, stale endpoints, empty quota shells, or nominal credits that cannot serve the workload from being mistaken for useful resources.

Outcomes affect future search/ranking, but never rewrite owner terms, eligibility, authority, license, or transport evidence.

## 10. Opportunity board lanes

`ResourceOpportunityBoard` schema v2 exposes:

- `frontier`: non-dominated resources usable now;
- `ownerVerificationQueue`: missing/stale owner truth;
- `acquisitionVerificationQueue`: missing/stale eligibility or cost facts;
- `acquireNowQueue`: positive-EV acquisition the Agent can perform itself;
- `humanActionQueue`: positive-EV acquisition requiring irreducible human action;
- `dependentAcquisitionQueue`: child offers waiting on parent entitlements;
- `transportVerificationQueue`: possessed resources needing current route/resolver proof;
- `consumptionQueue`: resources usable now;
- `feedbackQueue`: usable resources without workload outcome;
- `deferredAcquisition`: legitimate but currently below the acquisition threshold;
- `rejected`: terms, eligibility, fit, or current transport facts that actually block the resource.

`authorityQueue` is retained as a compatibility projection of `acquireNowQueue + humanActionQueue`; it should not be interpreted as a moral quarantine.

## 11. Expansion policy

Do not artificially order the universe as anonymous -> account -> student -> payment. Instead, compare all legitimate candidates on expected net opportunity value. A $100 student credit requiring one verification can dominate a weak anonymous API; a card-gated trial can be rational if spending protection is strong; an anonymous resource can dominate both when it gives the same capability with lower total burden.

The search universe should explicitly include:

- anonymous/open data;
- free API keys and developer plans;
- student/education entitlements;
- free trials and recurring monthly credits;
- cloud compute/storage/network credits;
- model inference quotas;
- search/index APIs;
- observability/security/dev tooling;
- domains/hosting/CI/CD;
- research/startup/community grants;
- self-hostable substitutes.

Scarcity or the possibility that another eligible person might also use the resource is not a reason to abstain from a legitimate entitlement. Capacity, currentness, rules, and net value are the relevant facts.

## 12. Currentness and invalidation

Owner terms, offers, eligibility, credits, authority state, transport, and consumer utility all expire at different rates. Each evidence type therefore carries its own timestamp/freshness budget. Stale evidence returns to the appropriate verification lane instead of silently persisting as truth.

## 13. Resource abundance, options and capability

The opportunity flywheel is one part of the broader [`Resource → Option → Capability World Model`](resource-option-capability-model.md).

The additional law is:

```text
resource candidate
  + current owner truth / required capability attestation
  + possessed authority
  + current access
  + workload fit
        ↓
current option
```

Several current options for the same target transition create useful redundancy only when they are substitutable and do not all collapse under the same relevant failure domain. Therefore candidate count, `diversity_potential`, geographic labels, or protocol labels alone must never be reported as proven redundancy.

`diversity_potential` remains an inexpensive candidate-ranking heuristic. Proven independence requires current evidence from the owner of the relevant failure-domain fact (for example Workstation for physical network access). The Resource Opportunity Board intentionally does not persist a universal failure-domain graph.

Semantic consumption then does more than validate utility: attributable outcomes increase Knowledge Capital and can improve later discovery, acquisition, promotion/demotion and retirement decisions. A capability exported by one owner may itself become a resource for another owner, but authority and currentness remain at their original boundaries.
