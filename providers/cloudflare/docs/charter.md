# Cloudflare Provider Charter

Status: active production provider adapter inside Ordivon World

This module provides bounded Cloudflare-native external execution and evidence. It owns Request IDs, request digests, execution leases, policy/capability revisions, pending/committed state, Receipts, Artifacts, release identity, rollback, retention, and cleanup.

It does not own Goal, Task, Attempt, Effect meaning, UNKNOWN, Verification, completion, generic placement, provider selection, connectivity, participant identity, or World continuity. Those remain with Host, source-native adapters, Runtime, and domain authorities.

Legacy Edge vocabulary and Node research are compatibility and historical surfaces. They do not establish a separate Edge layer.
