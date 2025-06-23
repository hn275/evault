use std::sync::Arc;

use axum::extract::{Query, Request, State};
use axum::response::IntoResponse;
use axum::{Json, debug_handler};
use serde::{Deserialize, Serialize};

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

#[derive(Serialize, Deserialize)]
pub struct RepositoryQuery {
    pub repo_owner: String,
    pub repo_name: String,
    pub repo_id: u64,
}

#[derive(Serialize, Deserialize)]
pub struct RepositoryResponse {
    pub vault_initialized: bool,
    is_admin: bool,
}

pub async fn repository(
    State(app): State<Arc<AppState>>,
    Query(query): Query<RepositoryQuery>,
    request: Request,
) -> Result<impl IntoResponse> {
    let user = request
        .extensions()
        .get::<UserSessionInternal>()
        .expect("Missing authentication middleware in the stack.");

    let repository = app.database.get_repo_by_id(query.repo_id).await?;

    // if the vault for this repo is initialized
    if let Some(repo) = repository {
        return Ok(Json(RepositoryResponse {
            vault_initialized: true,
            is_admin: repo.owner_id as u64 == user.user_id,
        }));
    }

    // vault not initialized, need to verify the request to be the repo owner
    let remote_repo = app
        .github
        .fetch_repository(&user.token, &query.repo_owner, &query.repo_name)
        .await?;

    Ok(Json(RepositoryResponse {
        vault_initialized: false,
        is_admin: remote_repo.owner.id as u64 == user.user_id,
    }))
}
