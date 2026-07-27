export const EDGE_POLICY_VERSION = "2026-07-27.p1.5" as const;

export const CAPABILITY_VERSIONS = {
  fetch: "fetch.v2",
  "browser.run": "browser.snapshot.v2",
  "artifact.put": "artifact.put.v1",
  "artifact.get": "artifact.get.v1",
  "artifact.delete": "artifact.delete.planned"
} as const;
