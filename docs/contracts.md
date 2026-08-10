# Contracts

## Contract authority

Public adapter documents use JSON Schema Draft 2020-12 under `src/ordivon_world/contracts/`. The schemas are packaged in the wheel and resolved through an in-memory Registry. Validation must not retrieve `ordivon.com` or another remote location during execution or recovery.

Published schemas:

| Schema | Purpose |
|---|---|
| `fetch-request` | bounded Cloudflare Fetch body |
| `browser-request` | bounded Browser Snapshot body |
| `browser-manifest` | Browser screenshot and rendered-content bundle manifest |
| `edge-capabilities` | current provider capability and deployment condition |
| `edge-receipt` | pending or final provider Receipt |
| `world-prepared-dispatch` | durable Host-to-provider binding |
| `world-observation` | provider Receipt mapped to Host evidence plus optional backward-compatible World availability time |
| `network-observation` | future normalized read-only network condition evidence |
| `foreign-egress-capability` | World projection of one owner-observed, destination-qualified foreign-egress relationship |
| `foreign-egress-capability-reference` | digest-only handoff reference that requires activation-owner revalidation |
| `effect-path-query` | informational Agent-facing comparison of provider-native effect-path candidates; no ranking, selection or action authority |
| `entity-departure-receipt` | source-World authority for one exact local Presence departure |
| `entity-migration-plan` | exact migration/entity/source/destination/departure/continuity identity |
| `entity-migration-destination-request` | materialize/reconcile Entity destination request |
| `entity-migration-destination-response` | materialized, not-committed, unknown or rejected response |
| `entity-migration-receipt` | historical destination body-carrier materialization receipt |
| `entity-migration-not-committed` | native-substrate proof that exact original migration retry is safe |
| `message-issuance-receipt` | source-World issuance of one exact informational Message |
| `message-delivery-plan` | exact source/destination/provenance/payload Message identity |
| `message-delivery-destination-request` | deliver/reconcile destination wire request |
| `message-delivery-destination-response` | delivered, not-committed, missing or rejected response |
| `message-delivery-receipt` | historical destination Message admission receipt |
| `message-delivery-not-committed` | destination proof that exact original Message retry is safe |
| `resource-egress-receipt` | source-World admission of one exact Resource occurrence |
| `resource-transfer-plan` | exact source/destination/payload transfer identity |
| `resource-transfer-destination-request` | materialize/reconcile destination wire request |
| `resource-transfer-destination-response` | materialized, not-committed, missing or rejected response |
| `resource-transfer-receipt` | historical destination semantic-admission receipt |
| `resource-transfer-not-committed` | destination proof that exact original retry is safe |


## Resource Transfer contracts

`ResourceEgressReceipt` is produced by the native source authority and binds one source occurrence to one transfer, destination and portable payload digest. `PreparedResourceTransfer` binds the canonical egress receipt digest and payload digest. The destination request carries the exact egress receipt only for materialization; reconciliation carries only the retained plan identity.

A `not_committed` response is stronger than absence. It must bind the exact transfer/plan/destination/payload and explicitly state `exactOriginalRetrySafe=true`. World persists the proof before releasing UNKNOWN for the exact original retry.

Contract validation proves structure and identity binding. It does **not** by itself authenticate a source authority across an untrusted relay. The first Security consumer declares a `caller-trust-boundary`; stronger deployments must independently verify source authority.

## Message Delivery contracts

`MessageIssuanceReceipt` is produced by the source domain and binds one immutable `messageId` to a source/destination pair, Message kind, provenance digest, payload digest and source occurrence. Unlike Resource custody, the source occurrence is not consumed: one retained Fact may authorize multiple independently identified Messages.

`PreparedMessageDelivery` embeds the exact issuance receipt for production delivery. Security/destination admission is independent and management-classified; a delivery receipt proves Message-specific admission, not destination belief, knowledge or world-truth.

A Message `not_committed` proof is issued only under the exact destination message lock while no semantic admission record exists. World persists that proof before releasing UNKNOWN for an exact original retry.

Contract validation proves structure and semantic binding. It does not authenticate source authority through an untrusted relay. The first production Security consumer declares a caller trust boundary; endpoint/source authentication remains deployment-specific until more real consumers force a shared mechanism.

## Entity Migration contracts

`EntityDepartureReceipt` is source-domain authority for one exact World-local Presence departure. The first Game producer binds a verified retained `extract` consequence and permits one migration identity per departure occurrence. The receipt does not claim ownership of portable cognition.

`PreparedEntityMigration` binds the exact source departure digest and opaque continuity payload digest. Production materialization requires a typed departure receipt; reconciliation carries only the retained plan and never resends departure or continuity.

`EntityMigrationNotCommitted` is stronger than semantic receipt absence. It must bind migration, plan, entity, destination, source departure and continuity payload, and explicitly require both `exactOriginalRetrySafe=true` and `nativeSubstrateChecked=true`. The first Security consumer may issue that proof after a dead, provably body-free staged or TPM-only preparation is compensated to zero residuals. Ambiguous QEMU launch evidence remains UNKNOWN even when no QEMU PID was durably published.

`EntityMigrationReceipt` records a historical destination materialization. It does not assert that the body or Presence is live at a later time. Current recovery may repair publication after independent physical re-observation, but it does not rewrite predecessor ownership or replay an Entity body merely because a durable ledger exists.

The first Security consumer uses a pre-body KVM ledger fence, an opaque `ORDIVON_MIG` continuity disk and QMP/native evidence. Guest self-report is not migration authority. The first accepted production profile is a trusted local owner-originated caller: Game proves departure from retained native state and can re-read the same receipt in a fresh process, while Security still declares `sourceAuthorityAuthentication=caller-trust-boundary`. Structural source receipts do not authenticate themselves through an untrusted relay, and World does not translate them into destination authority.

## Deterministic identities

The provider request ID is derived from:

```text
Host Dispatch ID
+ Host Effect ID
+ provider operation
+ canonical request digest
```

The request ID does not contain the URL or Secret. Reconstructing the same prepared Dispatch after process replacement produces the same provider request ID.

Cloudflare separately derives its native semantic request digest from:

```text
ordivon-edge-idempotency-v1
POST
<provider-path>
<SHA256(canonical-body)>
```

Both identities are verified when a Receipt is mapped into a Host Observation.

## Capability conditions

`CapabilitySnapshot.condition_digest` includes:

- provider name;
- effective policy version;
- retention contract;
- capability IDs, versions and states;
- Worker Version identity;
- deployment source and Worker-input digest.

It excludes observation time. `observation_digest` includes `capturedAt` and identifies the specific observation event.

## Effect Path Query

`EffectPathQuery` is a read-only Agent-choice projection across provider-native candidate evidence. It is not a generic Capability contract and does not translate owner-specific mechanics into one authority model. Each `EffectPathCandidate` retains the complete provider-native `sourceProjection` while exposing only the comparison coordinates forced by W-X3: effect/target, owner and activation authority, request-control mode, owner observation identity/time, optional owner-native validity horizon and successful usability evidence.

`ownerObservation.validUntil` is nullable by design. Surfpath owns an explicit freshness horizon and therefore projects `freshUntil`; the request-scoped Cloudflare experiment proved only point-in-time resource currentness and no owner-native TTL, so World does not invent one. Historical success evidence remains historical even when the owner resources still exist, and resource existence alone does not prove a usable destination relation.

Every candidate serializes `currentActionAuthority=false` and `requiresOwnerRevalidation=true`. The query serializes `selectionAuthority=agent`, contains no rank/recommendation field and requires one exact `candidateDigest` for selection. Stable candidate ordering is canonicalization only, never policy.

## Provider observation availability

Cloudflare Receipt `started_at` and `completed_at` are provider-native timestamps. `WorldObservation.availableAt` is separately recorded by World when a validated complete Receipt first becomes locally available to the World controller. The field is optional in the schema so previously retained `world-observation` objects remain structurally valid; newly produced Cloudflare observations always emit it.

`availableAt` is deliberately not named `observedAt` or `admittedAt`: it does not rewrite provider occurrence/completion time and it does not duplicate Host event admission time. It is also not Agent read time, truth time, freshness, currentness or authority. `WorldTaskInspector` may project the provider timestamps and `availableAt` together as informational `temporalEvidence`, while continuing to report `authority=not-granted-by-inspection` and `externalCurrentness=not-claimed`.

Repeated observation of the same provider Receipt must not rewrite temporal history. When a Host dispatch already retains an equivalent Receipt/ObservationEnvelope, later reconciliation returns the first retained World observation and its original `availableAt`. A different provider Receipt or envelope still fails closed as superseded evidence.

## Host mapping

`PreparedWorldDispatch` embeds a native Host `DispatchEnvelope` and records the capability condition as a required `StateRef`. `WorldObservation` embeds a native Host `ObservationEnvelope`, the complete provider Receipt and optional World `availableAt`; each provider Artifact becomes a Host `ArtifactRef` with provider key, media type and SHA-256 digest. The Host event timestamp remains Host-owned and is not copied into this object.

Provider success is not converted to a Host `VerificationReceipt`. Verification remains a separate domain or product action.

## Browser bundle contract

A succeeded `browser.run` Receipt must carry exactly three generation-scoped Artifacts in this order:

1. `screenshot.png` with media type `image/png`;
2. `content.html` with media type `text/html; charset=utf-8`;
3. `manifest.json` with media type `application/json; charset=utf-8`.

The Manifest is the Receipt's primary Artifact and contains the first two Artifact references, execution identity and page facts. The Host-facing reader verifies Receipt, Manifest and downloaded bytes as one closed bundle. A failed, rejected or pending Receipt cannot carry operation evidence. These checks establish provenance and integrity only; they do not verify the truth or usefulness of rendered content.

## Telemetry

`traceparent`, optional `tracestate` and an `x-ordivon-dispatch-id` header may accompany provider calls. They are not signed into the current provider request identity and are not durable evidence. Their sole purpose is correlation in logs and traces.

## Change policy

A contract change must update:

1. JSON Schema;
2. Python parser/mapping;
3. cross-language fixture/producer validation where the contract has a non-Python producer;
4. provider policy coupling where bounds changed;
5. compatibility documentation;
6. response-loss and stale-condition tests when semantics changed.

Run:

```bash
uv run python scripts/check_contracts.py
```
