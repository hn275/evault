use std::sync::Arc;

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Redirect},
};
use serde::Deserialize;

use crate::{
    app::AppState,
    cache::RedisAuthSession,
    errors::{AppError, Result},
    github::GITHUB_OAUTH_STATE_TTL,
    secrets,
};

// /api/github/auth
#[derive(Deserialize)]
pub struct AuthQuery {
    pub device_type: String,
}

#[axum::debug_handler]
pub async fn auth(
    State(app): State<Arc<AppState>>,
    Query(q): Query<AuthQuery>,
) -> Result<impl IntoResponse> {
    let oauth_state = secrets::token_urlsafe(32)?;
    let session_id = secrets::token_urlsafe(16)?;
    let oauth_login_url = app
        .github
        .make_login_url(&session_id, &oauth_state, &q.device_type)?;

    let auth_session = RedisAuthSession {
        state: oauth_state,
        device_type: q.device_type,
    };

    app.redis
        .make_auth_session(&session_id, &auth_session, GITHUB_OAUTH_STATE_TTL)?;

    Ok(Redirect::to(&oauth_login_url))
}

// /api/github/token
#[derive(Deserialize)]
pub struct TokenQuery {
    session_id: String,
    device_type: String,
    code: String,
    state: String,
}

pub async fn auth_token(
    State(app): State<Arc<AppState>>,
    Query(q): Query<TokenQuery>,
) -> Result<impl IntoResponse> {
    let auth_session = app.redis.get_auth_session(&q.session_id)?;

    if auth_session.state != q.state {
        Err(AppError::Response(
            StatusCode::UNAUTHORIZED,
            String::from("Invalid credentials."),
        ))?;
    }

    let github_oauth_token = app.github.fetch_user_auth_token(&q.code).await?;
    dbg!(&github_oauth_token);

    Ok(String::new())
}
