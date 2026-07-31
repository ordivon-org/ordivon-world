# World W1 — Host to Cloudflare response-loss comparison

This experiment implements the frozen contract in
[`../../docs/w1-experiment-contract.md`](../../docs/w1-experiment-contract.md).
It is not a production World service or a reusable schema.

## Compared arms

- **B0 direct:** Host uses the provider Request ID, Receipt endpoint, and Artifact
  verification directly. No correlation journal exists.
- **B1 correlation:** the same Host, provider, probe, request, fault, and verifier
  run with one additional experiment-local hash-chained correlation journal.

Both arms use `EffectLifecycleHost` from the exact pinned Ordivon Host revision.
The provider keeps request state, leases, Receipts, Artifacts, policy, and Worker
identity. The network module keeps the raw `ProbeResult`. The optional B1 journal
contains references and digests only.

## Fault

`dispatch` waits until the provider has returned a succeeded committed Receipt,
then discards the caller-visible result before Host admission. Host records
`UNKNOWN`. `resume` starts a fresh Python process, queries the original Receipt
before any POST, downloads and verifies the exact Artifact, applies the bounded
`Example Domain` predicate, and completes the original Task once.

## Deterministic tests

```bash
python -m unittest discover -s tests
```

The tests cover both arms, pending Receipt polling, false completion after an
Artifact mismatch, hash-chain tamper detection, and event identity rebinding.

## Live pair

From this directory after installation:

```bash
ordivon-world-w1 pair-live \
  --output-root artifacts/w1-live \
  --experiment-id w1-live-001 \
  --network wsl-current \
  --route host-current
```

The command runs one source-native `link-probe` observation, then starts separate
`dispatch` and `resume` processes for B0 and B1. It writes private per-arm Host
state and evidence plus `pair-report.json`. Provider credentials remain in the
existing client configuration and are never copied into experiment evidence.

## Retention rule

B1 is not retained merely because it works. The closeout must show a failure,
operator-cost reduction, recovery improvement, or necessary correlation that B0
cannot express without equivalent ad hoc state. Otherwise the result is to keep
Host plus provider/observation adapters and delete the correlation layer.
