#!/usr/bin/env node

import { createInterface } from "node:readline";
import { resolve } from "node:path";

import { ResearchNodeControlSession } from "../src/research-node-control.js";

function parseRoot(arguments_: readonly string[]): string {
  const index = arguments_.indexOf("--root");
  if (index < 0 || index + 1 >= arguments_.length) {
    throw new Error("usage: ordivon_edge_node_control.ts --root <provider-root>");
  }
  const root = arguments_[index + 1];
  if (root === undefined || root.length === 0) {
    throw new Error("provider root is empty");
  }
  return resolve(root);
}

async function main(): Promise<void> {
  const root = parseRoot(process.argv.slice(2));
  const session = new ResearchNodeControlSession({ root });
  const lines = createInterface({ input: process.stdin, crlfDelay: Number.POSITIVE_INFINITY });
  for await (const line of lines) {
    if (line.length === 0) continue;
    let request: unknown;
    try {
      request = JSON.parse(line);
    } catch {
      process.stdout.write(`${JSON.stringify({
        schema_version: 1,
        request_id: "invalid-json",
        ok: false,
        error: { code: "invalid_request", message: "request is not valid JSON" }
      })}\n`);
      continue;
    }
    const response = await session.handle(request);
    process.stdout.write(`${JSON.stringify(response)}\n`);
  }
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`${message.slice(0, 2048)}\n`);
  process.exitCode = 1;
});
