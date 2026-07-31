# W1 Results — Direct Integration Won

Status: completed at implementation revision
`41024df17e70b41c84705bf59c7966d6c90609ef`

Authoritative summary: [`../evidence/w1/w1-live-20260731c.json`](../evidence/w1/w1-live-20260731c.json)

## Decision

W1 does **not** retain an independent World correlation layer.

The surviving composition is:

```text
Host
  owns Task, Effect, Dispatch, UNKNOWN, reconciliation frontier,
  Verification, Artifact acceptance, and TaskOutcome

Cloudflare provider adapter
  owns exact signed body, provider idempotency digest, Request ID,
  Receipt lookup, Artifact retrieval, and provider protocol validation

network observation adapter
  supplies one source-native ProbeResult projected into a Host StateRef
```

`ordivon-world` remains the repository carrying the real Cloudflare provider,
private network-observation tools, inherited research fixtures, and dated
experiments. W1 did not earn a required production layer, service, database,
World Interaction schema, or separate authority.

## Frozen comparison

Both arms used:

- the same public `https://example.com/` Fetch workload;
- one shared source-native HTTP/TLS observation;
- the same pinned Ordivon Host revision;
- the same Cloudflare deployment, policy, and `fetch.v2` capability;
- the same provider request payload and idempotency algorithm;
- the fault `after-provider-receipt-commit-before-host-admission`;
- a fresh Python process for reconciliation;
- the same independent Receipt, Artifact SHA-256, HTTP status, and bounded
  `Example Domain` verification.

The only B1 variable was a separate hash-chained correlation journal.

## Live result

| Measure | B0 direct | B1 correlation |
|---|---:|---:|
| provider POST attempts | 1 | 1 |
| provider executions | 1 | 1 |
| Receipt queries after restart | 1 | 1 |
| Artifact downloads | 1 | 1 |
| duplicate external Effects | 0 | 0 |
| unsafe redispatch attempts | 0 | 0 |
| Host events | 6 | 6 |
| Host objects | 14 | 14 |
| Host database bytes | 77,824 | 77,824 |
| exactly-once Task completion | yes | yes |
| operator interventions | 0 | 0 |
| recovery latency | 3,307 ms | 3,489 ms |
| extra correlation events | 0 | 6 |
| extra correlation bytes | 0 | 4,535 |

Both arms produced the same 559-byte content with SHA-256
`ff67a9d764d6a2367a187734e697f6a53217db9a21c101d410a113ca871a299d`.
The 182 ms latency difference is one live network sample and is not treated as a
performance result.

B1 reduced no Host state, provider state, recovery step, verification step, or
operator action. It added six duplicate events and a 169-line experiment journal
implementation.

## What each B1 field became

| B1 field | Disposition |
|---|---|
| experiment and arm identity | retain only in experiment evidence |
| Host Goal, Task, Effect, Dispatch references | Host already owns them |
| path observation ref and digest | Host `StateRef` plus probe adapter |
| provider endpoint, operation, Request ID, digest | provider adapter plus Host Dispatch |
| Receipt and Artifact references | provider Receipt plus Host Observation/Verification |
| response-loss event | experiment-only fault evidence |
| reconciliation event | delete from World; Host and provider already record it |
| verification and Task outcome | delete from World; Host is authoritative |
| correlation chain and head digest | no production owner; historical experiment only |

No candidate World field survived the deletion test.

## Negative evidence retained

The first live B0 attempt exposed an adapter error before Host admission: the
experiment labelled the exact body SHA-256 as the provider request digest, while
the provider correctly uses an idempotency digest over method, path, and body
SHA-256. The provider operation was not redispatched. Its original Receipt was
queried, its Artifact was verified, and the invalid Trial was retained.

This failure strengthened the boundary:

- provider-native digest semantics belong in the provider adapter;
- Host should bind the provider's authoritative digest rather than invent one;
- an experiment must not rewrite durable Host state to make a failed Trial look
  valid.

## W2 decision

W2 remains conditional and inactive. W1 fixed the provider, target, path, and
capability and reproduced no capability mismatch, contract drift, or legitimate
Effect-rebinding failure. The successful direct path is not evidence for a
broker, automatic provider selection, or rebinding protocol.

## Retained repository surfaces

- Cloudflare Fetch, Browser, R2, request state, Receipts, Artifacts, release, and
  operations remain real provider capabilities.
- `link-probe`, observer, and console remain source-native private observation
  tools.
- Network World, disposable Node, Security port, custom wire/QUIC, VPN, and
  transport work remain historical or private carriers.
- the W1 implementation remains under `experiments/` for reproducibility, not as
  production architecture.
