import json, os, secrets
from urllib.parse import urlencode, parse_qs, urlparse
from typing import Literal
import fastapi
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from shared.types import Cookie, GithubAuthToken, DeviceType
from shared.utils import env_or_default
from .storage import Redis
from .httpreqs import HttpClient
from .oauth import GitHubOauth, GitHubClient


GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
GITHUB_OAUTH_REDIRECT_URI = env_or_default(
    "GITHUB_OAUTH_REDIRECT_URI", "http://localhost:5173/auth/github"
)
GITHUB_OAUTH_STATE_TTL = 120  # 2 minutes

EVAULT_SESSION_TOK_EXP = 300  # 5 minutes
EVAULT_WEB_URL = env_or_default("EVAULT_WEB_URL", "http://localhost:5173")
EVAULT_TOKEN_POLL_TTL = 30
EVAULT_TOKEN_POLL_MAX_ATTEMPT = 10

REDIS_HOST = env_or_default("REDIS_HOST", "localhost")
REDIS_PORT_DEFAULT = 6379

redis = Redis(REDIS_HOST, port=REDIS_PORT_DEFAULT)
redis.ping()

app = fastapi.FastAPI()
app.add_middleware(
    # TODO: configure this for prod
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


httpclient = HttpClient()


oauth_client = GitHubOauth(
    client_id=GITHUB_OAUTH_CLIENT_ID,
    client_secret=GITHUB_OAUTH_CLIENT_SECRET,
    redirect_uri=GITHUB_OAUTH_REDIRECT_URI,
)


@app.get("/api/auth")
async def auth(device_type: DeviceType):
    oauth_state = secrets.token_urlsafe(32)
    session_id = secrets.token_urlsafe(16)
    oauth_login_url = oauth_client.make_web_login_url(
        oauth_state, session_id, device_type
    )
    redis.set(
        f"evault-login-url:{session_id}", oauth_login_url, ex=GITHUB_OAUTH_STATE_TTL
    )
    return fastapi.Response(
        content=f"{EVAULT_WEB_URL}/auth?{urlencode({"session_id": session_id})}",
        media_type="text/plain",
    )


@app.get("/api/auth/url")
def auth_url(session_id: str):
    oauth_login_url = redis.get(f"evault-login-url:{session_id}")
    if oauth_login_url == None:
        return PlainTextResponse(status_code=401, content="Login link expired.")

    oauth_login_url = oauth_login_url.decode()
    redis.expire(f"evault-login-url:{session_id}", GITHUB_OAUTH_STATE_TTL)

    return PlainTextResponse(content=oauth_login_url)


@app.get("/api/auth/token")
def auth_token(session_id: str, code: str, state: str, device_type: DeviceType):
    oauth_login_url = redis.getdel(f"evault-login-url:{session_id}")
    if oauth_login_url == None:
        return PlainTextResponse(
            status_code=401,
            content="Login link expired.",
        )

    oauth_login_url = oauth_login_url.decode()
    params = parse_qs(urlparse(oauth_login_url).query)

    # verify state
    session_state = params.get("state")
    assert session_state
    session_state = session_state[0]
    if session_state != state:
        return PlainTextResponse(content="Invalid authentication", status_code=401)

    # get access token from github
    auth_url = oauth_client.make_web_access_tok_url(code)
    r = httpclient.post(auth_url, headers={"Accept": "application/json; charset=utf-8"})
    assert r.status_code == 200

    d = r.json()
    gh_token = GithubAuthToken(d["access_token"], d["token_type"], d["scope"])

    # get user information
    cx = GitHubClient(gh_token.access_token, gh_token.token_type)
    gh_user = cx.get_user()
    if gh_user == None:
        return PlainTextResponse(content="Failed to fetch user data.", status_code=401)

    # TODO: store user in database?
    # store a (new) session: github user to cache
    # create an evault access token, then cache it
    evault_access_token = secrets.token_urlsafe(32)
    redis.cache_user(evault_access_token, gh_token, gh_user, EVAULT_SESSION_TOK_EXP)

    response = fastapi.Response(status_code=200)
    if device_type == "web":
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOK_EXP,
        )
    else:
        redis.cache_token_poll(session_id, evault_access_token, EVAULT_TOKEN_POLL_TTL)

    return response


@app.get("/api/auth/poll")
async def auth_poll(session_id: str, req: fastapi.Request):
    access_token = redis.get_token_poll(session_id)

    if access_token != None:
        return JSONResponse(
            status_code=200,
            content=json.dumps({"status": "ok", "access_token": access_token}),
        )

    attempt = req.cookies.get("evault_poll_attempt", "0")
    attempt = int(attempt)

    if attempt >= EVAULT_TOKEN_POLL_MAX_ATTEMPT:
        return JSONResponse(
            status_code=403,
            content=json.dumps({"status": "abort", "error": "Max attempt exceeded."}),
        )

    else:
        response = JSONResponse(
            status_code=200,
            content=json.dumps({"status": "pending"}),
        )
        response.set_cookie("evault_poll_attempt", f"{attempt + 1}")
        return response
