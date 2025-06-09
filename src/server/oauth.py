from urllib.parse import urlencode, urlparse
from requests import Session
from shared.types import DeviceType, GitHubUser, GithubAuthToken
from typing import Optional


class GitHubOauth:
    client_id: str
    client_secret: str
    redirect_uri: str

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def make_login_url(
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
            "scope": "repo read:user",
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
