from dataclasses import asdict
from .config import *
from ..pkg.types import Cookie
from typing import Optional
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse


def auth_middleware(evault_access_token: Optional[str] = Cookie(None)) -> str:
    if evault_access_token == None:
        raise HTTPException(status_code=403, detail="Access token not found/expired.")

    # extend the session
    redis.renew_user_session(evault_access_token, EVAULT_SESSION_TOKEN_TTL)

    return evault_access_token


dashboard_router = APIRouter(
    prefix="/api/dashboard", dependencies=[Depends(auth_middleware)]
)


@dashboard_router.get("/user")
def get_user_information(evault_access_token: str = Depends(auth_middleware)):
    d = redis.get_user_session(evault_access_token)
    assert d != None
    (user, _) = d
    return JSONResponse(
        content=user.__dict__,
    )


@dashboard_router.get("/repositories")
def get_user_repositories(evault_access_token: str = Depends(auth_middleware)):
    d = redis.get_user_session(evault_access_token)
    assert d != None

    (_, token) = d
    repos = httpclient.fetch_user_repositories(token.token_type, token.access_token)

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


app.include_router(dashboard_router)
