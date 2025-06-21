use crate::{cache::Redis, github::GitHubAPI};

pub struct AppState {
    pub github: GitHubAPI,
    pub redis: Redis,
}
