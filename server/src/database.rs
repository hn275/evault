use anyhow::Context;
use sqlx::{PgPool, Pool, Postgres};
use tracing::info;

use crate::{github::GitHubUserProfile, utils::env::env_or_panic};

pub struct Database {
    pool: Pool<Postgres>,
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

    pub async fn create_github_user(&self, user: &GitHubUserProfile) -> anyhow::Result<()> {
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
        .unwrap();
        // .context("Failed to create GitHub user.")?;

        Ok(())
    }
}
