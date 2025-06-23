use std::time::Duration;

use anyhow::Context;
use reqwest::StatusCode;
use reqwest::header::{ACCEPT, AUTHORIZATION, HeaderName, HeaderValue, USER_AGENT};
use secrecy::{ExposeSecret, SecretString};
use serde::{Deserialize, Serialize};
use url::Url;

use crate::cache::UserSessionInternal;
use crate::errors::{AppError, Result};
use crate::utils::env::{env_or_default, env_or_panic};

const GITHUB_OAUTH_SCOPE: &'static str = "repo read:user";
pub const GITHUB_OAUTH_STATE_TTL: u64 = 120; // 2 minutes

#[derive(Debug, Deserialize, Clone)]
pub struct GitHubAuthToken {
    pub access_token: SecretString,
    pub token_type: String,
    pub scope: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct GitHubUserProfile {
    pub id: i64,
    pub login: String,
    pub name: String,
    pub email: Option<String>,
    pub avatar_url: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct RepoOwner {
    id: u64,
    login: String,
    avatar_url: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Repository {
    id: u64,
    full_name: String,
    private: bool,
    html_url: String,
    description: Option<String>,
    owner: RepoOwner,
}

pub struct GitHubAPI {
    oauth_client_id: String,
    oauth_client_secret: SecretString,
    oauth_redirect_uri: String,

    base_api: Url,

    http: reqwest::Client,
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
        headers.insert(USER_AGENT, HeaderValue::from_static("evault"));

        let http = reqwest::Client::builder()
            .default_headers(headers)
            .cookie_store(true)
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap();

        let base_api = Url::parse("https://api.github.com").expect("Invalid URL.");

        Self {
            oauth_client_id: env_or_panic("GITHUB_OAUTH_CLIENT_ID"),
            oauth_client_secret: env_or_panic("GITHUB_OAUTH_CLIENT_SECRET").into(),
            oauth_redirect_uri: env_or_default(
                "GITHUB_OAUTH_REDIRECT_URI",
                "http://localhost:5173/auth/github",
            ),

            base_api,

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
            .context("Failed to issue POST request")?;

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

    pub async fn fetch_user_profile(
        &self,
        gh_token: &GitHubAuthToken,
    ) -> Result<GitHubUserProfile> {
        let auth_header = HeaderValue::from_str(&format!(
            "{} {}",
            gh_token.token_type,
            gh_token.access_token.expose_secret()
        ))
        .context("Failed to format authorization header")?;

        let response = self
            .http
            .get("https://api.github.com/user")
            .header(AUTHORIZATION, auth_header)
            .send()
            .await
            .context("Failed to issue GET request.")?;

        if response.status() != StatusCode::OK {
            return Err(AppError::Response(
                response.status(),
                response
                    .text()
                    .await
                    .context("Failed to read response body.")?,
            ));
        }

        Ok(response
            .json::<GitHubUserProfile>()
            .await
            .context("Failed to parse GitHub user profile response")?)
    }

    pub async fn fetch_user_repositories(
        &self,
        token: &GitHubAuthToken,
    ) -> Result<Vec<Repository>> {
        let mut url = self.base_api.clone();
        url.path_segments_mut()
            .expect("invalid base url")
            .push("user")
            .push("repos");
        url.query_pairs_mut()
            .append_pair("sort", "pushed")
            .append_pair("direction", "desc");

        let token_str = format!(
            "{} {}",
            token.token_type,
            token.access_token.expose_secret()
        );
        let repos = self
            .http
            .get(url)
            .header(AUTHORIZATION, token_str)
            .send()
            .await
            .unwrap()
            .error_for_status()
            .map_err(|err| {
                let status = err.status().unwrap_or_else(|| StatusCode::BAD_GATEWAY);
                AppError::Response(
                    status,
                    "Failed to get repositories from GitHub.".to_string(),
                )
            })?
            .json::<Vec<Repository>>()
            .await
            .context("Failed to marshalized repositories")?;

        Ok(repos)
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
