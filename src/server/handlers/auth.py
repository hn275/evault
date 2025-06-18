import fastapi
import urllib.parse as urlparse
import json
import secrets
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_302_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from evault.src.server.config import (
    db,
    redis,
    httpclient,
    oauth_client,
)
from evault.src.server.config import EVAULT_WEB_URL
from evault.src.server.config import EVAULT_TOKEN_POLL_TTL
from evault.src.server.config import GITHUB_OAUTH_STATE_TTL
from evault.src.server.config import EVAULT_SESSION_TOKEN_TTL
from evault.src.server.config import EVAULT_TOKEN_POLL_MAX_ATTEMPT
from evault.src.pkg.types import DeviceType, GithubAuthToken, UserSession

router = APIRouter(prefix="/api/github/auth", dependencies=[])


@router.get("/")
async def auth(device_type: DeviceType):
    oauth_state = secrets.token_urlsafe(32)
    session_id = secrets.token_urlsafe(16)
    oauth_login_url = oauth_client.make_login_url(
        oauth_state,
        session_id,
        device_type,
    )

    redis.cache_auth_url(session_id, oauth_login_url, GITHUB_OAUTH_STATE_TTL)
    if device_type == "web":
        return RedirectResponse(
            url=oauth_login_url,
            status_code=HTTP_302_FOUND,
        )

    param = urlparse.urlencode({"session_id": session_id})
    url = f"{EVAULT_WEB_URL}/auth?{param}"
    return fastapi.Response(
        content=url,
        media_type="text/plain",
    )


@router.get("/url")
def auth_url(session_id: str):
    oauth_login_url = redis.get_auth_url(session_id)
    oauth_login_url = oauth_login_url.decode()
    redis.renew_auth_url(session_id, GITHUB_OAUTH_STATE_TTL)

    return PlainTextResponse(content=oauth_login_url)


@router.get("/token")
def auth_token(session_id: str, code: str, state: str, device_type: DeviceType):
    oauth_login_url = redis.get_auth_url(session_id)
    redis.remove_auth_url(session_id)
    params = urlparse.parse_qs(urlparse.urlparse(oauth_login_url).query)

    # verify state
    session_state = params.get("state")
    assert session_state
    session_state = session_state[0]
    if session_state != state:
        return PlainTextResponse(
            content="Invalid authentication",
            status_code=HTTP_401_UNAUTHORIZED,
        )

    # get access token from github
    auth_url = oauth_client.make_web_access_tok_url(code)
    r = httpclient.post(auth_url, headers={"Accept": "application/json; charset=utf-8"})
    assert r.status_code == HTTP_200_OK

    gh_token = GithubAuthToken(**r.json())

    # get user information
    gh_user, user_email = httpclient.fetch_github_credentials(gh_token)

    # store a (new) session: github user to cache
    # create an evault access token, then cache it
    user_session = UserSession(device_type, gh_user, gh_token)
    if device_type == "web":
        user_session.csrf_token = secrets.token_hex(32)

    evault_access_token = secrets.token_urlsafe(32)
    redis.create_user_session(
        evault_access_token, user_session, EVAULT_SESSION_TOKEN_TTL
    )

    db.create_or_update_user(
        user_id=gh_user.id, login=gh_user.login, name=gh_user.name, email=user_email
    )

    response: fastapi.Response
    if device_type == "cli":
        redis.cache_token_poll(session_id, evault_access_token, EVAULT_TOKEN_POLL_TTL)
        response = fastapi.Response(status_code=HTTP_200_OK)
    else:  # for web, set the cookie + transmit a session csrf token
        response = PlainTextResponse(
            status_code=HTTP_200_OK,
            content=user_session.csrf_token,
        )
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOKEN_TTL,
        )

    return response


@router.get("/poll")
async def auth_poll(session_id: str, req: fastapi.Request):
    access_token: str | None = redis.get_token_poll(session_id)

    if access_token is not None:
        return JSONResponse(
            status_code=HTTP_200_OK,
            content=json.dumps({"status": "ok", "access_token": access_token}),
        )

    attempt = req.cookies.get("evault_poll_attempt", "0")
    attempt = int(attempt)

    if attempt >= EVAULT_TOKEN_POLL_MAX_ATTEMPT:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content=json.dumps({"status": "abort", "error": "Max attempt exceeded."}),
        )

    else:
        response = JSONResponse(
            status_code=HTTP_200_OK,
            content=json.dumps({"status": "pending"}),
        )
        response.set_cookie("evault_poll_attempt", f"{attempt + 1}")
        return response


@router.get("/refresh")
def auth_refresh(access_token: str, device_type: DeviceType, request: fastapi.Request):
    """
    for device_type=web, the access_token should be an empty string
    """
    redis.renew_user_session(access_token, EVAULT_SESSION_TOKEN_TTL)

    if device_type == "cli":
        return fastapi.Response(status_code=HTTP_200_OK)

    else:
        evault_access_token = request.cookies.get("evault_access_token")
        assert evault_access_token

        response = fastapi.Response(status_code=HTTP_200_OK)
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOKEN_TTL,
        )
        return response
