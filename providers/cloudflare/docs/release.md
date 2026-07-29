# Release and rollback

## Release invariant

Production releases must originate from a clean local `main` that exactly matches `origin/main`. The release controller reruns the complete CI suite before contacting Cloudflare.

## Versioned release flow

```text
verify clean main
→ pnpm run ci
→ wrangler versions upload
→ deploy old 100% + candidate 0%
→ version-override Health smoke
→ version-override Fetch smoke
→ version-override Browser smoke
→ promote candidate 100%
→ normal-route Health verification
→ write release receipt
```

The candidate receives no ordinary traffic during smoke. Requests carry:

```text
Cloudflare-Workers-Version-Overrides:
  ordivon-edge="<candidate-version-id>"
```

Health, Capabilities, and execution Receipts must report the candidate Worker version through `CF_VERSION_METADATA`; otherwise promotion is refused. Candidate Health and Capabilities must also report the locally derived policy fingerprint and retention contract.

Each immutable Worker Version is tagged as:

```text
git-<12-char-source>-src-<16-char-worker-input-sha256>-<unix-time>
```

The Worker-input digest covers committed `src`, policy, Wrangler configuration, package/lock files, and TypeScript configuration. `/health` exposes both parsed fields as `deployment_identity`. Rollback preserves the identity chain because it selects an existing immutable Worker Version. Legacy `git-<source>-<time>` tags remain readable with an unknown input digest.

## Failure behavior

If any smoke or promotion check fails after the 0% deployment is established, the controller restores the previous version to 100% and writes a failure receipt. The uploaded candidate may remain available for diagnosis but receives no traffic.

## Commands

```bash
python3 scripts/ordivon_edge_release.py release \
  --message "P1.5 transactional execution"
```

Rollback to the most recent different 100% deployment:

```bash
python3 scripts/ordivon_edge_release.py rollback
```

Rollback to an explicit Worker Version:

```bash
python3 scripts/ordivon_edge_release.py rollback \
  --version-id <worker-version-id>
```

Release and rollback receipts are stored root-only in:

```text
/root/backups/ordivon-edge/releases/
```

## Smoke Artifact policy

Release Fetch and Browser smoke operations use unique Request IDs and the public `example.com` allowlist target. Their Receipts and Artifacts follow normal R2 lifecycle rules.


## Control-plane recovery

Read-only Wrangler control-plane queries are retried with bounded exponential backoff. If a Worker Version was uploaded but a later query failed, resume it without creating another candidate:

```bash
python3 scripts/ordivon_edge_release.py release \
  --candidate-version-id <uploaded-worker-version-id> \
  --message "resume release"
```

The controller reads the candidate's Git source tag. It accepts an older source commit only when the Worker release inputs (`src`, policy, Wrangler config, package/lock files, and TypeScript config) are byte-equivalent to current `main`; documentation, tests, or release-controller-only changes do not force a duplicate Worker upload. The candidate still starts at 0% ordinary traffic and must pass the complete propagation, Policy, Retention, Fetch, and Browser smoke sequence.


## Control-plane implementation

Version and Deployment reads use the Cloudflare REST API directly. A 100% promotion or rollback also uses the Deployment API, with forced deployment enabled for rollback. The 0% candidate split remains a bounded Wrangler operation because the public API schema does not express zero-percent entries. Wrangler is placed in its own process group with a 30-second deadline; after normal exit, error, or timeout, the controller queries the Deployment API and treats the operation according to the actual Cloudflare state.
