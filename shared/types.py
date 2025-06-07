from dataclasses import dataclass


@dataclass
class AuthDataDevice:
    device_code: str
    expires_in: int
    interval: int


@dataclass
class GithubAuthToken:
    access_token: str
    token_type: str
    scope: str


@dataclass
class GitHubUser:
    id: int
    name: str
    login: str
    type: str
