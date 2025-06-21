use axum::{Json, http::StatusCode, response::IntoResponse};
use serde_json::json;
use tracing::error;

pub enum AppError {
    Internal(anyhow::Error),
    Response(StatusCode, String),
}

pub type Result<T> = std::result::Result<T, AppError>;

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        match self {
            AppError::Internal(err) => {
                error!("Something went wrong: {}", err);
                let body = json!({ "detail": err.to_string() });
                (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response()
            }
            AppError::Response(code, err) => {
                let body = json!({ "detail": err });
                (code, Json(body)).into_response()
            }
        }
    }
}

impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        AppError::Internal(err)
    }
}
