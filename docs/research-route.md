# Research Route

## W0 — Carrier audit and experiment freeze

Status: completed by [`w0-carrier-inventory.md`](w0-carrier-inventory.md) and
[`w1-experiment-contract.md`](w1-experiment-contract.md).

W0 preserved both prototype histories and verified all current code, then
classified every major carrier as `retain`, `adapter-only`, `historical`, or
`delete-candidate`. No inherited Edge or Link type became an admitted World
schema. W1 is frozen before implementation.

## W1 — One Fetch response-loss comparison

Use one real Host research Task and one Cloudflare Fetch:

```text
Task / Attempt / Effect
→ one explicit HTTP/TLS path observation
→ stable provider Request ID and canonical Fetch payload
→ provider commits Receipt and Artifact
→ caller-visible response is discarded
→ fresh Host process queries the original Receipt before redispatch
→ exact Artifact retrieval and independent verification
→ continuation and exactly-once Task completion
```

Compare direct Host-to-provider integration with one minimum experiment-local
World correlation record. The path, provider, target, and capability remain
fixed. W1 closeout deletes fields and decides whether the responsibility belongs
in World, Host, provider adapters, or nowhere.

## W2 — Conditional capability negotiation and Effect rebinding

W2 remains inactive unless W1 reproduces a concrete failure caused by provider
capability mismatch, contract drift, or a valid need to rebind one still-open
Effect. When activated, compare static configuration, manual replacement through
native receipts, and the smallest explicit capability/binding decision.

No provider marketplace, universal broker, automatic routing, or blind
redispatch is authorized.

## Later work — only after W1/W2 evidence

A materially different second workload may test asynchronous participant
handoff or a programmable external Sandbox. Dynamic graph shapes, callbacks,
remote-to-remote Artifact movement, fan-out, and join remain later hypotheses.
They do not enter the first boundary decision.

## Architecture outcomes

- retain Ordivon World as a thin independent external-interaction layer;
- absorb the surviving semantics into Host and provider/observation adapters;
- retain only the Cloudflare product and private observation tools;
- freeze or delete abstractions that do not beat direct integration.
