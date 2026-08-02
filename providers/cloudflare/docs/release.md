# Release and rollback

## Release identity

A Worker release is identified by the committed tree of deployable inputs:

```text
src/
config/edge-policy.json
wrangler.jsonc
package.json
pnpm-lock.yaml
tsconfig.json
```

The version tag is:

```text
git-<source-prefix>-src-<worker-input-digest>-<time>
```

The source commit is provenance. The input digest decides whether a release changes the Worker. Documentation, tests, evidence, and release-tool-only changes do not require a new Worker version.

Dirty Worker inputs are rejected because they cannot be reconstructed. A branch, detached commit, unrelated dirty file, or commit not yet equal to `origin/main` is not rejected merely for organizational form.

## Flow

```text
read active Cloudflare version and deployment
→ return `no_change` when the input digest already matches
→ run local provider CI
→ upload one immutable candidate
→ deploy previous 100% + candidate 0%
→ observe candidate version once through an override
→ verify health, policy, capabilities, and affected operations
→ promote candidate 100%
→ observe promoted version once without override
→ write a private release receipt
```

One matching observation establishes the property checked. Repeating the same health request five times does not establish global propagation.

Fetch-only and Browser-only source changes run only their corresponding operation smoke. Shared routing, authentication, policy, configuration, dependency, or build changes run both. Local tests remain broader than deployment smoke because they exercise state-machine failure paths without creating remote Effects.

## Failure and reconciliation

Cloudflare Version and Deployment state is authoritative. If Wrangler times out after submitting a deployment, the controller queries the Deployment API before deciding whether to retry. It never assumes timeout means failure.

If admission fails after the 0% split exists, the previous version is restored to 100% and a failure receipt is written. An uploaded candidate may remain available for diagnosis but receives no ordinary traffic.

An already uploaded candidate may be resumed with:

```bash
sudo ordivon-edge-release release --candidate-version-id <version-id>
```

The candidate must carry the current Worker-input digest or point to a source tree with byte-equivalent Worker inputs.

## Commands

```bash
sudo ordivon-edge-release release --message "describe the Worker change"
sudo ordivon-edge-release rollback
sudo ordivon-edge-release rollback --version-id <version-id>
```

Private receipts are stored under `/root/backups/ordivon-world/cloudflare-releases/`.

## Why this controller remains

Wrangler uploads code but does not by itself preserve Ordivon's source-input identity, reconcile ambiguous zero-percent deployment responses, bind smoke results to the exact candidate version, restore the prior version after failed admission, or produce a private recovery receipt. Delete this controller only when a maintained deployment system provides those exact behaviors.
