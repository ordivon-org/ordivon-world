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


## Connector P1 and Effector P0: usable service is a separate proof boundary

Connector P0 proved that a real external relation may exist below service usability. Connector P1 therefore stopped asking whether a transport was merely connected and instead required a bounded service to carry one observable Agent action.

### Public volunteer transports remained below stable service usability

Two fresh Snowflake runs preserved the P0 relation proof but did not reach a usable SOCKS service. Workstation Direct Route A reacquired volunteer peers and reached 30% Tor bootstrap; Route B reached only 10%. The failures moved with the volunteer/broker relation rather than reducing to one route profile.

VPN Gate produced a different set of staged results. OpenVPN on the only currently reachable candidate completed TCP, certificate verification, TLS 1.3 and peer initiation, but did not receive `PUSH_REPLY`. A portable, signature-verified SSTP/PPP stack then reached further on the same public service without installing host packages.

SSTP exposed a useful distinction inside the protocol session itself:

```text
SSTP + MSCHAPv2
  → transport connected
  → authentication succeeded
  → no local IPv4 assignment

SSTP + PAP inside the same verified TLS session
  → transport connected
  → authentication succeeded
  → IPCP completed once
  → local IPv4 10.240.138.203
  → peer 1.0.0.1
```

The assigned PPP interface was real, but a fixed HTTPS action did not complete through it, and the same relay did not reproduce IPv4 assignment reliably in a later direct-path session. Therefore:

```text
protocol relation established
!= service usable

network interface/address assigned
!= forwarding verified
```

The public relay population itself also changed materially during the experiment. One expanded observation reported 98 current rows and returned 96 candidates; 90 `(host, IP)` pairs differed from an earlier 64-candidate snapshot. Fresh direct-path first-contact trials against previously unprobed JP and KR relays both became unreachable at TCP/443 and were confirmed unreachable by post-attempt probes. Discovery and reachability must therefore retain `observedAt` and cannot be promoted into durable capability grants.

### Request-scoped positive control completed the World loop

The public volunteer result does not imply that the Sense/Connect/Act model is unable to close. A separate positive control used an account-authorized temporary Cloudflare Worker as a **request-scoped external Connector**. The Worker accepted one fixed `/act` request and could fetch only `https://example.com/`; it was not a generic proxy.

The local Agent reached the Worker through `native-a`. The remote Connector then completed the fixed external GET and returned:

```text
upstream status = 200
body bytes      = 559
body sha256     = ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d
```

This proves one bounded closure:

```text
Agent
  ↓
Connector: account-authorized Cloudflare HTTPS relation
  ↓
Effector: fixed remote Fetch
  ↓
Observation: status + byte count + digest
```

The experiment deliberately does **not** relabel this as public-volunteer or host-wide Internet egress. It proves a narrower but more useful principle:

> An Agent may acquire exactly the external relationship required by the goal instead of first acquiring ownership of a complete network path.

### Workstation failure-domain discovery

Connector P1 also exposed a lower shared failure domain outside World ownership. During the experiment Surfshark WireGuard entered a half-dead state: its control structures and `/1` capture routes remained present while its handshake/data plane failed. Production and canary Cloudflare tunnels disappeared within roughly the same second because they still depended on the same lower Workstation/network substrate.

Stopping only the WireGuard child service or recycling the Surfshark main service recreated the captured structure without proving restored data flow. An explicit emergency direct window—stopping the Surfshark application and services—restored Windows direct reachability and destination-specific WSL paths. After the experiment, Surfshark was restored through its own UI `Connect` control; the WireGuard service, split routes and Windows/WSL ambient HTTPS were re-observed as usable.

This yields a cross-project requirement rather than new World route authority:

```text
multiple Connector identities
!= independent redundancy

if they share the same captured lower egress substrate
```

Workstation should own detection/recovery of that physical half-dead state. World should retain the resulting path-bound capability observations and let the Agent replan.

## Connector P1 / Effector P0 retained model

The strongest current model is now:

```text
Discover
  ↓
Acquire implementation
  ↓
Acquire relation
  ↓
Verify service usability
  ↓
Act
  ↓
Observe effect
  ↓
Reconcile
```

A lower-stage success must not be silently promoted to a higher stage. In particular:

```text
advertised != reachable
reachable != transport
transport != protocol relation
protocol relation != usable service
usable service != effect proven
```

Connector P1 still does not justify a global Connector manager, automatic relay selection or route mutation. The next experiments should prefer materially different real workloads over repeated relay enumeration. The request-scoped positive control is evidence that capability-granular external relationships are viable; repeated domain consumers are still required before extracting a shared production contract.


## W-X1 / W-X2: owner-observed foreign-egress capability and handoff

A 2026-08-10 experiment reused the Workstation-owned Surfpath schema-v2 substrate rather than moving VPN mechanics into World. The first saved observation was historically qualified but about 3,940 seconds old against Workstation's 180-second execution window. `surfpath status` therefore reported `fresh=false` and `executableNow=false`. World rejected that condition as current capability authority.

A complete 415-variant discovery then hit its bounded Runtime deadline at 180 seconds. A narrower owner-native refresh for the already relevant `jp-tok + openvpn-udp` family completed in about 39 seconds and produced two currently qualified paths. This is evidence for query-shaped refresh around candidate relationships, not for a global background route manager.

W-X1 explicitly selected one of those paths rather than accepting Workstation's advisory ranking implicitly. The selected relationship was:

```text
native-a
  → OpenVPN UDP
  → Surfshark jp-tok
  → exact endpoint 172.216.10.36:1194
  → observed JP/NRT egress 172.216.10.37
  → OpenAI HTTPS gate
```

World projected that owner observation into `ordivon.world.foreign-egress-capability`. The projection retains only the semantic relationship, owner observation/path/catalog digests, destination evidence and freshness window. It deliberately omits route-table/user mechanics, provider binary paths, authentication authority paths and raw VPN configuration. `activationAuthority` remains `ordivon.workstation.surfpath`, and every projection states `requiresOwnerRevalidation=true`.

The live W-X1 capability digest was `sha256:4c070368181602b2cf88d39ca18c48f23ca5a7b6fa8571fbb625f20506e998f8`, bound to Surfpath observation `sha256:327472b0046df888da2e573c6a59e9c8334d72212298f38885313e28dee77e4d` and selected path `sha256:ad19ae221df2a3028e8a16b554cf152194c6f383ab7a9a3f8c45d82adee6f5eb`.

W-X2 then opened a separate clean Runtime Workspace/Job context. That consumer received only the capability/observation/path digests and asked the Workstation owner to activate the selected relationship. It received no Surfshark username/password, OpenVPN auth file, private configuration or provider implementation path. Workstation revalidated the saved observation identity, current path binding and OpenAI destination gate before execution. A keyless `GET https://api.openai.com/v1/models` returned HTTP 401 through the selected JP egress, which is the expected bounded reachability result without API authority.

A negative control supplied the previous observation digest. Workstation rejected it before activation because the current saved observation identity had changed; the requested payload was never executed. Thus the handoff object is not a durable route grant.

The retained laws are:

```text
historically qualified path
!= current effect authority

World capability projection
= semantic relationship + owner evidence + time applicability

capability-reference handoff
!= secret transfer

fresh World reference
!= activation authority

activation
requires owner revalidation of current relationship and destination gate
```

W-X1/W-X2 justify the narrow `foreign-egress-capability` and `foreign-egress-capability-reference` contracts for this proven consumer. They still do **not** justify a generic Transfer framework, global capability router, automatic provider selection or persistent World-owned network session.


## W-X3 / P1: multi-provider effect-path semantics

W-X3 tested whether the already-proven Surfpath path and a materially different Cloudflare path justified one generic World capability object. The experiment instead forced a smaller shared view.

The prior Cloudflare fixed-target connector had successfully reached `https://api.openai.com/v1/models`, but a later current-state probe could not resolve its hostname. Cloudflare's owner API then reported the exact DNS record, Worker route and Worker as absent (`404`). Historical effect evidence therefore did not survive as current capability authority.

A fresh fixed-target connector was created. Before any effect, a point-in-time Cloudflare owner observation proved all three exact resources present and bound the route to the observed Worker/host. That still did not prove destination capability: the first exact `/act` returned HTTP `522 connection_timeout`. A retry through the **same resource identity** then completed the fixed OpenAI GET and observed upstream HTTP `401`; the edge observation was `LHR` with ingress country `GB`. Cleanup deleted the route, DNS record and Worker and re-observed absence.

Together with W-X1/W-X2, the cross-provider evidence is:

```text
historical successful effect
!= current capability

owner resource exists
!= usable relation

usable relation
!= current action authority

owner-native currentness laws may differ

shared Agent view
!= shared capability ownership
```

Surfpath owns an explicit 180-second freshness horizon. The Cloudflare control-plane experiment proved point-in-time resource existence but no equivalent TTL; World therefore must not fabricate a common `freshUntil` law. Conversely, both paths require current owner revalidation before a new effect even when historical usability evidence exists.

The retained production abstraction is `EffectPathQuery` rather than a generic Capability registry. Each candidate preserves its provider-native source projection and exposes only the coordinates needed by the Agent to compare paths: exact effect/target, owner and activation authority, request-control mode, owner observation identity/time, optional owner-native validity horizon and successful usability evidence. The query is deterministic for hashing but has no ranking or recommendation. `selectionAuthority=agent`; every candidate states `currentActionAuthority=false` and `requiresOwnerRevalidation=true`; action begins only after the Agent selects one exact `candidateDigest` and the activation owner revalidates it.

This is the current Agent-first composition rule:

```text
owner observation / provider-native evidence
        ↓
EffectPathQuery
        ↓
Agent exact selection
        ↓
owner revalidation
        ↓
Act
        ↓
Observe / Reconcile
```

W-X3 therefore supports **shared query semantics across heterogeneous Worlds**, but rejects, for now, a global capability database, automatic provider router, universal freshness law or hidden ranking policy.


## P2: provider occurrence versus World observation availability

P2 tested whether existing provider/Host evidence was already sufficient for an Agent to distinguish when an external effect occurred from when its observation became usable inside World. The experiment used the existing Cloudflare Fetch response-loss path rather than inventing a generic observation model.

Before the change, a real committed Fetch Receipt reported provider completion at `2026-08-10T06:56:19.348Z`. The caller lost the committed response, Host retained UNKNOWN, the experiment deliberately delayed reconciliation by four seconds, and Host finally admitted the recovered observation about 10.8 seconds after provider completion. Raw Host revision timing could reconstruct the later admission boundary, but `WorldObservation` retained no local availability coordinate and `WorldTaskInspector` exposed neither provider timing nor availability to the Agent. Thus the information was physically present across owners but not available as one bounded World projection.

The narrow repair added optional `WorldObservation.availableAt`, defined as the time when a validated complete provider observation first becomes available to the World controller. It did **not** add generic `observedAt`, `receivedAt`, `admittedAt`, `effectiveAt` or a universal Sensor/Observation type. Provider `started_at` / `completed_at` remain Cloudflare-owned; Host Event `recordedAt` remains Host-owned.

A fresh, non-replayed acceptance then used a new provider request identity. Cloudflare started the Fetch at `2026-08-10T07:04:37.367Z` and completed it at `07:04:39.956Z`. After committed-response loss and the bounded delay, the recovered observation first became available to World at `07:04:51.422995Z`; Host admitted it milliseconds later at approximately `07:04:51.455Z`. Reconciliation still performed no second POST.

The retained temporal laws are:

```text
provider execution time
!= World observation availability
!= Host admission time
!= Agent read time

availability
!= truth
!= freshness
!= current external state
!= action authority
!= Task completion

historical observation without availableAt
= unknown World availability time
not provider completion time

re-reading the same Receipt
!= a new availability occurrence
```

`WorldTaskInspector` therefore projects a bounded `temporalEvidence` view for retained provider observations: provider start/completion, World availability and the separate time sources that own those facts. It still reports `authority=not-granted-by-inspection` and `externalCurrentness=not-claimed`.

Repeated reconciliation exposed another subtle invariant. Because `availableAt` is local and dynamic, naively rebuilding the same provider observation later would change its CAS digest. World now treats the first retained equivalent provider observation as canonical: if a later reconcile returns the same Receipt and ObservationEnvelope, World returns the retained observation and original `availableAt` without advancing the Task revision; semantic drift still fails closed.

P2 therefore supports **temporal provenance as an owner-separated coordinate**, not a global time ontology. The next consumer should use these facts only when a real decision depends on evidence age or delayed availability; further time fields require another falsified gap.
