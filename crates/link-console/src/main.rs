use std::convert::Infallible;
use std::net::SocketAddr;
use std::path::PathBuf;
use std::sync::Arc;
use std::time::Duration;

use anyhow::{Context, Result, bail};
use async_stream::stream;
use axum::extract::{Query, State};
use axum::http::{HeaderValue, Request, StatusCode, header};
use axum::middleware::{self, Next};
use axum::response::sse::{Event, KeepAlive, Sse};
use axum::response::{Html, IntoResponse, Response};
use axum::routing::get;
use axum::{Json, Router};
use chrono::{DateTime, Utc};
use clap::Parser;
use link_observer::{LinkEvent, LinkSnapshot, LinkStateEngine, SystemObserver};
use serde::Serialize;
use serde_json::json;
use tokio::net::TcpListener;
use tower::{ServiceBuilder, make::Shared, util::BoxCloneService};
use tracing::{info, warn};
use tracing_subscriber::EnvFilter;

const INDEX_HTML: &str = include_str!("../assets/index.html");
const APP_JS: &str = include_str!("../assets/app.js");
const STYLES_CSS: &str = include_str!("../assets/styles.css");
const SSE_SNAPSHOT_INTERVAL: Duration = Duration::from_secs(15);

#[derive(Debug, Parser)]
#[command(
    name = "ordivon-link",
    version,
    about = "Private local Web control plane for Ordivon Edge"
)]
struct Cli {
    #[arg(long, default_value = "127.0.0.1:8787")]
    bind: SocketAddr,
    #[arg(long, default_value = "artifacts/runtime/edge.db")]
    database: PathBuf,
    #[arg(long, default_value = "config/targets/web.toml")]
    targets: PathBuf,
    #[arg(long, default_value_t = 30)]
    interval_seconds: u64,
    #[arg(long, env = "ORDIVON_LINK_CURL_BIN", default_value = "curl")]
    curl_bin: String,
}

#[derive(Clone)]
struct AppState {
    runtime: Arc<LinkStateEngine>,
    stale_after: Duration,
}

#[derive(Debug, Clone, Serialize)]
struct FreshnessStatus {
    served_at: DateTime<Utc>,
    snapshot_age_seconds: u64,
    stale: bool,
}

#[derive(Debug, Clone, Serialize)]
struct StatusResponse {
    snapshot: LinkSnapshot,
    freshness: FreshnessStatus,
}

#[derive(Debug, serde::Deserialize)]
struct EventQuery {
    limit: Option<usize>,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("ordivon_edge=info,link_observer=info")),
        )
        .without_time()
        .init();

    let cli = Cli::parse();
    validate_bind(cli.bind)?;
    if cli.interval_seconds == 0 {
        bail!("--interval-seconds must be at least 1");
    }

    let observer = SystemObserver::new(&cli.targets).with_curl_bin(cli.curl_bin);
    let runtime = LinkStateEngine::open(observer, &cli.database)?;
    if let Err(error) = runtime.refresh().await {
        if runtime.latest().await.is_none() {
            return Err(error).context("initial Edge observation failed");
        }
        warn!("live observation failed; serving the last sanitized snapshot");
    }
    let interval = Duration::from_secs(cli.interval_seconds);
    let stale_after = Duration::from_secs(cli.interval_seconds.saturating_mul(3).max(60));
    tokio::spawn(runtime.clone().run(interval));

    let app = app(runtime, stale_after);
    let listener = TcpListener::bind(cli.bind)
        .await
        .with_context(|| format!("failed to bind {}", cli.bind))?;
    info!(bind = %cli.bind, "Ordivon Edge Web plane listening");
    axum::serve(listener, Shared::new(app))
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    Ok(())
}

fn routes(runtime: Arc<LinkStateEngine>, stale_after: Duration) -> Router {
    Router::new()
        .route("/", get(index))
        .route("/assets/app.js", get(app_js))
        .route("/assets/styles.css", get(styles_css))
        .route("/api/v1/health", get(health))
        .route("/api/v1/status", get(status))
        .route("/api/v1/events", get(events))
        .route("/events", get(event_stream))
        .with_state(AppState {
            runtime,
            stale_after,
        })
}

fn app(
    runtime: Arc<LinkStateEngine>,
    stale_after: Duration,
) -> BoxCloneService<Request<axum::body::Body>, Response, Infallible> {
    BoxCloneService::new(
        ServiceBuilder::new()
            .layer(middleware::from_fn(security_headers))
            .layer(middleware::from_fn(require_local_request))
            .service(routes(runtime, stale_after)),
    )
}

async fn index() -> Html<&'static str> {
    Html(INDEX_HTML)
}

async fn app_js() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "text/javascript; charset=utf-8")],
        APP_JS,
    )
}

async fn styles_css() -> impl IntoResponse {
    (
        [(header::CONTENT_TYPE, "text/css; charset=utf-8")],
        STYLES_CSS,
    )
}

async fn health(State(state): State<AppState>) -> (StatusCode, Json<serde_json::Value>) {
    let Some(snapshot) = state.runtime.latest().await else {
        return (
            StatusCode::SERVICE_UNAVAILABLE,
            Json(json!({
                "status": "starting",
                "ready": false,
                "privacy": "redacted"
            })),
        );
    };
    let freshness = freshness(&snapshot, state.stale_after);
    let code = if freshness.stale {
        StatusCode::SERVICE_UNAVAILABLE
    } else {
        StatusCode::OK
    };
    (
        code,
        Json(json!({
            "status": if freshness.stale { "stale" } else { "ok" },
            "ready": !freshness.stale,
            "snapshot_age_seconds": freshness.snapshot_age_seconds,
            "privacy": "redacted"
        })),
    )
}

async fn status(State(state): State<AppState>) -> Result<Json<StatusResponse>, StatusCode> {
    state
        .runtime
        .latest()
        .await
        .map(|snapshot| Json(status_response(snapshot, state.stale_after)))
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)
}

async fn events(
    State(state): State<AppState>,
    Query(query): Query<EventQuery>,
) -> Result<Json<Vec<LinkEvent>>, StatusCode> {
    state
        .runtime
        .recent_events(query.limit.unwrap_or(50))
        .map(Json)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)
}

async fn event_stream(
    State(state): State<AppState>,
) -> Sse<impl futures_core::Stream<Item = Result<Event, Infallible>>> {
    let mut latest = state.runtime.latest().await;
    let mut updates = state.runtime.subscribe();
    let mut heartbeat = tokio::time::interval(SSE_SNAPSHOT_INTERVAL);
    heartbeat.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);
    let output = stream! {
        if let Some(snapshot) = latest.clone()
            && let Ok(event) = Event::default()
                .event("snapshot")
                .json_data(status_response(snapshot, state.stale_after))
        {
            yield Ok(event);
        }
        heartbeat.tick().await;
        loop {
            tokio::select! {
                update = updates.recv() => {
                    match update {
                        Ok(snapshot) => {
                            latest = Some(snapshot.clone());
                            if let Ok(event) = Event::default()
                                .event("snapshot")
                                .json_data(status_response(snapshot, state.stale_after))
                            {
                                yield Ok(event);
                            }
                        }
                        Err(tokio::sync::broadcast::error::RecvError::Lagged(_)) => {
                            latest = state.runtime.latest().await;
                        }
                        Err(tokio::sync::broadcast::error::RecvError::Closed) => break,
                    }
                }
                _ = heartbeat.tick() => {
                    if let Some(snapshot) = latest.clone()
                        && let Ok(event) = Event::default()
                            .event("snapshot")
                            .json_data(status_response(snapshot, state.stale_after))
                    {
                        yield Ok(event);
                    }
                }
            }
        }
    };
    Sse::new(output).keep_alive(
        KeepAlive::new()
            .interval(Duration::from_secs(15))
            .text("edge-keepalive"),
    )
}

async fn require_local_request(request: Request<axum::body::Body>, next: Next) -> Response {
    let allowed_host = request
        .headers()
        .get(header::HOST)
        .and_then(|value| value.to_str().ok())
        .is_some_and(is_allowed_host);
    if !allowed_host {
        return StatusCode::MISDIRECTED_REQUEST.into_response();
    }
    if !is_unambiguous_request_target(request.uri()) {
        return StatusCode::BAD_REQUEST.into_response();
    }
    next.run(request).await
}

fn is_unambiguous_request_target(uri: &axum::http::Uri) -> bool {
    if uri.scheme().is_some() || uri.authority().is_some() {
        return false;
    }
    let path = uri.path();
    if !path.is_ascii()
        || path.bytes().any(|byte| {
            !(byte.is_ascii_alphanumeric() || matches!(byte, b'/' | b'.' | b'-' | b'_'))
        })
    {
        return false;
    }
    !path.split('/').any(|segment| matches!(segment, "." | ".."))
}

fn is_allowed_host(raw: &str) -> bool {
    let host = raw.trim().to_ascii_lowercase();
    ["localhost", "127.0.0.1", "[::1]"].iter().any(|allowed| {
        host == *allowed
            || host
                .strip_prefix(allowed)
                .and_then(|suffix| suffix.strip_prefix(':'))
                .is_some_and(|port| !port.is_empty() && port.chars().all(|c| c.is_ascii_digit()))
    })
}

fn freshness(snapshot: &LinkSnapshot, stale_after: Duration) -> FreshnessStatus {
    let served_at = Utc::now();
    let snapshot_age_seconds = served_at
        .signed_duration_since(snapshot.observed_at)
        .to_std()
        .unwrap_or(Duration::ZERO)
        .as_secs();
    FreshnessStatus {
        served_at,
        snapshot_age_seconds,
        stale: snapshot_age_seconds > stale_after.as_secs(),
    }
}

fn status_response(snapshot: LinkSnapshot, stale_after: Duration) -> StatusResponse {
    let freshness = freshness(&snapshot, stale_after);
    StatusResponse {
        snapshot,
        freshness,
    }
}

async fn security_headers(request: Request<axum::body::Body>, next: Next) -> Response {
    let mut response = next.run(request).await;
    let headers = response.headers_mut();
    headers.insert(
        header::CONTENT_SECURITY_POLICY,
        HeaderValue::from_static(
            "default-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
        ),
    );
    headers.insert(
        header::X_CONTENT_TYPE_OPTIONS,
        HeaderValue::from_static("nosniff"),
    );
    headers.insert(header::X_FRAME_OPTIONS, HeaderValue::from_static("DENY"));
    headers.insert(
        header::REFERRER_POLICY,
        HeaderValue::from_static("no-referrer"),
    );
    headers.insert(header::CACHE_CONTROL, HeaderValue::from_static("no-store"));
    headers.insert(
        axum::http::HeaderName::from_static("cross-origin-opener-policy"),
        HeaderValue::from_static("same-origin"),
    );
    headers.insert(
        axum::http::HeaderName::from_static("cross-origin-resource-policy"),
        HeaderValue::from_static("same-origin"),
    );
    headers.insert(
        axum::http::HeaderName::from_static("permissions-policy"),
        HeaderValue::from_static("camera=(), microphone=(), geolocation=(), payment=()"),
    );
    response
}

fn validate_bind(bind: SocketAddr) -> Result<()> {
    if !bind.ip().is_loopback() {
        bail!("Ordivon Edge Web must bind to a loopback address");
    }
    Ok(())
}

async fn shutdown_signal() {
    let _ = tokio::signal::ctrl_c().await;
}

#[cfg(test)]
mod tests {
    use axum::body::{Body, to_bytes};
    use tower::ServiceExt;

    use chrono::Duration as ChronoDuration;
    use link_observer::{
        DnsSnapshot, HealthState, Ipv6Risk, LocalRuntimeSnapshot, PathState, PrivacyStatus,
        ProviderSnapshot, RouteSnapshot, ServiceState,
    };

    use super::*;

    fn sample_snapshot(observed_at: DateTime<Utc>) -> LinkSnapshot {
        LinkSnapshot {
            schema_version: 1,
            observed_at,
            health: HealthState::Healthy,
            path_state: PathState::Tunneled,
            provider: ProviderSnapshot {
                name: "surfshark".into(),
                detected: true,
                connected: true,
                protocol: Some("wireguard".into()),
            },
            route: RouteSnapshot {
                effective_interface_class: "tunnel".into(),
                ipv4_tunnel_route: true,
                mtu: Some(1380),
                ipv6_default_route: false,
                ipv6_tunnel_route: false,
                ipv6_risk: Ipv6Risk::NoneObserved,
            },
            dns: DnsSnapshot {
                mode: "wsl_dns_tunneling".into(),
                resolver_count: 1,
            },
            local_runtime: LocalRuntimeSnapshot {
                cloudflare_tunnel_running: Some(true),
                ordivon_mcp_running: Some(true),
            },
            services: vec![link_observer::ServiceCheck {
                id: "github-web".into(),
                state: ServiceState::Healthy,
                latency_ms: Some(200.0),
                failure_class: None,
            }],
            reasons: Vec::new(),
            privacy: PrivacyStatus {
                sensitive_fields_redacted: true,
                network_binding: "loopback_only".into(),
                raw_command_output_retained: false,
            },
        }
    }

    #[test]
    fn stale_snapshots_are_explicitly_marked() {
        let snapshot = sample_snapshot(Utc::now() - ChronoDuration::seconds(121));
        let response = status_response(snapshot, Duration::from_secs(60));
        assert!(response.freshness.stale);
        assert!(response.freshness.snapshot_age_seconds >= 120);
    }

    #[test]
    fn future_clock_skew_does_not_underflow_snapshot_age() {
        let snapshot = sample_snapshot(Utc::now() + ChronoDuration::seconds(30));
        let response = status_response(snapshot, Duration::from_secs(60));
        assert_eq!(response.freshness.snapshot_age_seconds, 0);
        assert!(!response.freshness.stale);
    }

    #[test]
    fn loopback_is_allowed_by_default() {
        let address: SocketAddr = "127.0.0.1:8787".parse().expect("address");
        assert!(validate_bind(address).is_ok());
    }

    #[test]
    fn non_loopback_is_rejected() {
        let address: SocketAddr = "0.0.0.0:8787".parse().expect("address");
        assert!(validate_bind(address).is_err());
    }

    #[tokio::test]
    async fn local_ui_has_security_headers_and_no_external_assets() {
        let directory = tempfile::tempdir().expect("tempdir");
        let runtime = LinkStateEngine::open(
            SystemObserver::new(directory.path().join("missing-targets.toml")),
            &directory.path().join("edge.db"),
        )
        .expect("runtime");
        let response = app(runtime, Duration::from_secs(60))
            .oneshot(
                Request::builder()
                    .uri("/")
                    .header(header::HOST, "localhost:8787")
                    .body(Body::empty())
                    .expect("request"),
            )
            .await
            .expect("response");

        assert_eq!(response.status(), StatusCode::OK);
        assert_eq!(
            response.headers().get(header::X_FRAME_OPTIONS),
            Some(&HeaderValue::from_static("DENY"))
        );
        assert!(
            response
                .headers()
                .contains_key(header::CONTENT_SECURITY_POLICY)
        );
        let body = to_bytes(response.into_body(), 128 * 1024)
            .await
            .expect("body");
        let body = String::from_utf8(body.to_vec()).expect("utf8");
        assert!(body.contains("Ordivon Edge"));
        assert!(!body.contains("https://"));
        assert!(!body.contains("http://"));
    }

    #[test]
    fn request_target_rejects_encoded_or_absolute_paths() {
        for target in ["/", "/api/v1/status", "/assets/styles.css"] {
            let uri: axum::http::Uri = target.parse().expect("uri");
            assert!(
                is_unambiguous_request_target(&uri),
                "expected safe {target}"
            );
        }
        for target in [
            "/assets/%2e%2e/api/v1/status",
            "/api/../api/v1/status",
            r"/api\v1\status",
            "http://attacker.example/api/v1/status",
        ] {
            let uri: axum::http::Uri = target.parse().expect("uri");
            assert!(
                !is_unambiguous_request_target(&uri),
                "unexpected safe target {target}"
            );
        }
    }

    #[tokio::test]
    async fn encoded_traversal_is_rejected_before_routing() {
        let directory = tempfile::tempdir().expect("tempdir");
        let runtime = LinkStateEngine::open(
            SystemObserver::new(directory.path().join("missing-targets.toml")),
            &directory.path().join("edge.db"),
        )
        .expect("runtime");
        let response = app(runtime, Duration::from_secs(60))
            .oneshot(
                Request::builder()
                    .uri("/assets/%2e%2e/api/v1/status")
                    .header(header::HOST, "localhost:8787")
                    .body(Body::empty())
                    .expect("request"),
            )
            .await
            .expect("response");
        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
        assert!(
            response
                .headers()
                .contains_key(header::CONTENT_SECURITY_POLICY)
        );
    }

    #[test]
    fn host_allowlist_rejects_dns_rebinding_names() {
        for host in [
            "localhost",
            "localhost:8787",
            "127.0.0.1:8787",
            "[::1]:8787",
        ] {
            assert!(is_allowed_host(host), "expected allowed host {host}");
        }
        for host in [
            "attacker.example",
            "127.0.0.1.attacker.example",
            "localhost.attacker.example",
            "localhost:bad",
            "",
        ] {
            assert!(!is_allowed_host(host), "unexpected allowed host {host}");
        }
    }

    #[tokio::test]
    async fn untrusted_host_is_rejected_with_security_headers() {
        let directory = tempfile::tempdir().expect("tempdir");
        let runtime = LinkStateEngine::open(
            SystemObserver::new(directory.path().join("missing-targets.toml")),
            &directory.path().join("edge.db"),
        )
        .expect("runtime");
        let response = app(runtime, Duration::from_secs(60))
            .oneshot(
                Request::builder()
                    .uri("/api/v1/status")
                    .header(header::HOST, "attacker.example")
                    .body(Body::empty())
                    .expect("request"),
            )
            .await
            .expect("response");
        assert_eq!(response.status(), StatusCode::MISDIRECTED_REQUEST);
        assert!(
            response
                .headers()
                .contains_key(header::CONTENT_SECURITY_POLICY)
        );
    }

    #[test]
    fn embedded_assets_do_not_call_external_origins() {
        for asset in [INDEX_HTML, APP_JS, STYLES_CSS] {
            assert!(!asset.contains("https://"));
            assert!(!asset.contains("http://"));
        }
    }
}
