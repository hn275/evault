use axum::extract::Request;

use crate::cache::UserSession;

pub async fn user(request: Request) -> String {
    let user = request
        .extensions()
        .get::<UserSession>()
        .expect("Session not found.");
    dbg!(user);

    String::from("Hello world")
}
