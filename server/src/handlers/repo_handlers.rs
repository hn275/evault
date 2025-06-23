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
    pub read_access: bool,
    pub write_access: bool,
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
        if repo.owner_id == user.user_id {
            return Ok(Json(RepositoryResponse {
                vault_initialized: true,
                read_access: true,
                write_access: true,
            }));
        }

        // TODO: not repo owner, need to check for read/write access.
        return Ok(Json(RepositoryResponse {
            vault_initialized: true,
            read_access: false,
            write_access: false,
        }));
    }

    Ok(Json(RepositoryResponse {
        vault_initialized: false,
        read_access: false,
        write_access: false,
    }))
}
