import json
import secrets
import urllib.parse as urlparse
import fastapi
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import (
    PlainTextResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_302_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from src.server.config import EVAULT_WEB_URL
from src.server.config import EVAULT_TOKEN_POLL_TTL
from src.server.config import GITHUB_OAUTH_STATE_TTL
from src.server.config import EVAULT_SESSION_TOKEN_TTL
from src.server.config import EVAULT_TOKEN_POLL_MAX_ATTEMPT
from src.server import cache, database as db
from src.server.github import oauth as gh_oauth, client as gh_client
from src.pkg.types import DeviceType, UserSession

router = APIRouter(prefix="/api/github/auth", dependencies=[])


@router.get("/")
async def auth(device_type: DeviceType):
    oauth_state = secrets.token_urlsafe(32)
    session_id = secrets.token_urlsafe(16)
    oauth_login_url = gh_oauth.make_login_url(
        oauth_state,
        session_id,
        device_type,
    )

    cache.cache_auth_url(session_id, oauth_login_url, GITHUB_OAUTH_STATE_TTL)
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
    oauth_login_url = cache.get_auth_url(session_id)
    oauth_login_url = oauth_login_url.decode()
    cache.renew_auth_url(session_id, GITHUB_OAUTH_STATE_TTL)

    return PlainTextResponse(content=oauth_login_url)


@router.get("/token")
def auth_token(
    session_id: str,
    code: str,
    state: str,
    device_type: DeviceType,
):
    oauth_login_url = cache.get_auth_url(session_id)
    cache.remove_auth_url(session_id)
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
    gh_token = gh_client.fetch_user_auth_token(code)

    # get user information
    gh_user, user_email = gh_client.fetch_github_credentials(gh_token)

    # store a (new) session: github user to cache
    # create an evault access token, then cache it
    evault_access_token = secrets.token_urlsafe(32)

    user_session = UserSession(device_type, gh_user, gh_token)
    cache.create_user_session(
        evault_access_token, user_session, EVAULT_SESSION_TOKEN_TTL
    )

    db.create_or_update_user(
        user_id=gh_user.id,
        login=gh_user.login,
        name=gh_user.name,
        email=user_email,
    )

    response = fastapi.Response(status_code=HTTP_200_OK)
    if device_type == "web":
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOKEN_TTL,
        )
    else:
        cache.cache_token_poll(
            session_id,
            evault_access_token,
            EVAULT_TOKEN_POLL_TTL,
        )

    return response


@router.get("/poll")
async def auth_poll(session_id: str, req: fastapi.Request):
    access_token: str | None = cache.get_token_poll(session_id)

    if access_token is not None:
        return JSONResponse(
            status_code=HTTP_200_OK,
            content={"status": "ok", "access_token": access_token},
        )

    attempt = req.cookies.get("evault_poll_attempt", "0")
    attempt = int(attempt)

    if attempt >= EVAULT_TOKEN_POLL_MAX_ATTEMPT:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"status": "abort", "error": "Max attempt exceeded."},
        )

    response = JSONResponse(
        status_code=HTTP_200_OK,
        content=json.dumps({"status": "pending"}),
    )
    response.set_cookie("evault_poll_attempt", f"{attempt + 1}")
    return response


@router.get("/refresh")
def auth_refresh(
    access_token: str,
    device_type: DeviceType,
    request: Request,
):
    """
    for device_type=web, the access_token should be an empty string
    """
    cache.renew_user_session(access_token, EVAULT_SESSION_TOKEN_TTL)

    if device_type == "cli":
        return fastapi.Response(status_code=HTTP_200_OK)

    evault_access_token = request.cookies.get("evault_access_token")
    assert evault_access_token

    response = Response(status_code=HTTP_200_OK)
    response.set_cookie(
        key="evault_access_token",
        value=evault_access_token,
        expires=EVAULT_SESSION_TOKEN_TTL,
    )
    return response
