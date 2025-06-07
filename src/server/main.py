import json, time, requests, os, math, secrets
from urllib.parse import urlencode
from typing import Literal, Optional
import fastapi
from shared.types import GithubAuthToken, GitHubUser
from .cache import Cache, REDIS_HOST


app = fastapi.FastAPI()
redis = Cache(REDIS_HOST)
GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
EVAULT_SESSION_TOK_EXP = 300

type DeviceType = Literal["web", "cli"]


@app.get("/api/auth")
async def auth(device_type: DeviceType):
    if device_type == "web":
        raise NotImplemented
    else:
        params = {
            "client_id": GITHUB_OAUTH_CLIENT_ID,
        }
        return fastapi.Response(
            content=f"https://github.com/login/device/code?{urlencode(params)}",
            media_type="text/plain",
        )


@app.get("/api/auth/device")
def auth_github(
    device_code: str,
    # user_code: str,
    # verification_uri: str,
    expires_in: int,
    interval: int,
):
    # poll for access token
    p = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    headers = {"Accept": "application/json"}

    url = f"https://github.com/login/oauth/access_token?{urlencode(p)}"
    attempt = 0
    gh_oauth_tok: Optional[GithubAuthToken] = None

    max_attempts = math.ceil(expires_in / interval)
    while attempt <= max_attempts:
        attempt += 1

        req = requests.post(url, headers=headers)

        assert req.status_code == 200
        data = req.json()

        if "error" in data:
            if data["error"] == "authorization_pending":
                time.sleep(interval)
                continue
            else:
                return fastapi.Response(
                    status_code=403, content=data["error_description"]
                )

        gh_oauth_tok = GithubAuthToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            scope=data["scope"],
        )
        break

    if gh_oauth_tok == None:
        return fastapi.Response(
            status_code=403, content="Request for user's information timed out."
        )

    # get user information
    url = f"https://api.github.com/user"
    headers = {
        "Authorization": f"{gh_oauth_tok.token_type} {gh_oauth_tok.access_token}",
        "Accept": "application/json",
    }

    req = requests.get(url, headers=headers)
    assert req.status_code == 200

    # create an evault access token, then cache it
    evault_access_token = secrets.token_urlsafe(32)
    redis.cache_user_token(
        evault_access_token, gh_oauth_tok.access_token, EVAULT_SESSION_TOK_EXP
    )

    data = req.json()
    github_user = GitHubUser(
        id=data["id"],
        login=data["login"],
        name=data["name"],
        type=data["type"],
    )
    body = json.dumps(github_user.__dict__)

    res = fastapi.Response(content=body, media_type="application/json")
    res.set_cookie(
        key="evault_access_token",
        value=evault_access_token,
        expires=EVAULT_SESSION_TOK_EXP,
    )
    return res
