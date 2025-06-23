use std::collections::HashMap;
use std::time::Duration;

use anyhow::Context;
use axum::http::StatusCode;
use redis::{Commands, FromRedisValue, ToRedisArgs};
use redis_macros::{FromRedisValue, ToRedisArgs};
use secrecy::ExposeSecret;
use serde::{Deserialize, Serialize};
use tracing::{error, info};

use crate::errors::{AppError, Result};
use crate::github::GitHubAuthToken;
use crate::utils::env::env_or_panic;

pub const EVAULT_SESSION_TTL: u64 = 300; // 5 minutes

#[derive(ToRedisArgs, FromRedisValue, Deserialize, Serialize)]
pub struct RedisAuthSession {
    pub state: String,
    pub device_type: String,
}

#[derive(Debug, Clone)]
pub struct UserSession {
    pub session_id: String,
    pub user_id: u64,
    pub token: GitHubAuthToken,

    // these are served to the client side, but we don't really need to read these
    #[allow(unused)]
    pub user_avatar_url: String,
    #[allow(unused)]
    pub user_name: String,
}

impl FromRedisValue for UserSession {
    fn from_redis_value(v: &redis::Value) -> redis::RedisResult<Self> {
        let m: HashMap<String, String> = HashMap::from_redis_value(v)?;
        if m.is_empty() {
            return Err(redis::RedisError::from((
                redis::ErrorKind::TypeError,
                "Empty hash data",
            )));
        }
        Ok(UserSession {
            session_id: String::default(), // since the session id is the key
            user_id: m
                .get("user.id")
                .expect("`user.id` not found.")
                .parse::<_>()
                .unwrap(),
            token: GitHubAuthToken {
                access_token: m
                    .get("token.value")
                    .expect("`token.value` not found.")
                    .to_owned()
                    .into(),
                token_type: m
                    .get("token.type")
                    .expect("`token.type` not found.")
                    .to_string(),
                scope: m
                    .get("token.scope")
                    .expect("`token.scope` not found.")
                    .to_owned(),
            },
            user_avatar_url: String::default(),
            user_name: String::default(),
        })
    }
}

pub struct Redis {
    pool: r2d2::Pool<redis::Client>,
}

impl Redis {
    pub fn new() -> anyhow::Result<Self> {
        let conn_str = format!(
            "redis://{}:{}",
            env_or_panic("REDIS_HOST"),
            env_or_panic("REDIS_PORT")
        );

        let client = redis::Client::open(conn_str).context("Failed to connect to Redis server.")?;
        let pool = r2d2::Pool::builder()
            .max_size(15)
            .min_idle(Some(5))
            .connection_timeout(Duration::from_secs(30))
            .idle_timeout(Some(Duration::from_secs(600)))
            .max_lifetime(Some(Duration::from_secs(3600)))
            .build(client)
            .context("Failed to build Redis pool.")?;

        info!("Connected to Redis server.");

        Ok(Redis { pool })
    }

    pub fn make_auth_session(
        &self,
        session_id: &str,
        auth_session: &RedisAuthSession,
        ttl: u64,
    ) -> Result<()> {
        let key = Self::make_auth_url_key(session_id);
        let opts = redis::HashFieldExpirationOptions::default()
            .set_existence_check(redis::FieldExistenceCheck::FNX)
            .set_expiration(redis::SetExpiry::EX(ttl));

        Ok(self
            .pool
            .get()
            .context("Failed to get Redis connection.")?
            .hset_ex(
                key,
                &opts,
                &[
                    ("state", &auth_session.state),
                    ("device_type", &auth_session.device_type),
                ],
            )
            .context("Failed to cache authentication URL.")?)
    }

    pub fn get_auth_session(&self, session_id: &str) -> Result<RedisAuthSession> {
        let key = Self::make_auth_url_key(session_id);
        let mut conn = self.pool.get().context("Failed to get Redis connection.")?;
        let result = conn
            .hgetall::<_, HashMap<String, String>>(&key)
            .context("Failed to deserialize authentication session.")?;

        if result.is_empty() {
            Err(AppError::Response(
                StatusCode::UNAUTHORIZED,
                String::from("Authentication failed."),
            ))?
        }

        let _: () = conn
            .del(key)
            .context("Failed to remove authentication session.")?;

        Ok(RedisAuthSession {
            state: result
                .get("state")
                .context("Key `state` does not exist.")?
                .to_owned(),
            device_type: result
                .get("device_type")
                .context("Key `device_type` does not exist.")?
                .to_owned(),
        })
    }

    pub fn create_user_session(&self, session: &UserSession, ttl: u64) -> Result<()> {
        let key = Self::make_user_session_key(&session.session_id);
        let opts = redis::HashFieldExpirationOptions::default()
            .set_existence_check(redis::FieldExistenceCheck::FNX)
            .set_expiration(redis::SetExpiry::EX(ttl));

        let _: () = self
            .pool
            .get()
            .context("Failed to get Redis connection.")?
            .hset_ex(
                key,
                &opts,
                &[
                    ("user.id", session.user_id.to_redis_args()),
                    (
                        "token.value",
                        session.token.access_token.expose_secret().to_redis_args(),
                    ),
                    ("token.type", session.token.token_type.to_redis_args()),
                    ("token.scope", session.token.scope.to_redis_args()),
                ],
            )
            .map_err(|err| {
                error!(
                    "Failed to create user session: {}, {}",
                    session.session_id, err
                );
                AppError::Response(
                    StatusCode::UNAUTHORIZED,
                    "Failed to create user session".to_string(),
                )
            })?;

        Ok(())
    }

    pub fn get_user_session(&self, session_id: &str) -> Result<UserSession> {
        let mut user_session = self
            .pool
            .get()
            .context("")?
            .hgetall::<_, UserSession>(Self::make_user_session_key(session_id))
            .map_err(|err| match err.kind() {
                redis::ErrorKind::TypeError => {
                    AppError::Response(StatusCode::FORBIDDEN, "Session expired.".to_owned())
                }
                _ => AppError::Internal(err.into()),
            })?;

        user_session.session_id = session_id.to_owned();

        Ok(user_session)
    }

    fn make_auth_url_key(session_id: &str) -> String {
        format!("evault-auth-session:{}", session_id)
    }
    fn make_user_session_key(session_id: &str) -> String {
        format!("evault-user-session:{}", session_id)
    }
}
