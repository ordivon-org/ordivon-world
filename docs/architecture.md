# Architecture

## Semantic flow

```text
Task / Attempt / Effect
        │
        ▼
World Interaction intent
  target relation
  capability and consequence
  data and locality
  identity and evidence
  continuity requirements
        │
        ▼
Candidate observations
  provider capability
  endpoint and path
  transport and session
  identity and policy
  availability, cost, freshness, uncertainty
        │
        ▼
Interaction Binding
  exact semantic references
  exact target and participant references
  exact path/transport/endpoint revisions
  exact provider/body/execution revisions
  authority and policy revisions
        │
        ▼
Classical mechanisms execute and communicate
        │
        ▼
Receipt / Artifact / Observation / callback / residual state
        │
        ▼
reconcile → verify → invalidate → rebind → continue
```

## Internal analytical planes

### Relationship and connectivity plane

Explains logical source and target, communication identity, endpoint, path,
transport, session, delivery state, callback, and path-conditioned evidence.
It does not implement the network stack or own Task strategy.

### Capability and action plane

Explains external capability, provider, body or service, operation, Dispatch,
provider execution, Receipt, Artifact, cancellation, compensation, and residual
state. It does not implement provider-native lifecycle or own Task meaning.

### Continuity plane

Correlates communication and execution under one interaction, preserves unknown
outcomes, invalidates condition-dependent evidence, and records rebinding. This
is the principal reason to study the planes together.

## Data topology

Control and evidence may pass through Host while bulk data moves directly:

```text
Host ──interaction intent──▶ World/provider
Host ◀──Receipt/reference── World/provider
Provider A ──Artifact bytes──▶ Object Store / Provider B
Host ◀──digest + provenance── Object Store / Provider B
```

World is not a universal proxy.

## Current code map

- `providers/cloudflare/` implements one provider and remote-effect reliability.
- `modules/network-observation/` implements observations, local presentation,
  private operations, and controlled research fixtures.
- no universal resolver, Interaction Binding schema, provider router,
  participant registry, or automatic recovery controller exists yet.
