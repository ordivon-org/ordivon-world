---
schema_version: 1
id: world.resource-ontology-r0-census
title: Resource Ontology R0 — Historical Ordivon Census
type: research
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
summary: Cross-domain historical census of real Ordivon resource episodes used to falsify future Resource definitions before ontology or production changes.
evidence_status: mixed
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.resource-option-capability-model
  - world.resource-opportunity-flywheel
---
# Resource Ontology R0 — Historical Ordivon Census

## 1. Question

R0 deliberately does **not** begin by defining `Resource`.

It asks:

> Across materially different Ordivon domains, what actually happened when something was discovered, possessed, withheld, acquired, composed, consumed, exhausted, invalidated, substituted, or reused as a resource?

The goal is to construct a sufficiently heterogeneous counterexample set for R1/R2. A future definition must explain these episodes without turning `Resource` into a synonym for “anything useful”.

R0 therefore records episodes first and postpones ontology.

## 2. Frozen evidence boundary

The census was assembled on 2026-08-15 from current owner-native repositories plus revision-fenced Host continuity records. The source repositories were observed at:

| Owner | Observed revision |
| --- | --- |
| World | `a76910f92f6d6af884e6f604c2f9d7001e81edf1` |
| Finance | `d9fdbfcbf2d578135587813cb9c8c14b640fbb40` |
| Game | `0c8581c6b5eebceaf33aeb8907fa91a8b53708dc` |
| Studio | `52f646022cc606985a63a5fd290c417fd337e80e` |
| Security | `6a7a8f9b22cb4995d436da2968b135248f8f6bb3` |
| Human | `f7725dfc9b391c3e9a0c509d49795994931c9d63` |
| Workstation | `85f904635e856612b78e8b13acc553b1e80d292a` |

Historical Host checkpoints are semantic evidence, not current Git truth. Where a checkpoint refers to an older owner revision, R0 uses it only for the historical episode that it records.

## 3. Sampling rule

The census intentionally samples different failure classes rather than maximizing case count from one project.

Required coverage includes:

- resource observed but not owned or authorized;
- resource owned but not currently accessible;
- resource accessible but not semantically useful;
- resource useful only for one workload or relation;
- apparent redundancy that collapses under a shared failure domain;
- a resource whose non-use preserves option value;
- a resource whose acquisition is rationally rejected or deferred;
- resources that become valuable only in composition;
- capability exported by one owner becoming a resource for another;
- information/evidence resources whose value depends on interpretation or transport;
- resource decay, stale observations, revoked authority, or lifecycle invalidation;
- negative results that themselves improve later selection.

The table below is **not** a taxonomy. `Pressure exposed` names the distinction that the episode forces a future model to explain.

---

# 4. Historical census

## A. World / acquisition / cross-owner resource semantics

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| W01 | Discovery source versus owner truth | Aggregators, indexes and catalogs can establish that an offer/resource was observed, but not current terms, quota, eligibility, license or permission. | discovery != authority; candidate != actionable resource | `docs/resource-opportunity-flywheel.md` §§1–2 |
| W02 | Required authority versus possessed authority | World split provider requirement, acquisition desirability and current possessed authority into separate coordinates. A positive-EV gated resource can be worth acquiring while still being unusable now. | requirement != acquisition decision != possession | `docs/resource-opportunity-flywheel.md` §2 |
| W03 | Parent entitlement unlocks children | One verified education/student entitlement can unlock many downstream developer offers; before the parent exists the children remain dependent acquisition candidates rather than independent usable resources. | prerequisite resource; complementarity; human-work compression | `docs/resource-opportunity-flywheel.md` §4; Host `task:world-open-knowledge-data-fabric-20260812` rev8 |
| W04 | Provider-specific acquisition failure | OCI Free Tier was a legitimate high-value candidate, but the current operator payment/eligibility path was rejected by the provider. The failure was retained as OCI-specific negative acquisition evidence instead of being generalized to unrelated providers. | acquirable-in-theory != eligible-now; negative evidence; non-generalization | Host `task:world-open-knowledge-data-fabric-20260812` rev8 |
| W05 | Signup transport versus resource value | A transient signup-page network failure is not allowed to erase the expected value of an otherwise legitimate entitlement; machine transport is qualified later when actual consumption begins. | access relation is time/path scoped; discovery/acquisition and machine consumption are different stages | `docs/resource-opportunity-flywheel.md` §7; Host rev8 above |
| W06 | HTTP success versus semantic utility | TCP/TLS/HTTP success can return error pages, stale endpoints, empty quota shells or nominal credits that do not serve a workload. World requires semantic consumption before `useful=true`. | reachable != useful; resource value is consumer-relative | `docs/resource-opportunity-flywheel.md` §9 |
| W07 | Historical admission versus current presence | Resource Transfer can retain a durable destination receipt even after the native destination bytes are deleted. The receipt proves historical semantic admission, not current resource presence. | historical evidence != current resource state; persistence has multiple meanings | `docs/w2-resource-transfer-production.md` §§5–6 |
| W08 | Capability becomes a higher-layer resource | Workstation scoped egress, Runtime contained execution and Harness cognition are capabilities at their native owner boundary but resources to Finance/Game/Security consumers. | Resource/Capability role is system-boundary relative | `docs/resource-option-capability-model.md` §7 |

## B. Workstation / network / infrastructure resource episodes

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| N01 | 415 Surfshark transport variants | The sanitized provider catalog exposed 142 logical nodes / 415 transport variants while current Surfpath execution evidence could still be stale or unqualified. Catalog growth did not create 415 usable egress capabilities. | catalog cardinality != current option count != capability | Workstation `README.md` NX8 |
| N02 | `native-a` and `native-b` can converge | Two loopback transport profiles can exist while both descend through one native physical WAN/access domain. | nominal alternatives != failure-domain-independent redundancy | Workstation `README.md` network profiles; World resource model §4 |
| N03 | 98 public VPN candidates versus one admitted root | A fresh VPN Gate directory exposed 98 candidates across many countries/operators, but physical qualification and exact admission were still required and only bounded candidates became roots. | candidate universe != executable resource stock | Workstation `README.md` NX6 |
| N04 | Snowflake broker success but no shared capacity | A pinned Tor/Lyrebird client could reach the broker and create offers while the broker reported no volunteer proxies. The resource remained known/testable but currently `UNAVAILABLE`. | executable client != available shared resource; capacity is separate | Workstation `README.md` NX1 |
| N05 | Same public mechanism, different parent relation | Direct Snowflake attempts failed in one relation while the same pinned client inside an admitted JP outpost bootstrapped and served traffic. | actionability is relation/path/context dependent, not intrinsic to the nominal resource | Workstation `README.md` NX4 |
| N06 | Different roots but shared physical access | Root A and B used different route profiles, protocols, nodes and endpoints, yet shared the same local gateway/MAC and Surfshark provider. The retained claim was graph/lifecycle diversity, not physical/provider independence. | diversity has dimensions; redundancy depends on relevant disturbance class | Workstation `README.md` NX5 |
| N07 | Public observation expansion without capability expansion | NX8 reached 24/24 current read-only resources across 12 observation owners while current capability coverage stayed 18/22 slots. More observers improved owner/mechanism/method diversity without creating new capability classes. | resource abundance can improve evidence robustness without increasing effect capability | Workstation `README.md` NX8 |
| N08 | Large public datasets left indexed | M-Lab raw data requires AUP/authenticated access; Censored Planet bulk data can impose requester-pays costs. Bounded APIs already satisfied current high-value truths, so bulk data remained indexed/query-on-demand instead of mirrored. | acquisition/storage/utilization can be irrational when marginal capability is zero | Workstation `README.md` NX7 |
| N09 | Historical child resource invalidated by parent change | A child external observation retained its own historical `AVAILABLE` fact, but stopping/replacing the parent Anchor caused current projection to become `UNKNOWN`; fresh discovery was required. | dependency currentness; historical truth survives while current option dies | Workstation `README.md` NX0.1/NX2 |
| N10 | Failed WARP experiment becomes search memory | A Cloudflare WARP experiment failed to realize a current usable L3 path; cleanup was exact, but the candidate was retained with a lower current-context score and explicit reconsideration triggers. | failed consumption can become Knowledge Resource; retirement can be conditional | Workstation `README.md` NX8 Validation Memory |
| N11 | Stable consumer resource over replaceable physical members | `finance-okx` presents a stable loopback consumer identity while Workstation owns replaceable member leases/generations underneath. A member/path may change without changing Finance's semantic resource identity. | abstraction boundary; stable resource contract can sit over renewable physical options | Workstation `README.md` egress-pool / exterior-connect |
| N12 | Installed capability deliberately excluded from ambient authority | Workstation removed stale user-scope Node/uv/PNPM paths from ambient execution authority while retaining exact installations or historical interpreters where active consumers still required them. | possession != ambient authority; retirement depends on dependencies, not age alone | Workstation `README.md` provider convergence / recovery paths |

## C. Finance / information / capital research resources

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| F01 | SEC EDGAR public data | SEC submissions/XBRL are current machine-readable and require no API key, but fair-access policy, identifying user-agent rules and immutable source snapshots still govern use. Public access does not grant trading authority. | public information resource != unrestricted use != effect authority | Host `task:finance-open-public-data-fabric-20260812` rev2 |
| F02 | FRED high-value but gated | FRED/ALFRED is considered high-value economic data, but current API use requires a user-held account/key authority. It remains a candidate until that authority is acquired. | known high-value resource != actionable resource | Host `task:finance-open-public-data-fabric-20260812` rev2 |
| F03 | Source bytes versus research evidence | Finance requires immutable filing/source snapshots before derived research signals. The same reachable upstream data is not yet attributable evidence until exact source identity is frozen. | observation bytes != research-grade evidence | Host Finance public-data rev2 |
| F04 | Large resource universe collapses through research | APF audit observed thousands of available resource candidates compress into a small set of information families/hypotheses, with no out-of-sample survivor and therefore no shadow/capital decision. The zero-trade outcome was valid research. | information abundance != hypothesis quality != capital capability; null outcomes are knowledge | `task:finance:alpha-production-foundations-root-20260815` / APF owner evidence |
| F05 | Workstation egress as Finance resource | Finance consumes `finance-okx` as a narrow available egress capability rather than owning Surfshark nodes, resolver mechanics or tunnel generations. | lower-layer capability becomes a higher-layer resource; implementation should sink below consumer | World resource model §7; Workstation egress-pool evidence |

## D. Studio / professional equipment / creative resources

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| S01 | REAPER crossed from installed tool to proven production resource | Official REAPER 7.78 was not promoted merely because it launched. ReaScript created native project state and an independent render reconstructed an exact WAV. | installation != capability; native editable state + reproducible effect matters | Host `task:studio:capability-expansion-tool-consumption-20260814` rev3 |
| S02 | OBS capability without permanent listener | OBS/obs-websocket was dogfooded through authenticated scene observe/mutate and then restored byte-exact with the websocket server disabled and no listener. | useful capability need not imply permanent utilization/presence; dormant resources can be safer | Studio capability-expansion rev3 |
| S03 | Blender exit code zero with failed work | Blender dogfood found that a Python traceback can coexist with exit code zero. Artifact/state postconditions were required before the tool counted as successful production equipment. | process success != semantic effect; resource consumption needs outcome evidence | Studio capability-expansion rev3 |
| S04 | One successful equipment encounter produced only provisional medium status | Blender and OBS established real spatial/live worlds, but Studio promoted those media only to `provisional`; mature craft profiles still require real works. | tool capability != domain mastery/value capability | Studio capability-expansion rev3 |
| S05 | Figma installed/configured but OAuth consent absent | Figma was installed and official Remote MCP OAuth initiation worked, yet user consent remained incomplete, so no design read/write capability was claimed. | installed/configured != possessed authority != actionable capability | Studio capability-expansion rev3 |
| S06 | TouchDesigner remains a high-information candidate | TouchDesigner could add a materially new realtime operator/dataflow world, but account/license authority was absent. It remained a valuable candidate rather than being installed to improve tool count. | option value can exist before acquisition; authority is a separate relation | Studio capability-expansion rev3 |
| S07 | Inkscape deliberately not acquired | Inkscape was withheld because current SVG+rsvg plus higher-information pending Figma work left little marginal information/capability gain. | available resource can have negative/zero marginal acquisition value | Studio capability-expansion rev3 |

## E. Game / assets / cognition / content resources

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| G01 | CC0 catalog still needs exact asset identity | Kenney and Poly Haven are strong CC0 seeds, but site metadata/logos are not automatically covered merely because downloadable assets are CC0. | source/catalog label != exact resource authority/license | Host `task:game-open-asset-fabric-20260812` rev2 |
| G02 | Freesound is not one legal resource class | Freesound contains CC0, CC-BY and CC-BY-NC items. Each sound's exact license determines whether it is actionable for a commercial-capable output. | shared source != homogeneous resource semantics | Game asset-fabric rev2 |
| G03 | Live Agent cognition is operational but value-unproven | Current matched Station Zero experiments proved live DeepSeek decisions diverge materially from fixture trajectories with successful provider calls, yet additional player value remains unproven. | expensive capability difference != outcome/value difference | `docs/STATION_ZERO_V3_DOMAIN_VALUE_GV.md` GV6 |
| G04 | Cheaper fixture remains a meaningful substitute | Fixture/policy actors preserve a playable baseline and some decision structure, making them a legitimate counterfactual resource against live cognition rather than merely a test stub. | resources can be partially substitutable; marginal value must be measured | Game GV6 |
| G05 | Two Scenario Cases did not equal two broad experiences | Production had two Cases, but Junction Bottleneck differed by one exact topology delta. Case count was therefore not accepted as replay/content breadth. | resource/content count != diversity of reachable experience states | Game GV0/GV5 |
| G06 | Existing content levers generated new research archetypes without new core | Existing topology, pressure and placement resources were recomposed into mechanically distinct research archetypes without adding a mission factory or new World rules. | complementarity/composition can create capability/option value from existing resources | Game GV5 |

## F. Security / evidence / sample / authority resources

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| Q01 | Public vulnerability intelligence is read-only resource, not exploit authority | OSV, CISA KEV and NVD were machine-readable and useful for observation/prioritization while explicitly granting no authority to probe or exploit third-party systems. | information resource != action authority | Host `task:security-open-defense-data-fabric-20260812` rev2 |
| Q02 | Provider claim and Security truth remain separate | Security Research Corpus records provider claims, source snapshots and case evidence but does not promote an upstream classification into independent Security truth. | evidence resource has provenance/truth-role; ingestion != belief/knowledge promotion | `research/corpus/README.md` |
| Q03 | Sample metadata/materialization never grants execution authority | A sample can be cataloged and even materialized in SampleVault while `executionAdmission` remains denied by default. | possession of dangerous resource != authority to consume it through execution | Security corpus README |
| Q04 | Large retained sample need not be duplicated into every research store | A retained case references an exact ~7.4 GiB archive identity/history without copying the bytes into the Git corpus. | local materialization/storage count != knowledge availability; references can preserve option value | Security corpus README |
| Q05 | libvirt was available but intentionally deferred | Security found legitimate feature overlap with libvirt but retained local exact QMP/process/ledger/recovery semantics because libvirt would add another state owner before deleting enough plumbing. | mature available tool can reduce net capability through coordination/authority cost | `research/tool-surface/TS9-VIRTUALIZATION-DISPLACEMENT.md` |
| Q06 | Remote entitlement and remote capability are different resources | CA-LIC experiments showed that a remote license/entitlement decision can leave the protected capability local, whereas external primitive/remote capability moves necessary secret/operation outside the client trust domain. | authority carrier != capability location; superficially similar resources have different causal roles | `research/ca-lic/WORLD_MODEL.md` |

## G. Human / knowledge / attention / joint-system resources

| ID | Episode | What actually happened | Pressure exposed | Evidence anchor |
| --- | --- | --- | --- | --- |
| H01 | Generic `resource` role was deleted from Human's minimum model | Human M0 found that money, time, roles, rights, relationships, access and tools did not form one useful universal variable role; they were represented question-specifically as situated state/context. | over-broad Resource ontology can reduce explanatory power | Human `methods/m0/MODEL-DELETION.md` |
| H02 | The same tool changes role with the question | Human's retained dynamic model states that a tool can be context, intervention or part of a joint system depending on the study. | resource role is relational/question-dependent rather than intrinsic | Human `methods/m0/DYNAMIC-RESEARCH-MODEL.md` |
| H03 | Model output, joint-system capability and retained Human capability diverge | Human research treats an Agent/model as a real joint-system resource while refusing to infer that its output has become retained individual knowledge or skill. | resource-assisted effect != internal capability transfer | Human `HUMAN-AI-CAPABILITY-TRANSFER.md`; Host Human root rev8 |
| H04 | Not all generated knowledge should consume Human attention | AE1 allocates representations using Durability × Future Control Value plus an independent promotion gate; many Agent outputs remain external or locator-level rather than entering stable Human memory. | attention is scarce conversion capacity; maximum knowledge internalization/utilization is not optimal | Host `task:human:agentic-capability-root-20260814` rev8 |

---

# 5. Coverage check

R0 freezes **48 materially distinct episodes**:

```text
World/acquisition        8
Workstation/network     12
Finance                  5
Studio                   7
Game                     6
Security                 6
Human                    4
                       ----
Total                   48
```

The sample includes:

- positive acquisition and rejected acquisition;
- public, gated and human-mediated resources;
- physical transport, software, professional tools, capital information, game content, security evidence and human attention;
- current resources, stale resources and historical-only evidence;
- abundant catalogs and narrow capabilities;
- idle/dormant resources whose non-use is rational;
- independent and correlated alternatives;
- information resources and effectful resources;
- resources that require complementary bundles;
- lower-layer capabilities reused as higher-layer resources;
- failed experiments that become later search/selection knowledge.

This is broad enough to begin definition falsification, but not broad enough to claim a universal ontology.

---

# 6. R0 observations — hypotheses for R1/R2, not promoted laws

The following patterns recur often enough to become explicit hypotheses. R1 must compare them with external foundational theory; R2 must attack them with counterexamples.

## O1 — Resource appears relational

Across network paths, tools, licenses, data and Agent cognition, usefulness repeatedly depends on:

```text
something in Reality
× actor/system boundary
× target transition / question
× current context
```

The same nominal object can be valuable, irrelevant, blocked, hazardous or merely historical under different relations.

## O2 — “Exists” hides multiple proof boundaries

Repeatedly observed distinctions include:

```text
known / discovered
verified
eligible / acquirable
held / possessed
accessible / reachable
qualified
semantically useful
actionable for this workload
selected / composed
consumed
```

R0 does not yet assert that every resource family traverses one universal lifecycle.

## O3 — Resource abundance and resource diversity are different

415 transport variants, 98 VPN candidates, many public observation owners and multiple game cases repeatedly failed to equal capability, replay breadth or redundancy.

A future model must preserve at least:

```text
cardinality
!= actionability
!= substitutability
!= independence
!= capability coverage
```

## O4 — Non-use can be rational

Examples include:

- TouchDesigner/Figma before authority;
- Inkscape when incremental value is low;
- bulk public datasets when bounded queries satisfy the claim;
- OBS with the listener disabled outside bounded production;
- failed WARP retained as reconsiderable knowledge rather than repeatedly retried.

Utilization rate therefore cannot be the universal objective.

## O5 — Composition is often the missing conversion step

GitHub parent entitlement + child offers, network parent/child relations, Game content-axis compositions and tool-mediated Human×Agent work all show that resource value can be superadditive or dependency-bound.

A list of resources is therefore insufficient to predict capability.

## O6 — Currentness/decay is resource-family specific

Eligibility, authority, transport, resolver evidence, provider offer, sample presence, child relation, model/provider availability and consumer utility decay on different timescales.

One global “resource current” bit would erase important truth.

## O7 — Capability/Resource is boundary-relative

The strongest recurring example is:

```text
Workstation egress Capability
→ Finance Resource

Runtime execution Capability
→ domain execution Resource

Agent cognition Capability
→ Game/Finance/Security Resource
```

A future ontology must allow role recursion without transferring owner authority.

## O8 — Evidence and Knowledge are resources, but not ordinary effect authority

Negative acquisitions, WARP failure memory, public vulnerability intelligence, provider claims, APF null results and Human external research all change later selection without granting action authority.

This supports folding Evidence Ecology into the broader Resource study while preserving truth-role and transport boundaries.

## O9 — Acquisition can destroy value

Installing or activating a resource can add:

- maintenance;
- authority/state owners;
- attack surface;
- listener exposure;
- payment exposure;
- coordination cost;
- lock-in;
- expiry burden.

Therefore “resource acquired” is not monotonically positive.

## O10 — Effect and broader Outcome need separate treatment

Several domains can prove exact effects—network path established, render produced, browser turn committed, provider data fetched—without proving the broader goal-relative outcome such as alpha, player value, creative quality or durable Human learning.

The current World chain may therefore be too compressed at:

```text
Capability → Effect → Knowledge
```

R6 should explicitly test whether `Outcome` and `Attribution` are necessary intermediate concepts.

---

# 7. Definitions R0 explicitly refuses to promote

The census already falsifies several tempting definitions:

### “A Resource is anything that exists and could be useful.”

Too broad: it cannot distinguish unavailable shared capacity, stale authority, a denied sample, an unqualified VPN candidate or a tool whose acquisition reduces net capability.

### “A Resource is an asset Ordivon owns.”

Too narrow: public data, external services, human actions, relationships, licensed capabilities and owner-exported capabilities can all create real options without object ownership.

### “A Resource is anything currently usable.”

Too narrow: dormant tools, parent entitlements, deferred high-value candidates, historical evidence and real options can have value before immediate use.

### “A Resource is a Capability.”

False at one system boundary and circular across boundaries. Current evidence repeatedly distinguishes resource stock/relations from reliable state-transition capability, while allowing a lower owner's exported Capability to become a higher owner's Resource.

### “More resources are always better.”

Falsified by shared failure domains, coordination burden, authority cost, attack surface, low marginal information gain and provider/tool state proliferation.

---

# 8. R0 result

R0 does **not** produce a Resource ontology.

It produces a sufficiently adversarial empirical base for one.

The most important finding is methodological:

> Ordivon's historical resource failures are rarely failures of raw existence. They are failures or transformations of **relation**: authority, access, currentness, fit, capacity, dependency, composition, independence, semantic consumption, outcome or attribution.

That makes a purely object-centric resource model unlikely to survive R2.

The next admissible work is R1 foundational theory triangulation against these 48 cases, followed by R2 competing-definition falsification. No production World schema/API/registry is justified by R0.
