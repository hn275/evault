import secrets, fastapi, urllib.parse as urlparse, json
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse
from fastapi import status
from starlette.status import HTTP_200_OK
from ..pkg.types import DeviceType, GithubAuthToken
from .config import (
    db,
    app,
    redis,
    httpclient,
    oauth_client,
    EVAULT_WEB_URL,
    EVAULT_TOKEN_POLL_TTL,
    GITHUB_OAUTH_STATE_TTL,
    EVAULT_SESSION_TOKEN_TTL,
    EVAULT_TOKEN_POLL_MAX_ATTEMPT,
)
from ..pkg.types import UserSession


@app.get("/api/auth")
async def auth(device_type: DeviceType):
    oauth_state = secrets.token_urlsafe(32)
    session_id = secrets.token_urlsafe(16)
    oauth_login_url = oauth_client.make_login_url(oauth_state, session_id, device_type)

    redis.cache_auth_url(session_id, oauth_login_url, GITHUB_OAUTH_STATE_TTL)
    if device_type == "web":
        return RedirectResponse(url=oauth_login_url, status_code=status.HTTP_302_FOUND)

    return fastapi.Response(
        content=f"{EVAULT_WEB_URL}/auth?{urlparse.urlencode({"session_id": session_id})}",
        media_type="text/plain",
    )


@app.get("/api/auth/url")
def auth_url(session_id: str):
    oauth_login_url = redis.get_auth_url(session_id)
    if oauth_login_url == None:
        return PlainTextResponse(status_code=401, content="Login link expired.")

    oauth_login_url = oauth_login_url.decode()
    redis.renew_auth_url(session_id, GITHUB_OAUTH_STATE_TTL)

    return PlainTextResponse(content=oauth_login_url)


@app.get("/api/auth/token")
def auth_token(session_id: str, code: str, state: str, device_type: DeviceType):
    oauth_login_url = redis.get_auth_url(session_id)
    redis.remove_auth_url(session_id)
    params = urlparse.parse_qs(urlparse.urlparse(oauth_login_url).query)

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

    gh_token = GithubAuthToken(**r.json())

    # get user information
    gh_user = httpclient.fetch_github_credentials(
        gh_token.token_type, gh_token.access_token
    )
    if gh_user == None:
        return PlainTextResponse(content="Failed to fetch user data.", status_code=401)

    # store a (new) session: github user to cache
    # create an evault access token, then cache it
    evault_access_token = secrets.token_urlsafe(32)
    user_session = UserSession(device_type, gh_user, gh_token)
    redis.create_user_session(
        evault_access_token, user_session, EVAULT_SESSION_TOKEN_TTL
    )
    # check if user exists in database
    gh_user.email = "N/A" if gh_user.email == None else gh_user.email
    user = db.get_user(gh_user.id)
    if user == None:
        # create new user
        db.create_new_user(gh_user.id, gh_user.login, gh_user.name, gh_user.email)

    response = fastapi.Response(status_code=HTTP_200_OK)
    if device_type == "web":
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOKEN_TTL,
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


@app.get("/api/auth/refresh")
def auth_refresh(access_token: str, device_type: DeviceType, request: fastapi.Request):
    """
    for device_type=web, the access_token should be an empty string
    """
    redis.renew_user_session(access_token, EVAULT_SESSION_TOKEN_TTL)

    if device_type == "cli":
        return fastapi.Response(status_code=200)

    else:
        evault_access_token = request.cookies.get("evault_access_token")
        assert evault_access_token

        response = fastapi.Response(status_code=200)
        response.set_cookie(
            key="evault_access_token",
            value=evault_access_token,
            expires=EVAULT_SESSION_TOKEN_TTL,
        )
        return response
