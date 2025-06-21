use std::time::Duration;

use anyhow::Context;
use reqwest::header::{ACCEPT, HeaderValue};
use secrecy::{ExposeSecret, SecretString};
use serde::Deserialize;
use url::Url;

use crate::errors::{AppError, Result};
use crate::utils::env::{env_or_default, env_or_panic};

const GITHUB_OAUTH_SCOPE: &'static str = "repo read:user";
pub const GITHUB_OAUTH_STATE_TTL: u64 = 120; // 2 minutes

pub struct GitHubAPI {
    oauth_client_id: String,
    oauth_client_secret: SecretString,
    oauth_redirect_uri: String,

    http: reqwest::Client,
}

#[derive(Debug, Deserialize)]
pub struct GitHubAuthToken {
    access_token: String,
    token_type: String,
    scope: String,
}

impl GitHubAPI {
    pub fn new() -> Self {
        let mut headers = reqwest::header::HeaderMap::new();
        headers.insert(
            "X-GitHub-Api-Version",
            HeaderValue::from_static("2022-11-28"),
        );
        headers.insert(
            ACCEPT,
            HeaderValue::from_static("application/vnd.github+json"),
        );

        let http = reqwest::Client::builder()
            .default_headers(headers)
            .cookie_store(true)
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap();

        Self {
            oauth_client_id: env_or_panic("GITHUB_OAUTH_CLIENT_ID"),
            oauth_client_secret: env_or_panic("GITHUB_OAUTH_CLIENT_SECRET").into(),
            oauth_redirect_uri: env_or_default(
                "GITHUB_OAUTH_REDIRECT_URI",
                "http://localhost:5173/auth/github",
            ),

            http,
        }
    }

    pub async fn fetch_user_auth_token(&self, auth_code: &str) -> Result<GitHubAuthToken> {
        let url = self.make_github_oauth_url(auth_code)?;
        let response = self
            .http
            .post(url)
            .send()
            .await
            .context("Failed to build request")?;

        if response.status() != reqwest::StatusCode::OK {
            Err(AppError::Response(
                response.status().into(),
                "Failed to fetch user credentials from GitHub.".to_string(),
            ))?;
        }

        Ok(response
            .json::<GitHubAuthToken>()
            .await
            .context("Failed to parse GitHub access token response")?)
    }

    fn make_github_oauth_url(&self, code: &str) -> Result<String> {
        let mut oauth_url =
            Url::parse("https://github.com").context("Failed to parse GitHub URL")?;
        oauth_url
            .path_segments_mut()
            .map_err(|_| anyhow::anyhow!("Invalid GitHub URL"))?
            .extend(&["login", "oauth", "access_token"]);
        oauth_url
            .query_pairs_mut()
            .append_pair("client_id", &self.oauth_client_id)
            .append_pair("client_secret", &self.oauth_client_secret.expose_secret())
            .append_pair("code", code);

        Ok(oauth_url.to_string())
    }

    pub fn make_login_url(
        &self,
        session_id: &str,
        state: &str,
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
