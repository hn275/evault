from dataclasses import asdict
from .config import db, app, redis, EVAULT_SESSION_TOKEN_TTL, httpclient
from typing import Optional
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse, Response
from argon2.profiles import RFC_9106_LOW_MEMORY
from argon2 import PasswordHasher
import secrets


def auth_middleware(evault_access_token: Optional[str] = Cookie(None)) -> str:
    if evault_access_token == None:
        raise HTTPException(
            status_code=403,
            detail="Access token not found/expired.",
        )

    # extend the session
    redis.renew_user_session(
        evault_access_token,
        EVAULT_SESSION_TOKEN_TTL,
    )

    return evault_access_token


dashboard_router = APIRouter(
    prefix="/api/dashboard", dependencies=[Depends(auth_middleware)]
)


@dashboard_router.get("/user")
def get_user_information(evault_access_token: str = Depends(auth_middleware)):
    d = redis.get_user_session(evault_access_token)
    assert d != None
    return JSONResponse(content=asdict(d.user))


@dashboard_router.get("/repositories")
def get_user_repositories(evault_access_token: str = Depends(auth_middleware)):
    user = redis.get_user_session(evault_access_token)
    assert user != None

    repos = httpclient.fetch_user_repositories(
        user.token.token_type,
        user.token.access_token,
    )

    body = [asdict(r) for r in repos]
    headers = {
        "Cache-Control": "max-age=120",
    }

    return JSONResponse(
        status_code=200,
        content=body,
        headers=headers,
    )


@dashboard_router.get("/repository/{repo_id}")
def get_repository(repo_id: int):
    repo = db.get_repository(repo_id)
    if repo == None:
        raise HTTPException(status_code=404)

    return "OK"


@dashboard_router.post("/repository/new")
def create_new_repository(
    repo_id: int,
    password: str,
    repo_fullname: str,
    evault_access_token: str = Depends(auth_middleware),
):
    # TODO: sanitize repo_fullname
    [owner, repo_name] = repo_fullname.split("/")

    d = redis.get_user_session(evault_access_token)
    assert d != None

    repository = httpclient.fetch_repository(
        d.token.token_type,
        d.token.access_token,
        owner,
        repo_name,
    )

    if d.user.id != repository.owner.id:
        raise HTTPException(status_code=403, detail="Not repository owner.")

    digest = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY).hash(
        password,
        salt=secrets.token_bytes(32),
    )

    db.create_new_repository(repo_id, repository.owner.id, digest)
    return Response(status_code=201)


app.include_router(dashboard_router)
