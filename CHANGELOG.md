# Changelog

All notable changes are recorded here. The project follows a pre-1.0 compatibility policy described in [`docs/compatibility.md`](docs/compatibility.md).

## Unreleased

### Added

- Python `ordivon-world` package pinned to the public Host and Protocol graph;
- Host-facing Cloudflare adapter with deterministic Dispatch-to-request identity;
- Host CAS/Journal persistence for prepared Dispatches, UNKNOWN outcomes and mapped Observations;
- response-loss reconciliation through the original Cloudflare Receipt without redispatch;
- packaged Draft 2020-12 contracts and a local Schema Registry;
- cross-language TypeScript Capability and multi-state Receipt fixture validation;
- legacy W3C Trace Context validation/round-trip support for retained pre-HP5 dispatches;
- repository and live-system `ordivon-world-doctor`;
- wheel, dependency, documentation and local acceptance gates;
- clean-commit live Host→Cloudflare W1 acceptance scenario;
- Browser Manifest machine contract and three-Artifact bundle reader;
- Browser response-loss and fresh-Host continuity tests;
- bounded `WorldTaskInspector` owner projection: Provider/Resource/Message/Entity families interpret their own retained state and expose only commitment identity, state, bounded evidence digests and next owner operation; no payload/provenance/continuity body, authority grant or global Owner registry is introduced;
- Fetch/Browser dual-mode clean-revision acceptance runner;
- pinned GitHub CI, CodeQL, secret scanning and dependency automation;
- HP0–HP4 destructive survival evidence covering public-surface contraction, direct-Host consequence kill tests, rejected wire genericization and fresh-Agent projection A/B;
- HP5 provider/verification court evidence for Browser integrity, exact provider binding, Trace Context deletion, owner-native doctor projections and provider repository separation;
- HP6–HP8 survival evidence for research-knowledge GC, 96-invocation mixed chaos, and the Minimal World tournament.

### Fixed

- Host core Events no longer shadow outstanding World owner state: Provider, Resource, Message and Entity journals now read the schema-v5 Host `world` extension namespace, so fresh controllers can reconcile exact commitments after later Task checkpoints without redispatch;
- Cloudflare R2 cleanup enumeration now uses the current `per_page` List Objects parameter instead of the unsupported `limit` parameter;
- GC pagination tests now verify `prefix`, `per_page` and `cursor` behavior;
- the installed GC controller now completes successfully and remains scheduled by the active timer;
- relative Schema references resolve exclusively from packaged local resources;
- contract fixture type checking no longer changes the Worker release-input digest;
- Browser non-PNG output now fails before Artifact commit;
- Receipt construction and JSON Schema reject succeeded operations without their required evidence and reject evidence on failed or pending outcomes;
- zero-traffic Worker admission no longer treats one transient version-override hit as stable routing; read-only checks retry and every external smoke POST is guarded by three consecutive version-bound health observations;
- World doctor validates the complete packaged contract registry (25 schemas in the 0.6 line) rather than a stale seven-schema provider subset; the unused reserved `network-observation` public Schema remains removed.
- `WorldTaskInspector` now names its denial as `actionAuthority` and marks UNKNOWN reconciliation hints `without-redispatch`, after fresh-Agent HP4 runs reproduced ambiguity in the older generic wording.

### Changed

- The 0.6 line contracts legacy/replacement responsibilities: `WorldTaskInspector.inspect_task()` remains the World-owned read-only commitment/current-recovery projection, while controller replacement policy returns to Harness/the consuming controller; transparent pre-P4 Resource, pre-M5 Message and pre-P5 provider flat Host-state upgrades are retired after current Host authority showed zero `world` namespace rows. Encountering those historical flat states now fails closed and requires pre-0.6 recovery/migration. Current v5 namespace state and exact Receipt/UNKNOWN recovery semantics are unchanged.
- World doctor now validates all packaged contract schemas from the package registry and the documented Host compatibility fence follows the current locked Host revision.
- The Cloudflare provider remains provider-owned/extractable but co-located: change-coupling census found only three provider+World-core commits since initial integration, all concentrated in the early integration/HP5 period, so a repository split still does not earn its migration cost.
- The frozen 31-line pre-HP5 `TraceContext` decoder remains for durable historical dispatch readability; new dispatches still do not author or propagate Trace Context.

- The 0.5 line retires the demand-scoped `resource_discovery` / `ResourceOpportunityBoard` executable planning layer after repository-wide consumer search and deletion pressure found no current production consumer. Resource/Option/Capability research remains canonical doctrine; acquisition/value/priority reducers remain with consuming owners/domains.

- World is now described as a recoverable external capability adapter and condition-observation boundary rather than only a repository containing provider and workstation tools;
- the reactivated Host-facing seam remains an absorbed direct integration, not an independent World runtime or universal interaction layer;
- Worker source provenance and test-only TypeScript compilation scopes are kept separate;
- default Python facade contracted from 90 to 17 names in HP0–HP4 and then 17 to 14 in HP5; Browser bundle/config/legacy Trace helpers remain explicit module APIs rather than default exports;
- five inactive W5-A/W5-B falsifier scripts moved out of the active source surface while their evidence/docs/Git history remain;
- new provider dispatches omit/stop propagating W3C Trace Context; retained legacy trace values remain structurally readable;
- World doctor now consumes provider-owned capability and read-only lifecycle projections instead of duplicating Cloudflare control-plane logic;
- closed W4/W5/Sense-Connect-Act narratives moved to historical research with one compact current closeout authority;
- research-only Foreign Egress Capability / Effect Path Query Python modules and three packaged contracts were deleted after failing fresh-Agent decision-value and independent-consumer tests; packaged schemas contract from 28 to 25 and the product Python suite from 139 to 121 tests.

### Removed

- Unconsumed Python `resource_wire` and `message_wire` destination adapters and their adapter-only tests. Resource/Message trajectory semantics, packaged JSON contracts, Host-backed reconciliation, and Security-owned destination consumers remain; no current production repo imports the removed World adapter classes.
- pre-0.6 `WorldTaskInspector.inspect_replacement_readiness()` and transparent flat Host-extension auto-upgrade behavior. Migration: consume `inspect_task()` for World-owned outstanding commitment/recovery standing; let Harness/controller policy decide replacement. Recover/migrate separately retained pre-P4/P5/M5 flat World state with a pre-0.6 client before upgrading.
- pre-0.5 explicit `ordivon_world` Resource planning attributes and the `ordivon_world.resource_discovery` module. Migration: consume `docs/research/world/RESOURCE-AND-CAPABILITY.md` for shared semantic constraints and use the relevant owner/domain decision surface for acquisition, ranking, composition and value judgments. Retained provider Receipts and durable external trajectory semantics are unchanged.

### Verified

- the portable P0–P1 matrix covers Python, Worker, provider-controller, network, dependency audit, contract, documentation and isolated wheel installation gates;
- live doctor reports current installation, Worker inputs, R2 lifecycle, GC and network prerequisites as healthy;
- live W1 proves one external POST, injected response loss, Host UNKNOWN, fresh-Host reconciliation by the original request ID, digest-verified Artifact recovery, independent Verification and no Task completion claim;
- live P2 proves one first-execution Browser POST, committed-response loss, Host UNKNOWN, fresh-Host reconciliation, screenshot/HTML/Manifest integrity, three independent Verification items, preserved Task state and no completion claim;
- HP5 standalone-provider full CI passes outside the World Git root, while 139 World Python tests and wheel validation pass with the provider subtree absent;
- HP6 compact current knowledge retrieval answers 9/9 tested laws from ~75.9 KB versus 7/9 from ~191 KB of active historical prose;
- HP7 runs 96 shuffled mixed-failure invocations with zero failures; HP8 repeats the same 96 on Minimal World with zero failures;
- Minimal World passes 121 Python product/compatibility tests, 29 Provider TypeScript tests and the complete portable gate with exactly 25 packaged Schemas.
