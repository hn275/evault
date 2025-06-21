use crate::github::GitHubAPI;

pub struct AppState {
    pub github: GitHubAPI,
}

impl AppState {
    pub fn initialize() -> Self {
        return Self {
            github: GitHubAPI::new(),
        };
    }
}
