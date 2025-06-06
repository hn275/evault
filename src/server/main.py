import json
import requests
from urllib.parse import urlencode
from typing import Literal
import fastapi
import os

from requests import request
from shared.types import AuthToken, GitHubUser


app = fastapi.FastAPI()
GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]


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
        url = f"https://github.com/login/device/code?{urlencode(params)}"
        return {"client-id": GITHUB_OAUTH_CLIENT_ID, "auth-url": url}


@app.get("/api/auth/user")
def auth_github(token_type: str, access_token: str):
    url = f"https://api.github.com/user"
    headers = {
        "Authorization": f"{token_type} {access_token}",
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
