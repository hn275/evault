use anyhow::Context;
use serde::{Deserialize, Serialize};
use sqlx::{PgPool, Pool, Postgres, Row, prelude::FromRow};
use tracing::{error, info};

use crate::{errors::Result, github::GitHubUserProfile, utils::env::env_or_panic};

pub struct Database {
    pool: Pool<Postgres>,
}

#[derive(FromRow, Serialize, Deserialize)]
pub struct Repository {
    pub id: i64,
    pub name: String,
    pub owner_id: i64,
    pub bucket_addr: Option<String>,
    pub password: String,
}

impl Database {
    pub async fn new() -> anyhow::Result<Self> {
        let conn_str = format!(
            "postgresql://{}:{}@{}:{}/{}?sslmode={}",
            env_or_panic("POSTGRES_USER"),
            env_or_panic("POSTGRES_PASSWORD"),
            env_or_panic("POSTGRES_HOST"),
            env_or_panic("POSTGRES_PORT"),
            env_or_panic("POSTGRES_DBNAME"),
            env_or_panic("POSTGRES_SSL")
        );

        let pool = PgPool::connect(&conn_str)
            .await
            .context("Failed to connect to database.")?;

        info!("Connected to PostGres database.");

        Ok(Database { pool })
    }

    pub async fn create_github_user(&self, user: &GitHubUserProfile) -> Result<()> {
        sqlx::query(
            "
            INSERT INTO users (id, login, email, name)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id)
            DO UPDATE SET
                login = EXCLUDED.login,
                email = EXCLUDED.email,
                name = EXCLUDED.name;
            ",
        )
        .bind(user.id as i64)
        .bind(&user.login)
        .bind(&user.email)
        .bind(&user.name)
        .execute(&self.pool)
        .await
        .context("Failed to create GitHub user.")?;

        Ok(())
    }

    pub async fn get_repo_by_id(&self, repo_id: u64) -> Result<Option<Repository>> {
        Ok(sqlx::query_as::<_, Repository>(
            "
            SELECT id, name, owner_id, bucket_addr, password
            FROM repositories
            WHERE id = $1;
            ",
        )
        .bind(repo_id as i64)
        .fetch_optional(&self.pool)
        .await
        .context("Failed to query for repository")?)
    }
}
