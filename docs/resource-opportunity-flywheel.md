# Resource Opportunity Flywheel

Ordivon should search the external world broadly without turning every observed service, dataset, API, model, machine, or account offer into owned infrastructure.

The governing asymmetry is simple:

- candidate discovery is cheap and should optimize recall;
- owner verification is more expensive and should be selective;
- authority acquisition can create durable user obligations and must be explicit;
- transport evidence is current, path- and resolver-scoped rather than a property of the resource forever;
- only real consumption can establish whether a resource was useful for a workload.

The resulting loop is deliberately thin:

```text
broad discovery feeds / indexes / search
                |
                v
        ResourceCandidate
        + exact provenance
                |
                v
      demand-scoped potential
                |
       bounded verification budget
          /              \
         v                v
 owner-native facts   transport + resolver evidence
         \                /
          \              /
           v            v
          hard admission gates
                 |
        +--------+--------+
        |                 |
        v                 v
 authority queue     consumable-now
                          |
                    Pareto frontier
                          |
                     real consumer
                          |
                 ConsumptionOutcome
                          |
                    ranking feedback
```

## 1. Broad recall is not authority

Aggregators, awesome lists, search engines, registries, OpenAPI directories, academic indexes, social discovery and provider comparison sites are candidate generators. They may establish that a claim was observed at a time and location. They cannot establish current owner terms, license, quota, payment requirements, identity requirements, or permission to consume.

`DiscoveryEvidence.source_kind` therefore distinguishes `aggregator`, `index`, and `owner` structurally. A candidate without a matching `OwnerVerification` remains `owner-verification-required` regardless of how many aggregators mention it.

## 2. Verify the smallest high-potential set

A universe can contain hundreds of candidates while the owner-verification queue remains small. `build_opportunity_board(..., verification_budget=N)` spends at most `N` expensive verification slots at a time.

The budget first resolves missing/stale owner facts, then spends remaining capacity on missing/stale transport facts. This is not because owner facts are intrinsically more important; it prevents network testing from being performed for a resource whose terms or authority already make it unusable.

Candidate breadth therefore does not create a proportional governance backlog.

## 3. Keep orthogonal facts orthogonal

The following must not be collapsed into one confidence or quality score:

- owner identity and currentness;
- service terms and allowed purpose;
- content/data/model license;
- account, key, student, identity, payment or operator authority;
- price/quota class;
- machine interface;
- current path + resolver reachability;
- workload capability fit;
- observed consumer value.

Hard gates are evaluated before ranking. A high-value resource forbidden for the workload is still blocked. A free-key resource does not become anonymous because it scores well. A public dataset does not imply that the hosted API is free for commercial production.

## 4. Transport is `(resource, path, resolver, time)`

`TransportEvidence` explicitly carries both `path_id` and `resolver_id`. This prevents an ambient DNS failure, polluted resolver, stale VPN generation, or temporary route failure from being promoted into a permanent claim that the owner resource is unavailable.

Workstation owns these physical facts. World consumes the evidence without becoming the route or resolver authority.

## 5. Pareto before scalar ranking

A universal scalar score destroys useful trade-offs. A lower-friction, broadly reusable public dataset and a more diverse but narrower resource can both be rational choices.

Ordivon therefore:

1. applies hard admission gates;
2. computes the non-dominated `pareto_frontier` among `consumable-now` resources;
3. uses `potential_score` only as a tie-break/order hint inside a semantic class.

The score is not permission, truth, or a substitute for the frontier.

## 6. Consumption closes the loop

A resource that passes owner and transport checks is still only a hypothesis about utility. Actual consumers should emit bounded `ConsumptionOutcome` evidence: workload identity, timestamp, whether the resource was useful, an approximate value in `[0,1]`, and evidence references.

Outcome evidence may change future ordering. It never changes owner authority, terms, license, or transport truth.

Resources in `consumable-now` with no workload-specific outcome are placed in the `feedback_queue`. This makes dogfood a first-class part of resource research rather than an optional postscript.

## 7. Opportunity board lanes

`ResourceOpportunityBoard` exposes separate next-action lanes:

- `frontier`: non-dominated immediately consumable resources;
- `owner_verification_queue`: top candidates whose owner facts are absent/stale;
- `transport_verification_queue`: owner-admitted candidates needing current path+resolver evidence;
- `authority_queue`: resources whose only remaining blocker is a stronger user authority class;
- `consumption_queue`: all currently consumable candidates;
- `feedback_queue`: consumable candidates still lacking outcome evidence for this workload;
- `rejected`: capability mismatch, terms block, or current transport failure.

This is a work-selection projection, not a durable resource inventory and not an automatic provisioning system.

## 8. Expansion policy

Prefer expansion in this order unless a concrete workload proves otherwise:

1. anonymous, owner-published machine-readable resources;
2. bulk snapshots/indexes that reduce repeated API/network dependency;
3. free-key/account resources with clear marginal value;
4. student/identity/payment-gated resources only for a named workload;
5. new external compute/network authority only after existing resources are shown insufficient.

Self-hostable alternatives should remain part of discovery because they convert recurring SaaS authority/cost into local execution cost. They are candidates, not automatically better choices.

## 9. Currentness and invalidation

No owner verification or transport result is permanent. Consumer demand supplies explicit freshness budgets. Stale evidence returns to a verification queue rather than being silently trusted.

This makes resource research a continuous world-model update loop without requiring a continuously growing orchestration framework.
