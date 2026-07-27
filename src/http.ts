const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store",
  "x-content-type-options": "nosniff",
  "referrer-policy": "no-referrer",
  "cross-origin-resource-policy": "same-origin",
  "content-security-policy": "default-src 'none'; frame-ancestors 'none'"
} as const;

export function jsonResponse(value: unknown, status = 200): Response {
  return new Response(JSON.stringify(value), {
    status,
    headers: JSON_HEADERS
  });
}

export function methodNotAllowed(allow: string): Response {
  const response = jsonResponse({ error: "method_not_allowed", allow }, 405);
  response.headers.set("allow", allow);
  return response;
}
