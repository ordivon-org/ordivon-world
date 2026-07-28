import { readFile } from "node:fs/promises";

const policy = JSON.parse(
  await readFile(new URL("../config/edge-node-policy.json", import.meta.url), "utf8")
);
const productionPolicy = JSON.parse(
  await readFile(new URL("../config/edge-policy.json", import.meta.url), "utf8")
);
const productionPolicyModule = await readFile(
  new URL("../src/policy.ts", import.meta.url),
  "utf8"
);

function requireValue(condition, message) {
  if (!condition) throw new Error(message);
}

requireValue(policy.schema_version === 1, "unsupported Edge Node policy schema");
const profiles = policy.profiles;
requireValue(
  JSON.stringify(Object.keys(profiles).sort()) ===
    JSON.stringify(["adversarial-range", "production", "research"]),
  "all Edge Node profiles must have explicit policy"
);
requireValue(
  new Set(Object.values(profiles).map(({ authority_id }) => authority_id)).size === 3,
  "Edge Node profiles must not share authority"
);
requireValue(
  new Set(Object.values(profiles).map(({ credential_scope }) => credential_scope)).size === 3,
  "Edge Node profiles must not share credential scopes"
);
requireValue(
  profiles.production.provider === "cloudflare-worker" &&
    profiles.production.consequence_scope === "production-allowlist",
  "production Node profile drifted"
);
requireValue(
  profiles.research.provider === "local-unshare" &&
    profiles.research.credential_mode === "none" &&
    profiles.research.consequence_scope === "range-local-only" &&
    profiles.research.status === "implemented",
  "research Node profile must remain credential-free and range-local"
);
requireValue(
  profiles["adversarial-range"].provider === "deferred" &&
    profiles["adversarial-range"].consequence_scope === "range-local-only" &&
    profiles["adversarial-range"].status === "deferred",
  "adversarial-range must remain separately scoped and deferred"
);
for (const [name, value] of Object.entries(policy.local_unshare)) {
  requireValue(Number.isSafeInteger(value) && value > 0, `invalid local bound: ${name}`);
}
requireValue(
  productionPolicy.node_profiles === undefined &&
    productionPolicy.local_unshare === undefined,
  "research Node policy leaked into Cloudflare production policy"
);
requireValue(
  !/node-policy|edge-node-policy|LOCAL_UNSHARE/.test(productionPolicyModule),
  "Cloudflare production policy module imports Node profile policy"
);

console.log(JSON.stringify({ ok: true, schema_version: policy.schema_version }));
