# Research Gaps and Evidence Frontier

The main gaps are no longer a wishlist for more body types. They are missing
evidence for the revised Task-to-external-execution responsibility.

## Current verified capability

- mature Cloudflare Fetch/Browser/R2 production provider;
- authoritative pending/committed request state;
- response-loss and ambiguous-write reconciliation;
- generation fencing and cleanup;
- exact provider policy and version binding;
- private Artifact export and Receipt replay;
- narrow local body lifecycle, evidence, reconstruction, and residual
  conformance experiment;
- Security lifecycle integration.

## Main unverified questions

| Question | Current state |
|---|---|
| Can one Host Effect bind exactly to the Cloudflare provider and replay after Host restart? | not demonstrated end to end |
| Which Placement Requirement fields generalize across Web research and software execution? | unknown |
| Does an external Binding layer outperform direct provider integration? | not compared |
| Can one Task continue across two different external providers using minimum sufficient state? | not demonstrated |
| Can parallel external bodies join without confused provenance? | not demonstrated |
| Does residual closure materially improve recovery or safety? | not measured |
| Is persistent Agent presence distinct from Task, participant, service, and provider identity? | unproven |

## Research order

1. Host-to-Cloudflare Effect binding and fault injection.
2. Two-workload Placement Requirement field derivation.
3. Direct integration versus Edge Binding comparison.
4. Cross-provider continuation benchmark.
5. Multi-body branch/join and residual closure.
6. Persistent presence falsification.

## Deferred classical mechanisms

The following are not Edge gaps and must remain supplied by mature systems:

- general container, VM, Sandbox, browser, device, scheduler, and cloud control
  planes;
- image management, package installation, writable workspace management, daemon
  supervision, multi-tenancy, and generic checkpoint/restore;
- network stack, VPN, CNI, proxy, service mesh, transport, and route control.

The local-unshare reference provider must remain narrow. A future real provider
may adapt established external systems only when required by the research
workload.
