# Contracts

## Contract authority

Public adapter documents use JSON Schema Draft 2020-12 under `src/ordivon_world/contracts/`. The schemas are packaged in the wheel and resolved through an in-memory Registry. Validation must not retrieve `ordivon.com` or another remote location during execution or recovery.

Published schemas:

| Schema | Purpose |
|---|---|
| `fetch-request` | bounded Cloudflare Fetch body |
| `browser-request` | bounded Browser Snapshot body |
| `edge-capabilities` | current provider capability and deployment condition |
| `edge-receipt` | pending or final provider Receipt |
| `world-prepared-dispatch` | durable Host-to-provider binding |
| `world-observation` | provider Receipt mapped to Host evidence |
| `network-observation` | future normalized read-only network condition evidence |

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

## Host mapping

`PreparedWorldDispatch` embeds a native Host `DispatchEnvelope` and records the capability condition as a required `StateRef`. `WorldObservation` embeds a native Host `ObservationEnvelope`; each provider Artifact becomes a Host `ArtifactRef` with provider key, media type and SHA-256 digest.

Provider success is not converted to a Host `VerificationReceipt`. Verification remains a separate domain or product action.

## Telemetry

`traceparent`, optional `tracestate` and an `x-ordivon-dispatch-id` header may accompany provider calls. They are not signed into the current provider request identity and are not durable evidence. Their sole purpose is correlation in logs and traces.

## Change policy

A contract change must update:

1. JSON Schema;
2. Python parser/mapping;
3. TypeScript fixture emission;
4. provider policy coupling where bounds changed;
5. compatibility documentation;
6. response-loss and stale-condition tests when semantics changed.

Run:

```bash
uv run python scripts/check_contracts.py
```
