use std::sync::Arc;

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Redirect},
};
use serde::Deserialize;

use crate::app::AppState;
use crate::errors::Result;
use crate::secrets;

#[derive(Deserialize)]
pub struct AuthQuery {
    pub device_type: String,
}

#[axum::debug_handler]
pub async fn auth(
    State(app): State<Arc<AppState>>,
    Query(q): Query<AuthQuery>,
) -> Result<Redirect> {
    let oauth_state = secrets::token_urlsafe(32)?;
    let session_id = secrets::token_urlsafe(16)?;
    let oauth_login_url = app
        .github
        .make_login_url(&oauth_state, &session_id, &q.device_type)?;

    Ok(Redirect::to(&oauth_login_url))
}
