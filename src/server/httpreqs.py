from dataclasses import dataclass
import json, dacite
from typing import List, Optional
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
    def __init__(self) -> None:
        super().__init__()

    def fetch_user_repositories(
        self, token_type: str, access_token: str
    ) -> List[Repository]:
        url = f"https://api.github.com/user/repos"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"{token_type} {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        r = self.get(url, headers=headers)
        assert r.status_code == 200

        repos_data = r.json()
        return [dacite.from_dict(Repository, repo_data) for repo_data in repos_data]

    def fetch_github_credentials(
        self, token_type: str, access_token: str
    ) -> Optional[GitHubUser]:
        """returns None if token is expired"""
        # get user information
        url = f"https://api.github.com/user"
        headers = {
            "Authorization": f"{token_type} {access_token}",
            "Accept": "application/json",
        }

        req = self.get(url, headers=headers)
        if req.status_code != 200:
            return None

        data = req.json()
        return GitHubUser(
            id=data["id"],
            login=data["login"],
            name=data["name"],
            type=data["type"],
            email=data["email"],
            avatar_url=data["avatar_url"],
        )
