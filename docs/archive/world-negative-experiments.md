# World negative architecture experiments

The shared World authority experiments left active `main` after two independent programs failed to earn a World service, database, workflow engine, callback journal, artifact-transfer service, provider broker, or universal interaction schema.

The final pre-reduction source is immutable at:

```text
5e20e1ce44da418c159fa92e0655f6234db71e32
```

Create a disposable worktree to inspect or reproduce the closed experiments:

```bash
git worktree add /tmp/ordivon-world-negative 5e20e1ce44da418c159fa92e0655f6234db71e32
cd /tmp/ordivon-world-negative

# Direct Host/provider comparison
cd experiments/w1-host-cloudflare
uv sync --frozen
uv run python -m unittest discover -s tests -v

# Callback-continuity candidate
cd ../wxp1-callback-continuity
python3 experiment.py
python3 -m unittest -v test_experiment.py

# Remote-artifact candidate
cd ../wxp2-remote-artifact
python3 experiment.py
python3 -m unittest discover -p 'test_*.py' -v
```

The historical program statement is `docs/world-capability-program-v0.md` at the same revision. Current `main` retains only Cloudflare provider capabilities and private network operator tools because those have present operational consumers.

## Why this archive entry remains

A negative architecture result is useful only when its comparison can still be inspected. This page preserves revision-level reproducibility without returning closed experiments, generated portfolios, or their CI to the active repository. Delete it only when the exact revision and commands are carried by a durable external archive or the historical conclusion is intentionally withdrawn.
