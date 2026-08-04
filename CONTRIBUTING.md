# Contributing

## Boundary first

A contribution must identify the current workload and the failure it prevents. Do not add a service, database, universal provider model, connector registry, automatic router or workflow layer merely because the abstraction is common elsewhere.

For a new provider or capability, state:

1. the Host Task and Effect that consume it;
2. the external authority and provider-native request identity;
3. what happens when delivery or response is uncertain;
4. which Receipt, Artifact or Observation proves the result;
5. how current conditions invalidate an old binding;
6. why an ordinary direct adapter is insufficient;
7. the deletion condition.

## Development setup

```bash
uv sync --locked
cd providers/cloudflare
pnpm install --frozen-lockfile
cd ../..
```

Run the complete portable gate:

```bash
scripts/local-acceptance
```

Run repository-only doctor output:

```bash
uv run ordivon-world-doctor --repo . --offline
```

Live checks require the target machine's private configuration and must not be added to ordinary pull-request CI.

## Change rules

- Persist intent before an external effect.
- Preserve one deterministic provider request ID across retries and process replacement.
- Reconcile UNKNOWN before another dispatch.
- Keep provider-native Receipt and error facts; do not invent generic success.
- Keep Task state, authority and completion in Host.
- Use packaged JSON Schema for public adapter contracts.
- Add TypeScript fixtures when a Worker contract changes.
- Bind tests to the failure trajectory, not source wording.
- Never add Secrets, private receipts, external Artifact bytes or raw network identity to Git.

## Tests required by change type

| Change | Required evidence |
|---|---|
| Python adapter or Host mapping | unit tests, fresh-Host recovery and wheel import |
| Worker request/Receipt | TypeScript state-machine tests and cross-language Schema gate |
| GC/lifecycle/release | focused controller tests and live read-only or bounded operational verification |
| network tools | static checks, namespace/key tests and no Secret disclosure |
| external effect/recovery | clean commit-bound live acceptance receipt |
| documentation only | documentation link and authority checks |

## Commit and release

Keep commits reviewable by responsibility. Do not force-push shared branches. A public release requires a clean commit, locked dependency graph, verified wheel, current operational status and a source-bound live acceptance receipt. Provider deployment and package release are independent: documentation or Host-adapter-only changes do not require a new Worker when deployable Worker inputs are unchanged.
