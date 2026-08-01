# WXP-2 — Remote-to-Remote Artifact Movement

This comparison measures:

```text
B0 Host proxy
source → Host → object storage

B1 provider-native
Cloudflare Workflow → R2
Host receives Workflow status, ArtifactRef, digest, and result-manifest reference
```

The Host does not need to proxy source bytes when the next consumer accepts a verified Artifact reference. The experiment retains provider-native Workflow and R2 authority and rejects a separate World transfer service.

Deterministic run:

```bash
python3 experiment.py
python3 -m unittest -v test_experiment.py
```

Live run after the Workflow-capable Worker is deployed:

```bash
python3 live_trial.py \
  https://raw.githubusercontent.com/zycxfyh/ordivon-world/9b17ebffc8765a0e910c00cdacddcea89de4a970/README.md \
  --output evidence-live.json
```

The live trial independently downloads the immutable source for comparison, submits a durable evidence run, polls the original Workflow handle, and compares the Provider Artifact digest without downloading the source Artifact through the operational Host path.
