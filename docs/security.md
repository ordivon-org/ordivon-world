# Security boundary

Current public behavior is intentionally minimal:

- `GET /health`;
- `GET /v1/capabilities`;
- all other paths return 404;
- mutation methods on known routes return 405;
- responses are non-cacheable and deny framing, referrers, MIME sniffing, and cross-origin resource embedding;
- Workers.dev and preview URLs are disabled;
- R2 public access remains disabled.

Before adding execution endpoints, the project requires:

1. service-to-service authentication;
2. explicit authorization per capability;
3. request and output size limits;
4. redirect, scheme, port, hostname, and private-address policy for fetch;
5. Browser Run time and action budgets;
6. receipt persistence and replay/idempotency semantics;
7. audit-safe logging with no secrets or response bodies by default.
