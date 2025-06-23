use std::sync::Arc;

use axum::{
    extract::{Query, State},
    response::{IntoResponse, Redirect},
};
use serde::Deserialize;

use crate::{app::AppState, errors::Result, github::GITHUB_OAUTH_STATE_TTL, secrets};

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
        .make_login_url(&oauth_state, &session_id, &q.device_type)?;

    app.redis
        .cache_auth_url(&session_id, &oauth_login_url, GITHUB_OAUTH_STATE_TTL)?;

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
    let a = app.redis.get_del_auth_url("alskdflksdflkj")?;
    dbg!(a);
    Ok(String::new())
}
