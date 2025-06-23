use axum::Json;
use axum::extract::Request;
use axum::response::IntoResponse;

use crate::cache::UserSessionInternal;
use crate::errors::Result;
use crate::github::GitHubUserProfile;

pub async fn user(request: Request) -> Result<impl IntoResponse> {
    let user = request
        .extensions()
        .get::<UserSessionInternal>()
        .expect("Missing authentication middleware in the stack.");

    let user = GitHubUserProfile {
        id: user.user_id,
        login: user.user_login.clone(),
        name: user.user_name.clone(),
        email: None, // not saved in user session, will always default to `None`
        avatar_url: user.user_avatar_url.clone(),
    };

    Ok(Json(user))
}
