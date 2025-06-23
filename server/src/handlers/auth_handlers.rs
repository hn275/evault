use std::sync::Arc;

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Redirect},
};
use axum_extra::extract::cookie::{Cookie, CookieJar};
use serde::Deserialize;

use crate::{
    app::AppState,
    cache::{EVAULT_SESSION_TTL, RedisAuthSession, UserSessionInternal},
    errors::{AppError, Result},
    github::GITHUB_OAUTH_STATE_TTL,
    handlers::COOKIE_ACCESS_TOKEN_KEY,
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
    #[allow(unused)] // TODO: add support for CLI login
    device_type: String,
    code: String,
    state: String,
}

pub async fn auth_token(
    State(app): State<Arc<AppState>>,
    Query(q): Query<TokenQuery>,
    cookie_jar: CookieJar,
) -> Result<impl IntoResponse> {
    let auth_session = app.redis.get_auth_session(&q.session_id)?;

    if auth_session.state != q.state {
        Err(AppError::Response(
            StatusCode::UNAUTHORIZED,
            String::from("Invalid credentials."),
        ))?;
    }

    let github_oauth_token = app.github.fetch_user_auth_token(&q.code).await?;
    let user_profile = app.github.fetch_user_profile(&github_oauth_token).await?;
    let evault_access_token = secrets::token_urlsafe(32)?;

    let user_session = UserSessionInternal {
        session_id: evault_access_token,
        user_id: user_profile.id as u64,
        user_name: user_profile.name.clone(),
        user_avatar_url: user_profile.avatar_url.clone(),
        user_login: user_profile.login.clone(),
        token: github_oauth_token,
    };

    app.redis
        .create_user_session(&user_session, EVAULT_SESSION_TTL)?;

    app.database.create_github_user(&user_profile).await?;

    let session_cookie = Cookie::build((COOKIE_ACCESS_TOKEN_KEY, user_session.session_id))
        .path("/")
        .build();

    let jar = cookie_jar.add(session_cookie);

    Ok((StatusCode::OK, jar))
}
