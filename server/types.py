from dataclasses import asdict, dataclass
import flatten_dict
from pydantic import BaseModel
from typing import Dict, Literal
import dacite

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
    avatar_url: str


_FLATTEN_DICT_REDUCER = "dot"


@dataclass
class UserSession:
    device_type: DeviceType
    user: GitHubUser
    gh_token: GithubAuthToken
    csrf_token: str | None = None

    @staticmethod
    def from_flat_map(flat_map: Dict[str, int | str]) -> "UserSession":
        m = flatten_dict.unflatten(flat_map, splitter=_FLATTEN_DICT_REDUCER)
        return UserSession(
            device_type=m["device_type"],
            user=dacite.from_dict(GitHubUser, m["user"]),
            gh_token=dacite.from_dict(GithubAuthToken, m["gh_token"]),
            csrf_token=m.get("csrf_token", None),
        )

    def make_flat_map(self) -> Dict[str, int | str]:
        m = {
            "device_type": self.device_type,
            "user": asdict(self.user),
            "gh_token": asdict(self.gh_token),
        }
        csrf = m.get("csrf_token", None)
        if csrf:
            m["csrf_token"] = csrf

        return flatten_dict.flatten(m, reducer=_FLATTEN_DICT_REDUCER)


class RequestCookieBase(BaseModel):
    evault_access_token: str
