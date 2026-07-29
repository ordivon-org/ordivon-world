import { readdir, readFile, stat } from "node:fs/promises";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const forbiddenPaths = [
  "Cargo.toml",
  "rust-toolchain.toml",
  "crates",
  "config/targets"
];
const forbiddenSourcePatterns = [
  /Surfshark/i,
  /WireGuard/i,
  /VLESS/i,
  /Hysteria/i,
  /route selection/i,
  /host route/i,
  /QUIC relay/i,
  /link-probe/i
];

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

for (const path of forbiddenPaths) {
  if (await exists(join(root, path))) {
    throw new Error(`Link/network path leaked into Edge: ${path}`);
  }
}

async function walk(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await walk(path)));
    else files.push(path);
  }
  return files;
}

for (const path of await walk(join(root, "src"))) {
  const text = await readFile(path, "utf8");
  for (const pattern of forbiddenSourcePatterns) {
    if (pattern.test(text)) {
      throw new Error(`${relative(root, path)} violates Edge boundary: ${pattern}`);
    }
  }
}

console.log("Edge boundary check passed");
