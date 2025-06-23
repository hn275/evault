use std::sync::Arc;

use axum::Json;
use axum::extract::{Request, State};
use axum::response::IntoResponse;

use crate::app::AppState;
use crate::cache::UserSessionInternal;
use crate::errors::Result;

pub async fn repositories(
    State(app): State<Arc<AppState>>,
    request: Request,
) -> Result<impl IntoResponse> {
    let user = request
        .extensions()
        .get::<UserSessionInternal>()
        .expect("Missing authentication middleware in the stack.");

    let repos = app.github.fetch_user_repositories(&user.token).await?;
    Ok(Json(repos))
}
