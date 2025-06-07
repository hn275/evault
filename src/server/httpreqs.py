from typing import Optional
import requests
from shared.types import GitHubUser


class HttpClient(requests.Session):
    def __init__(self) -> None:
        super().__init__()

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

        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            return None

        data = req.json()
        return GitHubUser(
            id=data["id"],
            login=data["login"],
            name=data["name"],
            type=data["type"],
        )
