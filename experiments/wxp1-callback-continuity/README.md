# WXP-1 — Callback Continuity

This deterministic comparison tests polling alone against authenticated callback wake-up plus provider inspection fallback.

The frozen invariant is:

```text
callback → wake or ignore
provider inspect → authoritative external status
Host Verification → Task completion
```

Faults include duplicate, lost, early, stale-generation, pre-registration, and acknowledgement-lost callbacks. The experiment does not model callbacks as completion evidence and does not add a World callback journal.

Run:

```bash
python3 experiment.py
python3 -m unittest -v test_experiment.py
```

The generated `evidence.json` records all trials, aggregate latency and state measurements, and the architecture disposition.
