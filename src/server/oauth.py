from urllib.parse import urlencode, urlparse
from requests import Session
from shared.types import DeviceType, GitHubUser, GithubAuthToken
from typing import Optional


class GitHubClient(Session):
    access_token: str
    token_type: str

    def __init__(self, access_token: str, token_type: str) -> None:
        super().__init__()
        self.access_token = access_token
        self.token_type = token_type

    def get_user(self) -> Optional[GitHubUser]:
        headers = {
            "Authorization": f"{self.token_type} {self.access_token}",
            "Accept": "application/json; charset=utf-8",
        }
        r = self.get("https://api.github.com/user", headers=headers)
        assert r.status_code == 200
        d = r.json()

        return GitHubUser(
            id=d["id"],
            name=d["name"],
            login=d["login"],
            type=d["type"],
            email=d["email"],
        )


class GitHubOauth:
    client_id: str
    client_secret: str
    redirect_uri: str

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def make_web_login_url(
        self, oauth_state: str, session_id: str, device_type: DeviceType
    ) -> str:
        p = {
            "session_id": session_id,
            "device_type": device_type,
        }
        redirect_url = f"{self.redirect_uri}?{urlencode(p)}"

        p = {
            "client_id": self.client_id,
            "redirect_uri": redirect_url,
            "state": oauth_state,
            "scope": "repo:read read:user",
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(p)}"

    def make_cli_login_url(self) -> str:
        p = {
            "client_id": self.client_id,
        }
        return f"https://github.com/login/device/code?{urlencode(p)}"

    def make_cli_poll_url(self, device_code: str) -> str:
        p = {
            "client_id": self.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        return f"https://github.com/login/oauth/access_token?{urlencode(p)}"

    def make_web_access_tok_url(self, code: str) -> str:
        p = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        return f"https://github.com/login/oauth/access_token?{urlencode(p)}"
