use std::time::Duration;

use anyhow::Context;
use redis::Commands;

use crate::errors::{AppError, Result};
use crate::utils::env::env_or_panic;

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

    pub fn cache_auth_url(&self, session_id: &str, auth_url: &str, ttl: u64) -> Result<()> {
        let key = Self::make_auth_url_key(session_id);
        Ok(self
            .pool
            .get()
            .context("Failed to get Redis connection.")?
            .set_ex(key, auth_url, ttl)
            .context("Failed to cache authentication URL.")?)
    }

    pub fn get_del_auth_url(&self, session_id: &str) -> Result<Option<String>> {
        let key = Self::make_auth_url_key(session_id);
        Ok(self
            .pool
            .get()
            .context("Failed to get Redis connection.")?
            .get_del::<_, Option<String>>(key)
            .context("Failed to get and delete authentication URL for session.")?)
    }

    fn make_auth_url_key(session_id: &str) -> String {
        format!("evault-auth-session:{}", session_id)
    }
}
