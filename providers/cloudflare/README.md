# Ordivon Cloudflare Provider

A signed provider adapter for bounded remote Fetch and Browser work.

## Active capabilities

- `fetch.v2` — allowlisted HTTPS fetch with bounded redirects, time, and bytes;
- `browser.snapshot.v2` — same-origin Browser Rendering snapshot;
- `receipt.v2` — pending state, fenced leases, exact Request ID/input binding, replay, and reconciliation;
- private R2 Artifact retrieval with digest and byte verification;
- versioned release, rollback, lifecycle, and garbage collection.

The provider owns Cloudflare execution state and objects. It does not own Host Task meaning or completion.

## Commands

```bash
ordivon-edge health
ordivon-edge capabilities
ordivon-edge fetch https://example.com/
ordivon-edge browser-run https://example.com/ --full-page
ordivon-edge receipt <request-id> --wait
ordivon-edge artifact-get <key> --output ./artifact.bin --sha256 <digest>

sudo ordivon-edge-release release
sudo ordivon-edge-release rollback
sudo ordivon-edge-gc run
```

Installed operations resolve `/root/projects/ordivon-world/providers/cloudflare` by default. Override with `ORDIVON_WORLD_REPO` when necessary. Release and GC receipts are private under `/root/backups/ordivon-world/`.

## Release behavior

A release is skipped when the active Worker already has the same Worker-input digest. The controller accepts any reconstructable Git commit; unrelated repository state does not block a Worker release, while dirty Worker inputs do.

For a changed Worker, the controller uploads a zero-traffic candidate, verifies one version-bound health observation, checks policy and capability identity, runs only the affected Fetch or Browser smoke where the change is capability-local, promotes the candidate, verifies one non-override health observation, and writes a private receipt. Ambiguous control-plane responses are reconciled through Cloudflare before any retry.

## Why retained

Fetch and Browser could be called directly, but direct calls would lose Ordivon's stable signed Request ID, exact input binding, transactional Receipt, response-loss reconciliation, private Artifact contract, and source-input release identity. These are the adapter's non-replaceable functions.

See `docs/operations.md`, `docs/reliability.md`, `docs/release.md`, and `docs/security.md`.
