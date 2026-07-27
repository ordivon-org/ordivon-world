import { CAPABILITIES, EDGE_SCHEMA_VERSION } from "./contracts.js";
import { jsonResponse, methodNotAllowed } from "./http.js";

export interface Env {
  readonly ARTIFACTS: R2Bucket;
}

export async function handleRequest(request: Request): Promise<Response> {
  const url = new URL(request.url);

  if (url.pathname === "/health") {
    if (request.method !== "GET") {
      return methodNotAllowed("GET");
    }
    return jsonResponse({
      schema_version: EDGE_SCHEMA_VERSION,
      service: "ordivon-edge",
      status: "ok"
    });
  }

  if (url.pathname === "/v1/capabilities") {
    if (request.method !== "GET") {
      return methodNotAllowed("GET");
    }
    return jsonResponse(CAPABILITIES);
  }

  return jsonResponse({ error: "not_found" }, 404);
}

export default {
  fetch(request: Request, _env: Env, _ctx: ExecutionContext): Promise<Response> {
    return handleRequest(request);
  }
} satisfies ExportedHandler<Env>;
