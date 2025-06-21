use std::collections::HashMap;
use std::time::Duration;

use anyhow::{Context, anyhow};
use redis::Commands;
use redis_macros::{FromRedisValue, ToRedisArgs};
use reqwest::StatusCode;
use serde::{Deserialize, Serialize};
use tracing::info;

use crate::errors::{AppError, Result};
use crate::utils::env::env_or_panic;

#[derive(ToRedisArgs, FromRedisValue, Deserialize, Serialize)]
pub struct RedisAuthSession {
    pub state: String,
    pub device_type: String,
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
        let result = self
            .pool
            .get()
            .context("Failed to get Redis connection.")?
            .hgetall::<_, HashMap<String, String>>(key)
            .context("Failed to deserialize authentication session.")?;

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

    fn make_auth_url_key(session_id: &str) -> String {
        format!("evault-auth-session:{}", session_id)
    }
}
