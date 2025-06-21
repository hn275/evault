use anyhow::Context;
use url::Url;

use crate::errors::Result;
use crate::utils::env::{env_or_default, env_or_panic};

const GITHUB_OAUTH_SCOPE: &'static str = "repo read:user";

pub struct GitHubAPI {
    oauth_client_id: String,
    oauth_client_secret: String,
    oauth_redirect_uri: String,
}

impl GitHubAPI {
    pub fn new() -> Self {
        Self {
            oauth_client_id: env_or_panic("GITHUB_OAUTH_CLIENT_ID"),
            oauth_client_secret: env_or_panic("GITHUB_OAUTH_CLIENT_SECRET"),
            oauth_redirect_uri: env_or_default(
                "GITHUB_OAUTH_REDIRECT_URI",
                "http://localhost:5173/auth/github",
            ),
        }
    }

    pub fn make_login_url(
        &self,
        state: &str,
        session_id: &str,
        device_type: &str,
    ) -> Result<String> {
        let mut redirect_url =
            Url::parse(&self.oauth_redirect_uri).context("Failed to parse github redirect uri")?;

        redirect_url
            .query_pairs_mut()
            .append_pair("session_id", session_id)
            .append_pair("device_type", device_type);
        let redirect_url = redirect_url.to_string();

        let mut oauth_url = Url::parse("https://github.com/login/oauth/authorize")
            .context("Failed to parse github oauth url")?;

        oauth_url
            .query_pairs_mut()
            .append_pair("client_id", &self.oauth_client_id)
            .append_pair("redirect_uri", &redirect_url)
            .append_pair("state", state)
            .append_pair("scope", GITHUB_OAUTH_SCOPE);

        Ok(oauth_url.to_string())
    }
}
