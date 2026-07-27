const $ = (id) => document.getElementById(id);

const labels = {
  wsl_dns_tunneling: "WSL DNS tunneling",
  local_resolver: "Local resolver",
  custom_resolver: "Custom resolver",
  latent_physical_default: "Latent risk",
  none_observed: "No route observed",
  tunnel_covered: "Tunnel covered",
  tunneled: "Tunneled",
  direct: "Direct",
  degraded: "Degraded",
  failed: "Failed",
  unknown: "Unknown",
};

function pretty(value) {
  return labels[value] || String(value || "unknown")
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function boolState(value) {
  if (value === true) return "Running";
  if (value === false) return "Stopped";
  return "Unknown";
}

function renderSnapshot(payload) {
  const snapshot = payload.snapshot || payload;
  const freshness = payload.freshness || null;
  const health = freshness?.stale ? "degraded" : (snapshot.health || "unknown");
  const badge = $("health-badge");
  badge.textContent = freshness?.stale ? "Stale" : pretty(health);
  badge.className = `badge ${health}`;

  $("path-title").textContent = `${pretty(snapshot.path_state)} · ${pretty(snapshot.provider.protocol || "provider observed")}`;
  $("path-summary").textContent = freshness?.stale
    ? `This is the last known sanitized state and is ${freshness.snapshot_age_seconds} seconds old.`
    : snapshot.provider.connected
      ? "The host VPN and WSL IPv4 tunnel route are observed independently. Sensitive network identity remains redacted."
      : "The Edge observer cannot verify an active Surfshark tunnel. No automatic network mutation is performed.";
  $("observed-at").textContent = new Date(snapshot.observed_at).toLocaleString();

  $("provider").textContent = pretty(snapshot.provider.name);
  $("provider-detail").textContent = snapshot.provider.connected
    ? `${pretty(snapshot.provider.protocol)} · connected`
    : snapshot.provider.detected ? "Detected · disconnected" : "Not detected";

  $("route").textContent = pretty(snapshot.route.effective_interface_class);
  $("route-detail").textContent = `${snapshot.route.ipv4_tunnel_route ? "IPv4 tunnel verified" : "IPv4 tunnel unverified"}${snapshot.route.mtu ? ` · MTU ${snapshot.route.mtu}` : ""}`;

  $("dns").textContent = pretty(snapshot.dns.mode);
  $("dns-detail").textContent = `${snapshot.dns.resolver_count} resolver${snapshot.dns.resolver_count === 1 ? "" : "s"} observed`;

  $("ipv6").textContent = pretty(snapshot.route.ipv6_risk);
  $("ipv6-detail").textContent = snapshot.route.ipv6_default_route
    ? snapshot.route.ipv6_tunnel_route ? "Default route covered" : "Physical default exists"
    : "No default route observed";

  $("cloudflared").textContent = boolState(snapshot.local_runtime.cloudflare_tunnel_running);
  $("mcp").textContent = boolState(snapshot.local_runtime.ordivon_mcp_running);
  $("privacy").textContent = snapshot.privacy.network_binding === "loopback_only" ? "Loopback only" : "Review required";

  renderServices(snapshot.services || []);
  renderReasons(snapshot.reasons || []);
}

function renderServices(services) {
  const root = $("services");
  root.replaceChildren();
  $("service-count").textContent = `${services.length} targets`;
  if (!services.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No service checks are available.";
    root.append(empty);
    return;
  }
  for (const service of services) {
    const item = document.createElement("div");
    item.className = "service";

    const name = document.createElement("span");
    name.className = "service-name";
    name.textContent = pretty(service.id);

    const meta = document.createElement("span");
    meta.className = "service-meta";
    const state = document.createElement("span");
    state.className = `service-state ${service.state}`;
    state.textContent = pretty(service.state);
    const latency = document.createElement("span");
    latency.className = "latency";
    latency.textContent = Number.isFinite(service.latency_ms)
      ? `${Math.round(service.latency_ms)} ms`
      : service.failure_class ? pretty(service.failure_class) : "—";
    meta.append(state, latency);
    item.append(name, meta);
    root.append(item);
  }
}

function renderReasons(reasons) {
  const root = $("reasons");
  root.replaceChildren();
  for (const reason of reasons) {
    const item = document.createElement("div");
    item.className = "reason";
    item.textContent = pretty(reason);
    root.append(item);
  }
}

function renderEvents(events) {
  const root = $("timeline");
  root.replaceChildren();
  if (!events.length) {
    const item = document.createElement("li");
    item.className = "empty";
    item.textContent = "No state transitions recorded yet.";
    root.append(item);
    return;
  }
  for (const event of events) {
    const item = document.createElement("li");
    const time = document.createElement("time");
    time.dateTime = event.observed_at;
    time.textContent = new Date(event.observed_at).toLocaleString();
    const summary = document.createElement("p");
    summary.textContent = event.summary;
    item.append(time, summary);
    root.append(item);
  }
}

async function loadStatus() {
  const response = await fetch("/api/v1/status", { cache: "no-store" });
  if (!response.ok) throw new Error(`status ${response.status}`);
  renderSnapshot(await response.json());
}

async function loadEvents() {
  const response = await fetch("/api/v1/events?limit=30", { cache: "no-store" });
  if (!response.ok) throw new Error(`events ${response.status}`);
  renderEvents(await response.json());
}

function connectStream() {
  const stream = new EventSource("/events");
  stream.addEventListener("open", () => {
    $("stream-dot").classList.add("live");
    $("stream-label").textContent = "Live";
  });
  stream.addEventListener("snapshot", (event) => {
    renderSnapshot(JSON.parse(event.data));
    loadEvents().catch(() => {});
  });
  stream.addEventListener("error", () => {
    $("stream-dot").classList.remove("live");
    $("stream-label").textContent = "Reconnecting";
  });
}

$("refresh").addEventListener("click", async () => {
  const button = $("refresh");
  button.disabled = true;
  button.textContent = "Refreshing…";
  try {
    await Promise.all([loadStatus(), loadEvents()]);
  } finally {
    button.disabled = false;
    button.textContent = "Refresh view";
  }
});

Promise.all([loadStatus(), loadEvents()])
  .catch(() => { $("path-summary").textContent = "The local Edge API is not available."; });
connectStream();
