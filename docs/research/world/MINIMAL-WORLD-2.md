# Minimal World 2.0 — Destructive Audit Closeout

This page is the current compact recovery surface for the 2026-08-28 **Minimal World 2.0 destructive audit**. It records what survived deletion/relocation pressure, what was retired, and why. It is not a new World architecture programme.

## Standing

**CLOSED / PRODUCT-BOUNDARY RE-ADJUDICATED.** The audit produced the `ordivon-world` 0.6 line by removing responsibilities that had become historical approximations while preserving all current consequence/recovery families.

| Surface | Verdict | Evidence / responsibility |
|---|---|---|
| `WorldTaskInspector.inspect_task()` | **RETAIN** | World-owned, revision-fenced projection of retained Provider/Resource/Message/Entity commitments; Host remains schema-blind and owns the namespace revision fence |
| `inspect_replacement_readiness()` | **RETIRE** | collapsed World relation standing into controller/morphology policy; Harness/controller owns the replacement judgment and must inherit exact outstanding reconciliation obligations |
| Resource Transfer semantics + JSON contracts | **RETAIN** | current Security production-side destination consumer plus exact UNKNOWN/Receipt recovery; Security emits/accepts the shared wire shape without importing World Python transport adapters |
| Message Delivery semantics + JSON contracts | **RETAIN** | current Security production-side destination consumer plus exact UNKNOWN/Receipt recovery; Security emits/accepts the shared wire shape without importing World Python transport adapters |
| World Python `resource_wire` / `message_wire` adapters | **RETIRE** | repository-wide production-import scan found no consumer; removing both adapters and their adapter-only tests preserves the Resource/Message trajectory core, packaged contracts, Host recovery, wheel surface and Security destination behavior |
| Entity Migration | **RETAIN** | current Security KVM/entity destination and reconciliation consumer; World also retains a production acceptance consumer of `entity_wire` |
| private `_host_trajectory` mechanics | **RETAIN** | already earned by three trajectory families; third-consumer pressure did not justify a public universal `WorldTrajectory` |
| transparent pre-P4/P5/M5 flat Host-state upgrader | **RETIRE** | current Host authority audit found zero `world` extension namespace rows; current v5 map state does not consume the upgrader |
| pre-HP5 `TraceContext` decoder | **RETAIN-FROZEN** | only 31 LOC and still protects readability/round-trip of separately retained historical `PreparedWorldDispatch`; no new work authors Trace Context |
| `ordivon-world-doctor` | **RETAIN / TIGHTEN** | fresh-Agent first interface with real current-health value; now validates the complete 25-schema package registry while consuming provider-native health/lifecycle projections |
| Cloudflare provider repository co-location | **RETAIN-COLOCATED / EXTRACTABLE** | provider authority is already separate and HP5 proved physical extraction; 2026-08-04→28 change census found 181 non-merge commits with only 3 provider+World-core commits, concentrated in initial integration/HP5, so physical split does not currently repay migration cost |
| root facade (14 names) | **RETAIN** | no fresh-Agent or maintenance evidence justified another cosmetic export-only contraction |

## Deletion result

The 0.6 contraction commit `b398d35f83ba3eb0772f269fc130c734dd54206c` removes 515 lines and adds 59, including:

- the World-owned replacement-readiness verdict and its product-specific E5 test/doc;
- transparent flat→map compatibility branches for provider/Resource/Message state;
- large compatibility fixtures whose only purpose was proving those historical automatic migrations.

Two compact regressions preserve the new boundary: encountering historical flat provider or Resource state fails closed with an explicit requirement to recover/migrate using a pre-0.6 client. Modern Provider/Resource/Message/Entity/Inspector recovery tests remain green.

A subsequent Existence Gauntlet 2.0 pass removed another **705 lines** of implementation/test residue: the unconsumed World Python `resource_wire` and `message_wire` adapters plus their adapter-only tests. The distinction is deliberate: **trajectory semantics and interoperable JSON wire contracts remain current; one unused World-side Python transport implementation does not.** Full World portable acceptance remained green at 115 Python tests plus the provider/packaging gates, and a separate Security regression passed 33/33 Resource/Message destination and surface tests, including explicit assertions that the destination CLIs do not import `ordivon_world`.

## Current Host evidence cut

A read-only Host integrity observation at the audit cut reported schema v5, 1,065 retained Tasks and healthy journal/CAS invariants. A direct read-only census of the authoritative `task_extension_state` table found **zero rows for namespace `world`**. This is source-fenced evidence for retiring the transparent upgrader; it is not a claim that future Host state can never contain World relations.

## Doctor / provider currentness finding

Live doctor dogfood proved the aggregation interface remains useful. Installed provider tools, secret-file mode, capabilities, R2 lifecycle and GC were current/healthy, while provider-native status identified the active Worker generation as built from older Worker release inputs (`a85a493...`). The current committed release digest changed only because `package.json` / `pnpm-lock.yaml` moved the build toolchain to `undici 7.29.0`; Worker TypeScript source, policy and Wrangler configuration were unchanged.

That deployment difference remains **provider-owned currentness**, not World failure. The provider release controller already defines zero-traffic candidate admission, version-bound Fetch+Browser smoke, promotion and rollback. This audit does not convert deployment currentness into World semantic authority.

## Reopen conditions

Reopen these contraction decisions only when one of the following appears:

- a real retained flat Host World state cannot be safely recovered with the documented pre-0.6 migration boundary;
- a consumer needs controller replacement standing that cannot be derived from World `inspect_task()` plus Harness/controller policy without duplicating World truth;
- a fourth materially different trajectory family produces repeated missing mechanics that the private helper cannot express without semantic duplication;
- Cloudflare provider change cadence or independent consumers make co-location create measurable coordination/release cost;
- a fresh-Agent trial shows the 14-name facade or doctor aggregation causes concrete wrong action/currentness interpretation.

Until then, the 0.6 boundary is: **retain consequence identity and owner-native recovery; delete policy verdicts and compatibility machinery whose consumers have disappeared.**
