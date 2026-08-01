import assert from "node:assert/strict";
import test from "node:test";

import { validateEvidenceRunRequest } from "../src/evidence-run-contracts.js";
import { TEST_ENV_BASE } from "./helpers.js";

test("valid evidence run keeps source-native fetch and browser inputs", () => {
  const value = validateEvidenceRunRequest({
    schema_version: 1,
    consumer: "ordivon-computer",
    workload: "research-source-capture",
    steps: [
      {id: "source", operation: "fetch", input: {url: "https://allowed.example.org/data", maximum_bytes: 1024}},
      {id: "page", operation: "browser.run", input: {url: "https://allowed.example.org/page", full_page: true}}
    ]
  }, TEST_ENV_BASE);
  assert.equal(value.steps.length, 2);
  assert.equal(value.steps[0]?.operation, "fetch");
  assert.equal(value.steps[1]?.operation, "browser.run");
});

test("evidence run rejects unknown fields and unsupported operations", () => {
  assert.throws(() => validateEvidenceRunRequest({
    schema_version: 1,
    consumer: "ordivon-computer",
    workload: "capture",
    unexpected: true,
    steps: [{id: "source", operation: "fetch", input: {url: "https://allowed.example.org"}}]
  }, TEST_ENV_BASE), /unsupported fields/);
  assert.throws(() => validateEvidenceRunRequest({
    schema_version: 1,
    consumer: "ordivon-computer",
    workload: "capture",
    steps: [{id: "write", operation: "artifact.delete", input: {url: "https://allowed.example.org"}}]
  }, TEST_ENV_BASE), /unsupported/);
});

test("evidence run requires unique bounded step IDs", () => {
  assert.throws(() => validateEvidenceRunRequest({
    schema_version: 1,
    consumer: "ordivon-computer",
    workload: "capture",
    steps: [
      {id: "same", operation: "fetch", input: {url: "https://allowed.example.org/a"}},
      {id: "same", operation: "fetch", input: {url: "https://allowed.example.org/b"}}
    ]
  }, TEST_ENV_BASE), /unique/);
});
