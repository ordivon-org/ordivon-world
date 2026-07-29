# World Interaction Model

This document is a field inventory for research, not a stable schema.

## One interaction may contain

### Semantic references

- Goal, Task, Attempt, Effect, Dispatch, Claim, Verification;
- completion, cancellation, compensation, and consequence expectations.

### Parties and authority

- initiator, logical target, provider, participant, resource owner;
- credential domain, delegated authority, budget, allowed consequence.

### Capability and placement

- required operation or relationship;
- local/remote execution position, provider, region, body or service generation;
- input data, locality, privacy, duration, callback, and evidence requirements.

### Connection

- endpoint, route/path class, transport, protocol, session, identity generation;
- direct, VPN, proxy, provider network, queue, Artifact handoff, or intermediary.

### Physical action and delivery

- request/message/Artifact delivery identity;
- provider operation or execution identity;
- accepted, delivered, running, replied, succeeded, failed, rejected, cancelled,
  compensated, or unknown states.

### Result and evidence

- Receipt, Artifact, Observation, callback, logs, content digests;
- provider, body, path, identity, policy, build, method, time, and freshness;
- verified, conditional, expired, superseded, or unresolved status.

### Continuity

- query/reconciliation key;
- invalidation dependencies;
- replacement of path, endpoint, identity, provider, body, transport, or
  participant;
- reconstruction inputs and residual state.

## Cardinality

One Task may create many interactions. One Effect may require several Dispatches
but must preserve one semantic identity and reconcile before repetition. One
provider execution may emit many Artifacts and use many external relationships.
One path may carry many interactions. One Artifact may become input to many
later interactions.

## Identity rule

Do not collapse Task, Effect, Dispatch, message delivery, provider execution,
session, body generation, path observation, Receipt, and Artifact into one ID.
A unified project needs one correlated graph, not one universal identifier.
