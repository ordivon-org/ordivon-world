# Agent instructions

## Scope

Ordivon Edge is the Task-to-external-execution continuity overlay above mature
providers. Its active research question is how one open Task binds an Attempt
or Effect to exact external execution, reconciles uncertain outcomes, exports
Artifacts and evidence, and continues across body or provider replacement.

The repository contains three deliberately different classes:

- **production provider** — Cloudflare Fetch, Browser Run, private R2 Artifacts,
  transactional request state, release, rollback, GC, and operations;
- **remote-effect reliability mechanisms** — request identity, pending/committed
  state, generation fencing, reconciliation, Receipt replay, provenance, and
  cleanup;
- **body/lifecycle research substrate** — provider-neutral Node contracts,
  deterministic lifecycle, local-unshare conformance body, Security control,
  reconstruction, and residual evidence.

The body/lifecycle substrate is a research hypothesis, not a proven permanent
Agent-native core. See `docs/research-route.md` and `docs/component-map.md`.

## Candidate vocabulary and ownership

- **Placement Requirement** describes what one Attempt or Effect needs from an
  external execution environment.
- **Provider Capability Observation** records versioned, time-bounded provider
  capability and limitation facts.
- **Placement Binding** relates exact Task/Attempt/Effect/Dispatch references to
  one provider, body or Sandbox generation, capability/policy revision, and
  provider execution identity.
- **Provider Execution** is the provider-native physical operation or body.
- **Semantic reconstruction** declares minimum sufficient inputs for continuing
  work elsewhere.
- **Residual evidence** records what remains after external execution ends.

These are research candidates, not frozen schemas.

The current code's **Node**, body, lifecycle, and generation terms remain valid
for the existing experiment. A Node must not be documented as a proven
long-lived Agent-presence identity. The current code has no complete independent
Sandbox abstraction.

Host or the semantic Kernel owns Goal, Task, Attempt, Effect, Dispatch,
verification, and work continuity. Runtime owns trusted-local Workspace, Job,
process, and recovery. Link owns connectivity. Providers own physical bodies,
images, Sandboxes, schedulers, snapshots, and native lifecycle.

## Route constraints

1. Preserve and harden the Cloudflare production provider.
2. Next integration evidence is one Host-consumable external Effect backend with
   exact Effect/Dispatch/provider execution/Receipt binding.
3. Derive Placement Requirement fields from at least two real workloads before
   defining a schema or automatic provider router.
4. Prove cross-provider continuation with minimum sufficient state before
   expanding body classes.
5. Revisit persistent Agent presence only after a real workload fails without
   it and Task, participant, service, or provider identity is insufficient.
6. Keep local-unshare frozen as a narrow conformance/reference body.

## Engineering rules

1. Do not add local route, VPN, DNS, WARP, TUN, path-selection, or
   transport-client code.
2. Do not reimplement Ordivon Runtime Task, process, Workspace, Artifact, or
   recovery lifecycle.
3. Do not build a container runtime, VM orchestrator, scheduler, browser,
   device platform, or generic Sandbox service.
4. Every executable capability needs authentication, authorization, budgets,
   and a Receipt.
5. External Fetch must reject unsupported schemes, unsafe ports,
   private/link-local destinations, unbounded redirects, and unbounded bodies.
6. Browser Run must have explicit time, action, and Artifact budgets.
7. R2 remains private by default; do not enable `r2.dev` or a public object route
   without review.
8. Never expose account IDs, bucket names, tokens, cookies, private URLs, raw
   external response bodies, lease tokens, or R2 ETags in status APIs, logs, or
   Receipts.
9. Keep platform adapters thin and stable contracts independently testable.
10. `pnpm check:boundary` must continue to reject Link/network code.
11. New execution outputs must be generation-scoped and committed through the
    authoritative request state.
12. Production release must use `scripts/ordivon_edge_release.py`; do not deploy
    directly from a feature branch.
13. Cleanup tasks may delete only matching-generation `fetch/v2` or
    `browser/v2` Artifacts.
14. Production, research, and adversarial-range profiles must have separate
    credentials, authority, and lifecycle policy.
15. Broad internal capability does not imply external authority; every remote
    action binds an explicit consequence profile.
16. The evaluated action must not control authoritative lifecycle, observer
    state, or destruction evidence.
17. Execution bounds, retention, and expected rate limits belong in
    `config/edge-policy.json`; do not introduce parallel constants.
18. Artifact downloads must fail closed on missing or mismatched SHA-256
    metadata and must not partially replace destinations.
19. Prefer Cloudflare REST control-plane APIs for reads, lifecycle, promotion,
    and rollback. Wrangler remains only where the public API cannot express the
    required operation, with time bounds and reconciliation.
20. Do not add a Sandbox type by relabeling the current Node, identity digest,
    local body, or lease generation.
21. Do not create an Edge/Link attachment schema until a real Host workload
    requires it and independent placement/connectivity revisions are understood.
22. Do not standardize or promote Placement vocabulary from documentation alone.

## Required checks

```bash
pnpm run ci
```
