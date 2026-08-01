const shims = new Map([
  ["cloudflare:workers", new URL("./cloudflare-workers-shim.mjs", import.meta.url).href],
  ["cloudflare:workflows", new URL("./cloudflare-workflows-shim.mjs", import.meta.url).href]
]);

export async function resolve(specifier, context, nextResolve) {
  const url = shims.get(specifier);
  return url === undefined
    ? nextResolve(specifier, context)
    : {url, shortCircuit: true};
}
