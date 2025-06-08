import json, time, requests, os, math, secrets, threading
from urllib.parse import urlencode
from typing import Literal, Optional
import fastapi
from shared.types import GithubAuthToken, GitHubUser
from shared.utils import env_or_default
from redis import Redis
from .httpreqs import HttpClient
from .oauth import GitHubOauth


GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
GITHUB_OAUTH_REDIRECT_URI = env_or_default(
    "GITHUB_OAUTH_REDIRECT_URI", "http://localhost:5173/auth/github"
)
GITHUB_OAUTH_STATE_TTL = 120  # 2 minutes
EVAULT_SESSION_TOK_EXP = 300  # 5 minutes
REDIS_HOST = env_or_default("REDIS_HOST", "localhost")
REDIS_PORT_DEFAULT = 6379

redis = Redis(REDIS_HOST, port=REDIS_PORT_DEFAULT)
redis.ping()

app = fastapi.FastAPI()
httpclient = HttpClient()

type DeviceType = Literal["web", "cli"]

oauth_client = GitHubOauth(
    client_id=GITHUB_OAUTH_CLIENT_ID,
    client_secret=GITHUB_OAUTH_CLIENT_SECRET,
    redirect_uri=GITHUB_OAUTH_REDIRECT_URI,
)


@app.get("/api/auth")
async def auth(device_type: DeviceType):
    login_url: str
    if device_type == "web":
        oauth_state = secrets.token_urlsafe(16)
        redis.set(f"github-oauth-state:{oauth_state}", "", ex=GITHUB_OAUTH_STATE_TTL)
        login_url = oauth_client.make_web_login_url(oauth_state)
    else:
        login_url = oauth_client.make_cli_login_url()

    return fastapi.Response(
        content=login_url,
        media_type="text/plain",
    )


@app.get("/api/auth/device")
async def auth_github(
    device_code: str,
    # user_code: str,
    # verification_uri: str,
    expires_in: int,
    interval: int,
):
    # poll for access token
    gh_oauth_tok: Optional[GithubAuthToken] = None

    url = oauth_client.make_cli_poll_url(device_code)
    headers = {"Accept": "application/json"}

    max_attempts = math.ceil(expires_in / interval)
    attempt = 0
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
    github_user = httpclient.fetch_github_credentials(
        gh_oauth_tok.token_type, gh_oauth_tok.access_token
    )
    if github_user == None:
        return fastapi.Response(
            content="Access token expired.", status_code=403, media_type="text/plain"
        )

    # create an evault access token, then cache it
    evault_access_token = secrets.token_urlsafe(32)
    key = f"evault-access-token:{evault_access_token}"
    redis.hset(
        name=key,
        mapping={
            "user-id": github_user.id,
            "github-access-token": gh_oauth_tok.access_token,
            "github-access-token-type": gh_oauth_tok.token_type,
        },
    )
    redis.expire(key, EVAULT_SESSION_TOK_EXP)

    # build response
    body = json.dumps(
        {
            "user-login": github_user.login,
            "evault-access-token": evault_access_token,
        }
    )

    res = fastapi.Response(content=body, media_type="application/json")
    res.set_cookie(
        key="evault_access_token",
        value=evault_access_token,
        expires=EVAULT_SESSION_TOK_EXP,
    )
    res.set_cookie(
        key="device_type",
        value="cli",
        expires=EVAULT_SESSION_TOK_EXP,
    )
    return res


@app.get("/api/auth/check")
def auth_check(token: str, device_type: DeviceType):
    key = f"evault-access-token:{token}"
    tok = redis.hgetall(key)
    print(tok)

    if tok == {}:  # instead of reporting a not found, it returns `{}`
        return fastapi.Response(
            content="Access token expired.", status_code=403, media_type="text/plain"
        )

    access_token = tok.get(b"github-access-token").decode()
    token_type = tok.get(b"github-access-token-type").decode()

    # get user information
    github_user = httpclient.fetch_github_credentials(token_type, access_token)
    if github_user == None:
        return fastapi.Response(
            content="Access token expired.", status_code=403, media_type="text/plain"
        )

    body = json.dumps(
        {
            "user-login": github_user.login,
            "evault-access-token": token,
        }
    )

    res = fastapi.Response(content=body, media_type="application/json")
    res.set_cookie(
        key="evault_access_token",
        value=key,
        expires=EVAULT_SESSION_TOK_EXP,
    )
    res.set_cookie(
        key="device_type",
        value=device_type,
        expires=EVAULT_SESSION_TOK_EXP,
    )

    # extend session
    redis.expire(key, EVAULT_SESSION_TOK_EXP)
    return res
