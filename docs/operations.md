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

This checks Git state and packaged contracts. Machine, Secret, provider, lifecycle, GC and network checks are explicitly marked `skipped`; they are never inferred from CI.

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
- R2 lifecycle rules against policy;
- GC timer and latest service result;
- private network tool prerequisites and key/profile consistency.

Any unresolved item produces `status: attention` and exit code 1.

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

The live scenario performs one bounded allowlisted Fetch, deliberately discards the successful POST response, replaces the Host process, queries the original Receipt, reads and verifies the Artifact, and records an independent Host VerificationReceipt without completing the Task.

It requires a clean source commit:

```bash
revision=$(git rev-parse HEAD)
uv run python scripts/live_host_cloudflare_w1.py \
  --source-repo /root/projects/ordivon-world \
  --source-revision "$revision" \
  --output "/root/projects/ordivon-world/target/acceptance/world-w1-${revision:0:7}.json"
```

The output is written with mode `0600`. It contains no Secret or Artifact body.

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

The scenario verifies one Browser POST, Host UNKNOWN, fresh-Host Receipt reconciliation, screenshot/HTML/Manifest download integrity, exact request generation and independent three-item Verification. A successful bundle still does not complete the Task or assert page truth.

## Recovery rules

- Transport failure after POST creates UNKNOWN.
- Never generate a new provider request ID merely because the response was lost.
- A fresh Host loads `PreparedWorldDispatch` from CAS and queries the original Receipt.
- A missing Receipt remains UNKNOWN and requires operator or domain policy; it is not automatic permission to retry.
- A changed capability condition fences delivery before POST.
- A mismatched Receipt ID, request digest, operation or capability version fails closed.
- Artifact bytes are accepted only when provider header, Host ArtifactRef and observed SHA-256 agree.

Provider deployment, lifecycle and rollback procedures remain in [`../providers/cloudflare/docs/operations.md`](../providers/cloudflare/docs/operations.md) and [`../providers/cloudflare/docs/release.md`](../providers/cloudflare/docs/release.md).
