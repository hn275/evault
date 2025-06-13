from dataclasses import dataclass
import json, dacite
from typing import Dict, List, Optional
import requests
from ..pkg.types import GitHubUser


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


class HttpClient(requests.Session):
    base_url: str

    def __init__(self) -> None:
        super().__init__()
        self.base_url = f"https://api.github.com"

    def fetch_user_repositories(
        self, token_type: str, access_token: str
    ) -> List[Repository]:
        url = f"{self.base_url}/user/repos"
        headers = self._make_header(token_type, access_token)

        r = self.get(url, headers=headers, params={"sort": "pushed", "direction": "desc"})
        assert r.status_code == 200

        repos_data = r.json()
        return [dacite.from_dict(Repository, repo_data) for repo_data in repos_data]

    def fetch_github_credentials(
        self, token_type: str, access_token: str
    ) -> Optional[GitHubUser]:
        """returns None if token is expired"""
        # get user information
        url = f"https://api.github.com/user"
        headers = self._make_header(token_type, access_token)

        req = self.get(url, headers=headers)
        if req.status_code != 200:
            return None

        data = req.json()

        # if the user has MFA, they do not have an email, set as N/A
        if data["email"] is None:
            data["email"] = "N/A"

        return dacite.from_dict(GitHubUser, data)

    def fetch_repository(
        self,
        token_type: str,
        access_token: str,
        repo_owner: str,
        repo_name: str,
    ) -> Repository:
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}"
        headers = self._make_header(token_type, access_token)
        r = self.get(url, headers=headers)
        assert r.status_code == 200
        return dacite.from_dict(Repository, r.json())

    def _make_header(
        self,
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
