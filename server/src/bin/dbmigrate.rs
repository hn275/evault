use sqlx::{PgPool, migrate::Migrator};
use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = env::var("DATABASE_URL").expect("DATABASE_URL not set.");
    // Create database connection
    let pool = PgPool::connect(&url).await?;

    // Embed migrations at compile time
    static MIGRATOR: Migrator = sqlx::migrate!("./migrations");

    // Run migrations
    MIGRATOR.run(&pool).await?;

    println!("Database migrated successfully!");
    Ok(())
}
