import json, time, requests, os
from urllib.parse import urlencode
from typing import Literal, Optional
import fastapi

from requests import request
from shared.types import AuthToken, GitHubUser


app = fastapi.FastAPI()
GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
AUTH_MAX_RETRY_ATTEMPT = 10


@app.get("/")
async def root():
    response = fastapi.Response(
        content="Hello, World!",
        status_code=200,
        media_type="text/plain",
    )

    return response


@app.get("/api/auth")
async def auth(device_type: Literal["web", "cli"]):
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


@app.get("/api/auth/user")
def auth_github(
    device_code: str,
    user_code: str,
    verification_uri: str,
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
    auth_token: Optional[AuthToken] = None
    # TODO: change this to time based instead of retry based (somehow)
    # can leverage the math MAX_TIME / interval?
    while attempt <= AUTH_MAX_RETRY_ATTEMPT:
        attempt += 1

        r = requests.post(url, headers=headers)

        assert r.status_code == 200
        data = r.json()

        if "error" in data:
            if data["error"] == "authorization_pending":
                time.sleep(interval)
                continue
            else:
                return fastapi.Response(
                    status_code=403, content=data["error_description"]
                )

        auth_token = AuthToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            scope=data["scope"],
        )
        break

    if auth_token == None:
        return fastapi.Response(
            status_code=403, content="Request for user's information timed out."
        )

    # get user information
    url = f"https://api.github.com/user"
    headers = {
        "Authorization": f"{auth_token.token_type} {auth_token.access_token}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)

    data = response.json()
    github_user = GitHubUser(
        id=data["id"],
        login=data["login"],
        name=data["name"],
        type=data["type"],
    )
    body = json.dumps(github_user.__dict__)

    response = fastapi.Response(content=body, media_type="application/json")
    response.set_cookie(key="user-id", value=f"{github_user.id}", expires=100)
    return response
