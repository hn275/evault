from dataclasses import dataclass


@dataclass
class AuthData:
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int


@dataclass
class AuthToken:
    access_token: str
    token_type: str
    scope: str


@dataclass
class GitHubUser:
    id: int
    name: str
    login: str
    type: str
