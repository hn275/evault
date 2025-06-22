use std::{net::SocketAddr, sync::Arc};

use anyhow::Context;
use app::AppState;
use axum::{
    Router,
    http::{Method, header},
    routing::get,
};
use cache::Redis;
use database::Database;
use dotenv::dotenv;
use github::GitHubAPI;
use tower_http::{
    cors::{Any, CorsLayer},
    trace::TraceLayer,
};
use tracing::info;
use tracing_subscriber::{EnvFilter, layer::SubscriberExt, util::SubscriberInitExt};

mod app;
mod cache;
mod database;
mod errors;
mod github;
mod handlers;
mod secrets;
mod utils;

use utils::{Stage, env};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let _ = dotenv();
    // configure logging
    let stage = Stage::read_from_env()?;
    let log_cfg = match stage {
        Stage::Production => [
            "main=info",             // code in this file
            "server=info",           // code in this crate (but not this file)
            "tower_http=info",       // http request/response pairs
            "axum::rejection=trace", // extractor rejections (i.e. bad form input)
        ],
        Stage::Development => [
            "main=debug",            // code in this file
            "server=debug",          // code in this crate (but not this file)
            "tower_http=debug",      // http request/response pairs
            "axum::rejection=trace", // extractor rejections (i.e. bad form input)
        ],
    };

    tracing_subscriber::registry()
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| log_cfg.join(",").into()))
        .with(tracing_subscriber::fmt::layer())
        .init();

    // build app state
    let app = Arc::new(AppState {
        github: GitHubAPI::new(),
        redis: Redis::new()?,
        database: Database::new().await?,
    });

    // build router
    // nested router, path prefix `/api/github`
    let github_router = Router::new()
        .route("/auth", get(handlers::auth::auth))
        .route("/auth/token", get(handlers::auth::auth_token))
        .with_state(app);

    // main router
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods([Method::GET, Method::POST])
        .allow_headers([header::CONTENT_TYPE, header::AUTHORIZATION]);

    let router = Router::new()
        .nest("/api/github", github_router)
        .layer(cors)
        .layer(TraceLayer::new_for_http());

    // bind listener to router
    let addr: SocketAddr = env::env_or_default("EVAULT_ADDR", "0.0.0.0:8000")
        .parse()
        .context("invalid binding socket address.")?;
    let listener = tokio::net::TcpListener::bind(addr).await?;

    info!("Listening on {}", addr);
    axum::serve(listener, router)
        .await
        .context("failed to start server listener.")
}
