use std::sync::Arc;

use axum::{
    extract::{Request, State},
    http::{HeaderMap, Response, StatusCode},
    middleware::{self, Next},
    response::IntoResponse,
};
use axum_extra::extract::CookieJar;
use tracing::{trace, warn};

use crate::errors::Result;
use crate::{app::AppState, errors::AppError, handlers::COOKIE_ACCESS_TOKEN_KEY};

pub async fn authenticated_requests(
    State(app): State<Arc<AppState>>,
    cookie_jar: CookieJar,
    mut request: Request,
    next: Next,
) -> Result<impl IntoResponse> {
    let auth_cookie = cookie_jar.get(COOKIE_ACCESS_TOKEN_KEY).ok_or_else(|| {
        AppError::Response(StatusCode::FORBIDDEN, String::from("Missing credentials."))
    })?;

    let user_session_id = auth_cookie.value();
    dbg!(&user_session_id);
    Ok("")
}
