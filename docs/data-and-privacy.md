# Data and Privacy

## Data ownership

World does not become the source of truth for connected systems. Data remains owned by the operator, the connected organization and the external provider that stores or processes it. World records only the provider requests, conditions, Receipts, Artifacts and Host references needed for reliable action and recovery.

## Stored data

| Location | Data | Retention owner |
|---|---|---|
| Host CAS/Journal | prepared Dispatch, uncertainty, mapped Receipt/Observation, Verification references | Host operator |
| Cloudflare R2 `requests/v2/` | pending/committed provider request state | R2 lifecycle policy |
| Cloudflare R2 `receipts/v2/` | best-effort Receipt mirror | R2 lifecycle policy |
| Cloudflare R2 Fetch/Browser paths | response bodies, screenshots, HTML and manifests | R2 lifecycle policy |
| Cloudflare R2 `cleanup/v2/` | deferred cleanup tombstones | R2 lifecycle policy and GC |
| `/root/backups/ordivon-world/` | private release and GC receipts | local operator |
| `target/acceptance/` | local commit-bound acceptance receipts | local operator; Git-ignored |
| systemd journal | controller result and bounded error text | local system policy |
| network measurement directories | route, egress and connectivity observations | local operator |

Current policy retains request state, Receipt mirrors and cleanup tombstones for 90 days and capability Artifacts for 91 days. The extra day prevents a replayable Receipt from outliving its lifecycle-managed Artifact.

## Sensitive content

Treat all external request URLs, Artifact bytes, Receipt metadata, network observations, source paths and identifiers as potentially sensitive. HTML, screenshots, documents and API responses can contain personal, proprietary or credential-bearing information even when the adapter does not recognize it.

World does not automatically redact:

- URL paths or query strings;
- fetched or rendered content;
- provider error metadata;
- Host Task/Effect/Dispatch identifiers;
- network egress and route facts;
- local source paths in private operational reports.

## Secrets

The following remain outside Git and must use mode `0600`:

- `/root/.config/ordivon/secrets/edge-client.json`;
- `/root/.config/ordivon/secrets/cloudflare.json`;
- WireGuard keys and rendered profiles.

Secrets must not enter Host CAS, provider Receipts, structured logs, acceptance receipts, command output or issue reports. The current HMAC Secret is a shared machine credential, not a user identity.

## Artifact handling

R2 remains private. Artifact reads are authenticated, returned as attachment bytes and verified against provider and Host SHA-256 values before use. Do not publish raw acceptance Artifacts or attach them to a public issue.

## Export and deletion

Before deleting or rotating provider state:

1. identify any pending or UNKNOWN Host Dispatch;
2. export Receipts and required Artifact digests;
3. reconcile or explicitly abandon the Host work under Host policy;
4. allow provider lifecycle or an authorized bounded deletion to remove bytes;
5. retain the minimal audit evidence required by the operator.

Deleting R2 state before the Host reconciliation window closes can make an uncertain external action permanently unverifiable.

## Sharing evidence

Before sharing a doctor report, Receipt or trace:

- remove source paths and account identifiers not needed for diagnosis;
- do not include Secrets, signatures or raw Artifact bytes;
- prefer digests and bounded identities;
- distinguish historical provider evidence from current capability observations;
- state whether the report was repository-only or live.
