import requests
import dacite
from . import oauth
from loguru import logger
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from fastapi import HTTPException, status
from src.pkg.types import GitHubUser, GithubAuthToken


@dataclass
class RepoOwner:
    id: int
    login: str
    avatar_url: str


@dataclass
class Repository:
    id: int
    full_name: str
    private: bool
    html_url: str
    description: Optional[str]
    owner: RepoOwner


base_url = "https://api.github.com"
_s = requests.Session()


def fetch_user_auth_token(auth_code: str) -> GithubAuthToken:
    auth_url = oauth.make_web_access_tok_url(auth_code)
    r = _s.post(
        auth_url,
        headers={
            "Accept": "application/vnd.github.raw+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    if r.status_code != status.HTTP_200_OK:
        logger.error("Failed to authenticate with GitHub", r.text())
        raise HTTPException(
            status_code=r.status_code,
            detail="Failed to authenticate with GitHub.",
        )

    return dacite.from_dict(GithubAuthToken, r.json())


def fetch_user_repositories(
    token_type: str,
    access_token: str,
) -> List[Repository]:
    """
    returns a list of `Repository`
    raises `HTTPException` if the network call fails.
    """
    url = f"{base_url}/user/repos"
    headers = _make_header(token_type, access_token)

    r = _s.get(
        url,
        headers=headers,
        params={"sort": "pushed", "direction": "desc"},
    )

    if r.status_code != status.HTTP_200_OK:
        logger.error("Failed to get repositories from GitHub:", r.text())
        raise HTTPException(
            r.status_code,
            "Failed to retrieve user's repositories from GitHub.",
        )

    repos_data = r.json()
    return [dacite.from_dict(Repository, r) for r in repos_data]


def fetch_github_credentials(
    token: GithubAuthToken,
) -> Tuple[GitHubUser, str | None]:
    """
    returns a tuple of `GitHubUser` and an optional user email
    raises `HTTPException` if the network call fails.
    """
    url = "https://api.github.com/user"
    headers = _make_header(token.token_type, token.access_token)

    req = _s.get(url, headers=headers)
    if req.status_code != status.HTTP_200_OK:
        logger.error("Failed to get repositories from GitHub:", req.text())
        raise HTTPException(
            req.status_code,
            "Failed to retrieve user's data from GitHub.",
        )

    data = req.json()
    user_email: str | None = data.get("email")

    return (dacite.from_dict(GitHubUser, data), user_email)


def fetch_repository(
    token_type: str,
    access_token: str,
    repo_owner: str,
    repo_name: str,
) -> Repository:
    """
    returns a `Repository`
    raises `HTTPException` if the network call fails.
    """
    url = f"{base_url}/repos/{repo_owner}/{repo_name}"
    headers = _make_header(token_type, access_token)

    r = _s.get(url, headers=headers)
    if r.status_code != status.HTTP_200_OK:
        logger.error("Failed to fetch repository from GitHub:", r.text())
        raise HTTPException(
            status_code=r.status_code,
            content="Failed to fetch repository from GitHub.",
        )

    return dacite.from_dict(Repository, r.json())


def _make_header(
    token_type: str,
    token: str,
    opts: Dict[str, str] = {},
) -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"{token_type} {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    for k, v in opts:
        headers[k] = v

    return headers
