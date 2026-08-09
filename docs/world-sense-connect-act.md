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


## Connector P0: external relations are staged, path-bound and degradable

Sensor P0 ended at an advertised OpenVPN affordance. Connector P0 asked the next question:

> After an Agent discovers an explicitly public external capability, what does it actually mean for a connection to exist?

The live experiments reject a boolean answer.

### VPN Gate: reachability was not session usability

The experiment temporarily installed the distribution OpenVPN client and selected only publicly advertised VPN Gate relay configurations discovered by the Sensor. All OpenVPN runs used `route-nopull`; no run was allowed to replace the Host default route.

A bounded candidate set demonstrated several distinct states under the same nominal `JP + OpenVPN + TCP/443` description:

```text
advertised endpoint
  ├─ CONNECT 502
  └─ CONNECT 200
       ↓
       TLS certificate verification
       ↓
       OpenVPN Peer Connection Initiated
       ↓
       repeated PUSH_REQUEST
       ↓
       no PUSH_REPLY
```

Several endpoints were CONNECT-reachable through both Workstation A/B HTTPS CONNECT sidecars while neighboring endpoints in the same public relay population returned 502. Three candidates completed TLS verification and OpenVPN peer initiation but never received server configuration. An ambient control against the same relay reached the same peer-initiation state and also failed to receive `PUSH_REPLY`, relocating that failure away from the A-side CONNECT sidecar.

Therefore:

```text
advertised Connector affordance
!= reachability

reachability
!= transport establishment

transport establishment
!= protocol session

protocol session
!= usable tunnel
```

### Connector implementation acquisition is a separate capability

The Host initially had no OpenVPN client and could not directly retrieve Tor Project tooling through the tested local paths. Connector P0 therefore also exposed a prior dependency:

```text
need Connector X
  ↓
need implementation of X
  ↓
implementation source may itself be unreachable
```

A temporary fixed-target Cloudflare Worker was used only to discover and retrieve the current Tor Linux x86_64 Expert Bundle from the Tor distribution service. It was not an arbitrary proxy. The first download left a 19,080,660-byte local file while the remote object reported 32,203,755 bytes; gzip/tar verification failed with unexpected EOF. The file was therefore rejected as non-materialized despite existing locally.

A later retrieval produced exactly 32,203,755 bytes and passed gzip integrity. The bundle digest was:

```text
sha256:5a8f19f5f119b5fa2a8fd799a3a532e3236ad36164241800d6302e32f0e1c2a9
```

The detached signature was verified against Tor Browser Developers fingerprint `EF6E286DDA85EA2A4BA7DE684E2C6E8793298290`; the signing key was acquired independently from the artifact relay. The temporary Worker, DNS record and Worker Route were then deleted, and exact follow-up reads returned 404.

This preserves an existing Ordivon law in another domain:

```text
local file existence
!= immutable Artifact materialization
```

### Snowflake: a borrowed relation really formed, then degraded

The signed Expert Bundle contained Tor 0.4.9.11 and lyrebird 0.8.1 plus current bundled Snowflake bridge parameters. The managed transport was given a process-private resolver view bound to the Workstation Direct DNS stub. `lyrebird` ran as routing UID 951, whose outbound sockets select policy table 201.

This runtime binding is deliberately described as **Workstation Direct Route A**, not the `native-a` HTTPS-CONNECT transport profile. The two share lower physical route machinery, but the Snowflake runtime used direct UID-routed TCP/UDP sockets and therefore exceeds the HTTPS-only semantic scope of `native-a`.

The first 180-second run reached:

```text
0%  starting
1%  connecting to pluggable transport
2%  connected to pluggable transport
10% connected to a relay
14% relay handshake
15% relay handshake done
20% encrypted directory connection
25% requesting networkstatus consensus
30% loading networkstatus consensus
```

The extended 360-second run reproduced the same upper stage. It physically captured `lyrebird` as UID 951 with direct external TCP connections to a CDN/rendezvous address on port 443 plus UDP/WebRTC sockets; an exact route probe for UID 951 selected table 201. The Tor process itself exposed only its loopback SOCKS endpoint and loopback connections to lyrebird in the captured snapshots.

The relation was not stable enough to become a fully ready Tor client. Logs repeatedly showed peer acquisition followed by `DataChannel.OnOpen` timeout, stale peer closure or broker no-answer conditions. Some peers did connect and carry a Tor bridge handshake; the current borrowed peer population simply did not sustain full bootstrap in the bounded acceptance windows.

Thus Connector P0 has a positive result without claiming a fully usable egress:

```text
borrowed peer acquired       ✅
external transport connected ✅
Tor relay handshake          ✅
encrypted directory relation ✅
full Tor bootstrap           ❌ not proven
```

### obfs4: a different transport failed earlier

The same signed Expert Bundle also contained seven built-in obfs4 bridges. A stricter acceptance ran both Tor and lyrebird as UID 951 with zero effective Linux capabilities, a process-private Direct DNS view and table-201 routing. This physically removed route-mutation authority from the Connector process tree.

The pluggable transport initialized, but all observed bridge attempts remained TCP `SYN-SENT`; bootstrap stopped at 2%. The run ended with no residual process or listener and no default-route drift.

This falsifies another shortcut:

```text
public bridge configuration
+ working pluggable transport implementation
!= currently reachable bridge
```

It also demonstrates useful transport diversity: under the same current Route A substrate, dynamic Snowflake acquired real peers and reached a Tor relay while the bundled static obfs4 bridge population did not establish TCP connections.

## Connector P0 retained model

The experiments do not justify one public universal state enum yet, but they do require callers to preserve more than `connected=true|false`. A Connector observation may need to distinguish evidence such as:

```text
discovered / advertised
        ↓
path reachable
        ↓
transport established
        ↓
protocol relation established
        ↓
service usable
        ↓
degraded / expired / unavailable
```

These are observations, not authority upgrades. A relation may be real at one layer while a higher layer remains unusable.

Additional retained laws are:

```text
Connector implementation acquisition
!= Connector runtime acquisition

Connector A may compose with Connector B
without becoming the same authority object.

Connection evidence is path-, peer-, protocol- and time-bound.

Borrowed Connector acquisition latency and peer population
are part of external reality, not hidden retry noise.

A Connector may establish a real relationship and later degrade
without erasing the historical connection evidence.
```

## Connector P0 product decision

Connector P0 passes as a research falsifier of the boolean-connection model. It does **not** prove a production-grade borrowed Internet egress and does not justify:

```text
ConnectorManager
GlobalConnectionRegistry
AutomaticRelaySelection
AutomaticRouteMutation
UniversalConnectionStateMachine
```

The next Connector experiment should target a borrowed transport that reaches a bounded **usable-service** condition under current Route A/B constraints. Only then should an Effector experiment claim that a useful external action traversed the newly acquired Connector.
