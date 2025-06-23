use std::sync::Arc;

use axum::{
    extract::{Request, State},
    http::StatusCode,
    middleware::Next,
    response::{IntoResponse, Response},
};
use axum_extra::extract::CookieJar;

use crate::{app::AppState, errors::AppError, handlers::COOKIE_ACCESS_TOKEN_KEY};

pub async fn authenticated_requests(
    State(app): State<Arc<AppState>>,
    cookie_jar: CookieJar,
    mut request: Request,
    next: Next,
) -> Response {
    let auth_cookie = if let Some(cookie) = cookie_jar.get(COOKIE_ACCESS_TOKEN_KEY) {
        cookie
    } else {
        return AppError::Response(StatusCode::FORBIDDEN, "Missing credentials.".to_string())
            .into_response();
    };

    // TODO: test to see if the cookie is expired (do i even have to?)

    match app.redis.get_user_session(auth_cookie.value()) {
        Ok(user_session) => {
            request.extensions_mut().insert(user_session);
            // TODO: extend the session.
            next.run(request).await
        }
        Err(err) => err.into_response(),
    }
}
