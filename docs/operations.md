# Operations

## Portable verification

```bash
uv sync --locked
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
scripts/local-acceptance
```

The portable gate does not require production Secrets or a live Cloudflare deployment.

## Repository-only doctor

```bash
uv run ordivon-world-doctor --repo . --offline
```

This checks Git state and packaged contracts. Machine, effect-client Secret, provider, lifecycle, GC and network checks are explicitly marked `skipped`; they are never inferred from CI.

## Live doctor

```bash
uv run ordivon-world-doctor --repo /root/projects/ordivon-world
```

The live report checks:

- repository HEAD and cleanliness;
- packaged contract Registry;
- installed controller digests against source;
- private configuration presence and `0600` modes;
- Worker health and source-input relation;
- live capabilities and condition digest;
- R2 lifecycle rules against policy through the provider-owned read-only `ordivon-edge-lifecycle --check` projection;
- GC timer and latest service result;
- private network tool prerequisites and key/profile consistency.

Any unresolved item produces `status: attention` and exit code 1.


Provider lifecycle ownership is explicit. The provider install materializes its policy to `/usr/local/lib/ordivon-world/edge-policy.json`, and World doctor checks that source/installed policy bytes match before consuming `ordivon-edge-lifecycle --check`. `ordivon-edge-lifecycle --check` performs one read-only provider control-plane observation and compares it with provider-owned policy; the World doctor consumes its JSON and does not read the Cloudflare control credential or call the R2 API itself. The same provider tool without `--check` remains the explicit mutation/apply path.

## Cloudflare garbage collection

The GC controller enumerates only `cleanup/v2/` tombstones using the current R2 List Objects contract:

```text
prefix=cleanup/v2/
per_page=<1..1000>
cursor=<opaque-next-page-token>
```

Install updated controllers from the provider directory:

```bash
cd /root/projects/ordivon-world/providers/cloudflare
sudo scripts/install-edge-operations
```

Run one bounded service execution and inspect the result:

```bash
sudo systemctl start ordivon-edge-gc.service
systemctl show ordivon-edge-gc.service \
  -p Result -p ExecMainStatus -p ActiveState -p SubState
journalctl -u ordivon-edge-gc.service -n 100 --no-pager
```

A successful oneshot service normally returns to `inactive` with `Result=success` and `ExecMainStatus=0`. The timer must remain `active`.

## Live W1 acceptance

The live scenario performs one bounded allowlisted Fetch, deliberately discards the successful POST response, replaces the Host process, queries the original Receipt, and reads and verifies the Artifact. It constructs an acceptance-local `VerificationReceipt` for evidence checking but does not write a Host core verification Event or complete the Task; World durable state remains limited to World-owned observation/reconciliation evidence. The acceptance Host state is persistent under `<output>.state` (or explicit `--state-root`) rather than a process-temporary directory, so a controller/job deadline cannot erase the exact prepared/UNKNOWN relation after an external Effect may already have committed.

It requires a clean source commit:

```bash
revision=$(git rev-parse HEAD)
uv run python scripts/live_host_cloudflare_w1.py \
  --source-repo /root/projects/ordivon-world \
  --source-revision "$revision" \
  --output "/root/projects/ordivon-world/target/acceptance/world-w1-${revision:0:7}.json"
```

The output is written with mode `0600`. It contains no Secret or Artifact body. The adjacent state root is local/private recovery evidence and must remain Git-ignored. If the first-execution wrapper is interrupted after the prepared/UNKNOWN state is durable, **do not rerun the first-execution path**. Reconcile the exact retained request instead:

```bash
uv run python scripts/live_host_cloudflare_w1.py \
  --source-repo /root/projects/ordivon-world \
  --source-revision "$revision" \
  --state-root "/root/projects/ordivon-world/target/acceptance/world-w1-${revision:0:7}.json.state" \
  --recover-only \
  --output "/root/projects/ordivon-world/target/acceptance/world-w1-${revision:0:7}-recovered.json"
```

`--recover-only` requires the retained UNKNOWN original dispatch and performs zero external POSTs; it queries the original provider Receipt and verifies its referenced Artifact(s).

## Live P2 Browser acceptance

After the committed Worker candidate has passed release-controller smoke and deployment, run the same response-loss schedule against Browser Snapshot:

```bash
revision=$(git rev-parse HEAD)
uv run python scripts/live_host_cloudflare_w1.py \
  --source-repo /root/projects/ordivon-world \
  --source-revision "$revision" \
  --operation browser \
  --output "/root/projects/ordivon-world/target/acceptance/world-p2-browser-${revision:0:7}.json"
```

The scenario verifies one Browser POST, Host UNKNOWN, fresh-Host Receipt reconciliation, screenshot/HTML/Manifest download integrity, exact request generation and an acceptance-local three-item VerificationReceipt. The receipt is evidence-checking data, not a Host core verification Event. A successful bundle still does not complete the Task or assert page truth.

## Recovery rules

- Transport failure after POST creates UNKNOWN.
- Never generate a new provider request ID merely because the response was lost.
- A fresh Host loads `PreparedWorldDispatch` from CAS and queries the original Receipt.
- A missing Receipt remains UNKNOWN and requires operator or domain policy; it is not automatic permission to retry.
- A changed capability condition fences delivery before POST.
- A mismatched Receipt ID, request digest, operation or capability version fails closed.
- Artifact bytes are accepted only when provider header, Host ArtifactRef and observed SHA-256 agree.

Provider deployment, lifecycle and rollback procedures remain in [`../providers/cloudflare/docs/operations.md`](../providers/cloudflare/docs/operations.md) and [`../providers/cloudflare/docs/release.md`](../providers/cloudflare/docs/release.md).
