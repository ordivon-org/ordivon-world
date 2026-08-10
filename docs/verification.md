# Verification

## Verification layers

### 1. Deterministic Python layer

```bash
uv lock --check
uv sync --locked
uv run python -m compileall -q src tests scripts
uvx ruff==0.15.17 check src tests scripts
uv run python -W error::ResourceWarning -m unittest discover -s tests -v
```

This proves request identity, Schema validation, capability fencing, Receipt mapping, Host CAS persistence and fresh-Host recovery under injected failures.

### 2. Cross-language contract layer

```bash
cd providers/cloudflare && pnpm install --frozen-lockfile && cd ../..
uv run python scripts/check_contracts.py
```

TypeScript emits current Capability and Receipt fixtures. Python validates them against packaged Schemas and checks Schema bounds against provider policy.

### 3. Provider layer

```bash
cd providers/cloudflare
pnpm run ci
```

This runs TypeScript type checking, provider state-machine tests, Python controller tests, policy coupling, systemd unit verification and Wrangler dry-run build.

### 4. Network operator layer

```bash
cd modules/network-observation
scripts/check-vpn-controller
```

This verifies command syntax, key/profile handling, namespace topology and profile scheduler behavior without exposing private keys.

### 5. Distribution layer

```bash
uv build --wheel --out-dir target/wheel
uv run python scripts/check_wheel.py target/wheel
```

The checker inspects metadata, exact Host revision, CLI entry point and packaged Schemas, then installs the wheel in an isolated virtual environment and imports the public facade without the source tree.

### 6. Operational layer

```bash
uv run ordivon-world-doctor --repo /root/projects/ordivon-world
```

This is the current machine/provider health projection. CI cannot substitute for it.

### 7. Live Fetch W1 and Browser P2 layers

[`operations.md`](operations.md) documents the commit-bound response-loss scenarios. Both receipts must prove:

- intent persisted before POST;
- one external POST;
- response discarded only after a committed provider Receipt was observed;
- Host recorded UNKNOWN;
- fresh Host recovered the same prepared Dispatch;
- reconciliation queried the original provider request ID;
- no redispatch occurred;
- Receipt request digest and capability version matched;
- Artifact bytes and digest were verified;
- acceptance-local VerificationReceipt accepted the evidence without being written as a Host core Event;
- Task state and Ready Frontier were preserved;
- no completion claim was made.

Browser P2 additionally requires exactly three Artifacts, Receipt-primary Manifest identity, one lease generation, PNG signature, UTF-8 HTML, Manifest equality with Receipt execution/page facts, and a Verification result item for every Artifact. It does not assert that the rendered page is semantically correct.

## Evidence interpretation

Passing tests prove the exercised failure trajectories. They do not prove every connected target is correct, safe or semantically useful. A Worker health response proves service reachability and current identity, not Task completion. A provider Receipt proves provider state under its contract; a domain verifier still decides whether the observed result satisfies the Task.

## Full portable gate

```bash
scripts/local-acceptance
```

This portable gate is necessary but not sufficient for a release/integration claim. Current Host ownership compatibility and live provider recovery remain separate owner-native gates exercised by the live W1/P2 scenarios above.
