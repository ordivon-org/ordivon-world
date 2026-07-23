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
use clap::Parser;
use edge_runtime::{EdgeEvent, EdgeRuntime, EdgeSnapshot, SystemObserver};
use serde_json::json;
use tokio::net::TcpListener;
use tracing::{info, warn};
use tracing_subscriber::EnvFilter;

const INDEX_HTML: &str = include_str!("../assets/index.html");
const APP_JS: &str = include_str!("../assets/app.js");
const STYLES_CSS: &str = include_str!("../assets/styles.css");

#[derive(Debug, Parser)]
#[command(
    name = "ordivon-edge",
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
    #[arg(long, env = "ORDIVON_EDGE_CURL_BIN", default_value = "curl")]
    curl_bin: String,
}

#[derive(Clone)]
struct AppState {
    runtime: Arc<EdgeRuntime>,
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
                .unwrap_or_else(|_| EnvFilter::new("ordivon_edge=info,edge_runtime=info")),
        )
        .without_time()
        .init();

    let cli = Cli::parse();
    validate_bind(cli.bind)?;
    if cli.interval_seconds == 0 {
        bail!("--interval-seconds must be at least 1");
    }

    let observer = SystemObserver::new(&cli.targets).with_curl_bin(cli.curl_bin);
    let runtime = EdgeRuntime::open(observer, &cli.database)?;
    if let Err(error) = runtime.refresh().await {
        if runtime.latest().await.is_none() {
            return Err(error).context("initial Edge observation failed");
        }
        warn!("live observation failed; serving the last sanitized snapshot");
    }
    tokio::spawn(
        runtime
            .clone()
            .run(Duration::from_secs(cli.interval_seconds)),
    );

    let app = router(runtime);
    let listener = TcpListener::bind(cli.bind)
        .await
        .with_context(|| format!("failed to bind {}", cli.bind))?;
    info!(bind = %cli.bind, "Ordivon Edge Web plane listening");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    Ok(())
}

fn router(runtime: Arc<EdgeRuntime>) -> Router {
    Router::new()
        .route("/", get(index))
        .route("/assets/app.js", get(app_js))
        .route("/assets/styles.css", get(styles_css))
        .route("/api/v1/health", get(health))
        .route("/api/v1/status", get(status))
        .route("/api/v1/events", get(events))
        .route("/events", get(event_stream))
        .with_state(AppState { runtime })
        .layer(middleware::from_fn(security_headers))
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

async fn health() -> Json<serde_json::Value> {
    Json(json!({"status": "ok", "privacy": "redacted"}))
}

async fn status(State(state): State<AppState>) -> Result<Json<EdgeSnapshot>, StatusCode> {
    state
        .runtime
        .latest()
        .await
        .map(Json)
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)
}

async fn events(
    State(state): State<AppState>,
    Query(query): Query<EventQuery>,
) -> Result<Json<Vec<EdgeEvent>>, StatusCode> {
    state
        .runtime
        .recent_events(query.limit.unwrap_or(50))
        .map(Json)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)
}

async fn event_stream(
    State(state): State<AppState>,
) -> Sse<impl futures_core::Stream<Item = Result<Event, Infallible>>> {
    let initial = state.runtime.latest().await;
    let mut updates = state.runtime.subscribe();
    let output = stream! {
        if let Some(snapshot) = initial
            && let Ok(event) = Event::default().event("snapshot").json_data(snapshot)
        {
            yield Ok(event);
        }
        loop {
            match updates.recv().await {
                Ok(snapshot) => {
                    if let Ok(event) = Event::default().event("snapshot").json_data(snapshot) {
                        yield Ok(event);
                    }
                }
                Err(tokio::sync::broadcast::error::RecvError::Lagged(_)) => continue,
                Err(tokio::sync::broadcast::error::RecvError::Closed) => break,
            }
        }
    };
    Sse::new(output).keep_alive(
        KeepAlive::new()
            .interval(Duration::from_secs(15))
            .text("edge-keepalive"),
    )
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

    use super::*;

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
        let runtime = EdgeRuntime::open(
            SystemObserver::new(directory.path().join("missing-targets.toml")),
            &directory.path().join("edge.db"),
        )
        .expect("runtime");
        let response = router(runtime)
            .oneshot(
                Request::builder()
                    .uri("/")
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
    fn embedded_assets_do_not_call_external_origins() {
        for asset in [INDEX_HTML, APP_JS, STYLES_CSS] {
            assert!(!asset.contains("https://"));
            assert!(!asset.contains("http://"));
        }
    }
}
