use axum::{Json, http::StatusCode, response::IntoResponse};
use serde::Serialize;
use tracing::error;

pub struct ApiError {
    pub detail: String,
    pub code: StatusCode,
}

pub enum AppError {
    Internal(anyhow::Error),
    Response(ApiError),
}

pub type Result<T> = std::result::Result<T, AppError>;

#[derive(Serialize)]
struct ErrorMessage {
    detail: String,
}
impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        match self {
            AppError::Internal(err) => {
                error!("Something went wrong: {}", err);
                let msg = ErrorMessage {
                    detail: String::from("Something went wrong."),
                };
                (StatusCode::INTERNAL_SERVER_ERROR, Json(msg)).into_response()
            }
            AppError::Response(err) => {
                let msg = ErrorMessage { detail: err.detail };
                (err.code, Json(msg)).into_response()
            }
        }
    }
}

impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        AppError::Internal(err)
    }
}
