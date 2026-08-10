---
schema_version: 1
id: world.w5.execution-mobility
title: W-X4 Execution Mobility Research Boundary
type: research
profile: engineering
lifecycle: active
source_role: current-research
visibility: public
owners:
  - ordivon-world
audience:
  - maintainer
  - builder
  - agent
summary: W-X4 tests whether one Host-owned objective can continue across materially different Runtime execution contexts while physical lineage remains Runtime-owned and already-admitted World effects reconcile instead of redispatching.
evidence_status: experimental
readiness: RESEARCH
applies_to:
  - ordivon-world
related:
  - world.w5.external-commitment-continuity
  - world.authority
---
# W-X4 Execution Mobility Research Boundary

## Starting question

W5-E fixed World durability at the first owner-admitted consequence boundary. W-X4 asks what happens when the Agent's physical execution context changes around that boundary:

> Can one semantic objective move between execution worlds without turning Runtime Workspace/process state into World truth, carrying stale pre-admission capability choices forward, or losing the exact identity of an external effect that may already have happened?

The tempting response is an `ExecutionMigrationManager`, shared execution-world registry or World-owned input/artifact transport. W-X4 tries to falsify those abstractions first.

## X4-A: Linux to Windows-native continuation

A canonical World workspace at source revision `e5e63116d4a2959588d0674b022dd1127ca25471` was used by two materially different Runtime execution providers. Both Runtime Jobs carried the same Host semantic Task reference.

Phase A ran under the Runtime `local_linux_runner_v1` provider and independently hashed canonical `README.md`:

```text
execution target  local_linux
source revision   e5e63116d4a2959588d0674b022dd1127ca25471
README SHA-256    sha256:bf25bdefef6750b81d7fb8619f291ed29a0fa469a268e198feeb2389dd09ec71
job               job-019feaff-5e67-77a0-8f46-3650c2278c57
stdout Artifact   sha256:5395da7c19fd08ab0e680af7e6789c29c98eda9df85055dacbcbb2bba59eeb02
```

Phase B ran under the configured Runtime `windows_native_launcher_v1` provider with a limited native Windows token. Its Runtime operation identity froze three opaque `foreignReferences`: the same Host Task, the Phase A Job ID and the Phase A stdout Artifact digest. Windows PowerShell accessed the UNC-projected WSL workspace and independently reproduced the exact same `README.md` digest.

```text
execution target  windows_native
provider          windows_native_launcher_v1
Windows authority limited
WSL distribution  archlinux
README SHA-256     sha256:bf25bdefef6750b81d7fb8619f291ed29a0fa469a268e198feeb2389dd09ec71
inputMatches       true
job                job-019feaff-9386-75b1-bcd3-a16367de8b3a
```

This proves a useful but narrow mobility property: canonical source bytes and exact upstream Runtime identities can survive a Linux → Windows-native continuation without World owning process, launcher, path or token mechanics.

It does **not** make filesystem semantics universal. A `cmd.exe` control rejected the UNC Workspace as its current directory and fell back, while PowerShell handled the same path. This is an execution-provider/tool property, not a World relationship that should be normalized behind a synthetic shared filesystem model.

## X4-B: immutable external input does not yet migrate to Windows-native

Canonical Git bytes are not equivalent to Runtime immutable external inputs. W-X4 therefore attempted the stronger boundary directly with `workspace.execBound` plus `executionTarget=windows_native`. Runtime rejected the request before commit:

```text
code        INVALID_REQUEST
commitState not_committed
field       execution.executionProfile
message     windows_native currently supports trusted_local only
```

The reason is structural: the public exact-input path selects Runtime `contained_local`, while the current Windows target accepts `trusted_local` only. Runtime source/docs also state that Windows-native immutable input bindings are not implemented.

This is a **Runtime substrate gap**, not a World contract gap. Runtime `foreignReferences` bind opaque identity/correlation into the execution plan and terminal evidence; they do not transport Artifact bytes and do not prove that the destination process consumed an external object. World must not paper over this by copying bytes through Agent arguments, environment variables, ad-hoc temporary files or a new World storage layer.

The requirement is tracked separately as Host continuity Task `task:runtime:windows-immutable-input-portability-20260810`.

## X4-C: migrate after the consequence boundary

The decisive experiment split one real Cloudflare Fetch across two fresh Runtime controller workspaces.

### Controller C: admit once, then lose the response

The source controller did **not** carry a P3 path selection forward. It freshly queried the Cloudflare provider capability and prepared a Fetch bound to its current capability condition. It then issued one exact POST. The provider committed a fresh non-replayed Receipt, but the transport deliberately discarded the successful response.

World/Host therefore retained:

```text
dispatchId               dispatch:world-wx4:1786354240743-e5e63116:r1
providerRequestId         world_69eff304e46190c5ef9a0f52051f24051dec38bd0183a563187b7c7614
capabilityConditionDigest sha256:fbb7aba00eda37385e386e97832d3a941b037292c34bbafa2273633d246d261f
external POST count       1
World outcome             UNKNOWN
```

The provider consequence existed independently of controller memory. At this point execution migration must preserve the exact admitted identity rather than re-plan a replacement effect.

### Controller D: fresh workspace, original-request reconciliation only

A separate Runtime workspace/process opened the retained Host/World state. It also queried the current provider capability for contemporary informational context, but that new observation did not authorize a new effect. Recovery loaded the original prepared dispatch and reconciled the original provider request ID.

```text
restored request   world_69eff304e46190c5ef9a0f52051f24051dec38bd0183a563187b7c7614
reconciled receipt world_69eff304e46190c5ef9a0f52051f24051dec38bd0183a563187b7c7614
reconcile GETs     2
recovery POSTs     0
status             succeeded
Task state         preserved
Ready Frontier     preserved
```

This is the P3 consequence-bound durability law surviving controller migration:

```text
before owner admission
    re-observe → re-query → re-select

after owner admission
    preserve exact effect identity
    → Receipt or UNKNOWN
    → reconcile original identity before retry
```

A fresh execution context is not a new authorization to repeat an old consequence.

## Ownership after W-X4

The experiment remained composable because each layer kept its own facts:

```text
Host
  semantic Task continuity / Ready Frontier / UNKNOWN meaning

Runtime
  execution target + provider
  Workspace / Job / Attempt
  source revision
  immutable inputs when supported
  Artifacts / terminal evidence
  foreignReferences as opaque correlation identity

World
  current external capability observation
  prepared external effect identity
  Receipt / UNKNOWN / reconciliation
```

No layer needs a second copy of another owner's state. Runtime Job or Workspace identity is not external authority; World capability is not an execution target; Host Task continuity is not a process-migration mechanism.

## Product decision

W-X4 does **not** justify:

```text
ExecutionMigrationManager
ExecutionWorldRegistry
World-owned Artifact transport
World filesystem/path translation
World-owned immutable-input materialization
generic failure-domain ontology
durable pre-admission path selection
```

The current World contracts already express the semantic part of migration. `ForeignEgressCapability` / `EffectPathQuery` remain recomputable before admission. Typed provider/transfer journals preserve already-admitted consequences. Runtime's own Job/Artifact/input evidence remains the physical lineage authority.

The one concrete missing substrate capability is outside World: exact `workspace.execBound`-grade external input materialization is not yet available to the Windows-native target.

## Limitations

- X4-A and X4-B are same-machine WSL/Windows execution-world changes, not remote multi-node migration.
- The Windows test proves canonical source-byte access and Runtime lineage, not portable external immutable-input bytes.
- X4-C/D used the production World/Host libraries and a durable local Host state root across fresh Runtime workspaces. The top-level MCP Host Task tracks the research objective, but the Cloudflare Effect journal in this experiment was not inserted into the separately deployed Host MCP service.
- Cloudflare was the post-admission effect family used for migration. Resource/Message/Entity families already share the same typed UNKNOWN/reconciliation skeleton but were not all repeated across Runtime targets.
- No shared failure-domain projection was forced by `cmd.exe` versus PowerShell or by Linux versus Windows provider mechanics.

[`../evidence/acceptance/wx4-execution-mobility-20260810.json`](../evidence/acceptance/wx4-execution-mobility-20260810.json) records the physical evidence.

## W-X4 stopping condition

World's semantic migration question is answered for the available machine: source-bound execution can cross Linux/Windows while Runtime retains exact target lineage; pre-admission World planning is recomputed; a committed-but-unobserved external effect survives controller migration through exact UNKNOWN reconciliation; and no World migration manager is needed.

W-X4 therefore closes at the World layer. The remaining exact external-input portability gap belongs to Runtime. A later cross-node/remote execution experiment should begin only when a second physical execution substrate can own equivalent input/artifact lineage; World should consume that evidence rather than pre-designing a multi-node manager.
