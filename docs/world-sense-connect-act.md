---
schema_version: 1
id: world.research.sense-connect-act
title: Sense, Connect and Act Research Boundary
type: research
profile: engineering
lifecycle: active
source_role: current-research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: Reframes World around the external organs an Agent needs beyond its current Host: sensing reality, establishing usable relations, and causing bounded effects, while preserving owner-native authority and recovery semantics.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.w5.discovery-connection
  - world.w5.interaction
---
# Sense, Connect and Act Research Boundary

## Starting observation

The current production World implementation is strongest after an external target and capability are already known. Cloudflare capability snapshots and provider observations, Browser/Fetch receipts, network-condition observations, Resource/Message/Entity wire destinations and reconciliation all begin from a bounded known object, endpoint, trajectory or provider.

That leaves a prior question underdeveloped:

> How does an Agent whose current Body is hosted on one machine discover external entities and capabilities that are not already present in its bounded view?

A useful first decomposition is:

```text
Agent
  ├─ Sensor     World → Agent
  ├─ Connector Agent ↔ World
  └─ Effector   Agent → World
```

This is a research decomposition, not a new universal production API.

## Repository audit at World `2f964511`

### Sensor: present, but fragmented and target-first

Current Sensor-like mechanisms include:

- `CloudflareWorldAdapter.capabilities()` and `CapabilitySnapshot`;
- provider `WorldObservation` and Browser Artifact verification;
- `network-observation.schema.json` plus operator network-condition tooling;
- `surfshark-profile-scan`, which already uses the word discovery for a bounded configured profile population;
- W5-C owner-native discovery/reachability evidence.

The common limitation is that these mechanisms normally start from a known provider, known profile population, known endpoint or known domain object. They observe current conditions well; they do not yet form an Agent-facing substrate for discovering previously unknown external capability candidates.

### Connector: typed and owner-native

Current Connector-like mechanisms include:

- `SignedHttpTransport` and the Cloudflare adapter transport;
- Resource, Message and Entity `*WireDestination` transports;
- endpoint identity and reachability research retained by W5-C;
- operator-controlled VPN/network tools.

These are intentionally not a universal `WorldLink`. Existing W5-C evidence remains valid: discovery, reachability, relationship/session and authority are orthogonal.

### Effector: the most mature side

Current Effector-like production families include:

- Cloudflare bounded Fetch and Browser effects;
- Resource Transfer;
- Message Delivery;
- Entity Migration.

They already have exact intent/request identity, native owner/provider execution, Receipt-or-UNKNOWN semantics and identity-bound reconciliation before retry. The missing Sensor layer does not weaken these existing Effect laws.

## Sensor P0: borrowed external discovery

A live P0 experiment used the current local Agent/Runtime environment and a public, explicitly offered external relay catalog.

The target was VPN Gate's public relay list. The catalog is intended for public client use; the experiment did not connect to any relay.

### Direct local observation failed through two paths

The same catalog was first requested directly from the current Host environment:

```text
ambient
  → DNS resolution timeout

native-a
  → HTTPS CONNECT sidecar established the selected transport profile
  → TLS failed with unexpected EOF
```

These observations are path-bound failures. They do not prove that the catalog or relays were absent.

### A borrowed Sensor widened the observable world

A temporary Cloudflare Worker was then deployed as a read-only Sensor. The Agent reached that Sensor through the already-proven `native-a` transport and a temporary `ordivon.com` custom route. The Worker fetched the same public catalog remotely and returned only bounded candidate metadata.

The first successful observation found 97 current catalog rows. A second observation shortly afterward found 99 rows, demonstrating that the observed population was live and changing rather than a static fixture.

The second observation also extracted advertised Connector affordances from the public OpenVPN configuration without establishing a connection. Example:

```text
entity       = public-vpn-78
country      = JP
address      = 219.100.37.53
connector    = OpenVPN
transport    = tcp
port         = 443
```

Seven other bounded candidates in the same observation exposed the same protocol family on distinct current endpoints.

The local machine did not have an OpenVPN client installed, so the experiment stopped before protocol connection. This is an intentional boundary:

```text
Discovered connector affordance
!=
connection established
```

### Cleanup

The temporary Worker, DNS record and Worker Route were deleted after the observation. Exact follow-up GETs returned 404 for all three resources.

## What Sensor P0 proves

```text
Failure to observe through Sensor A
!= external entity absence

Observation is bound to a sensing path / Body / provider condition.

An Agent can borrow an external sensing capability
without owning the remote machine that performs the observation.

A Sensor may discover both external entities
and their advertised Connector affordances
without establishing a relationship or minting authority.

Sensor != Connector != Effector.
```

This also sharpens W5-C rather than replacing it. Discovery remains epistemic evidence. A discovered relay address or protocol declaration does not prove reachability, relationship, trust, authorization beyond its public grant, or successful execution.

## Current product decision

Sensor P0 does **not** justify:

```text
SensorManager
GlobalDiscoveryRegistry
GlobalCapabilityGraphDatabase
WorldLink
AutomaticConnectorSelection
AutomaticRouteMutation
```

The next experiment should use one explicitly public/authorized candidate and independently test the Connector layer while keeping the machine's default route unchanged. Only after a real connection is established should a separate Effect experiment test whether useful external action can traverse that connection.

The production World boundary remains unchanged until repeated workloads prove a stable shared contract.
