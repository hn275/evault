use crate::{cache::Redis, database::Database, github::GitHubAPI};

pub struct AppState {
    pub github: GitHubAPI,
    pub redis: Redis,
    pub database: Database,
}
