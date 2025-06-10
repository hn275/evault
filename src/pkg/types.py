from dataclasses import dataclass
from pydantic import BaseModel
from typing import Annotated, Literal
import fastapi

type DeviceType = Literal["web", "cli"]


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
    email: str
    avatar_url: str


class RequestCookieBase(BaseModel):
    evault_access_token: str


# type Cookie = Annotated[RequestCookieBase, fastapi.Cookie()]
type Cookie = Annotated[str, fastapi.Cookie()]
