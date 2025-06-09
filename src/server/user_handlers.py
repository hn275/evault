from dataclasses import asdict
import json
from .config import *
from shared.types import Cookie
from typing import Optional
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi import Response


def auth_middleware(evault_access_token: Optional[str] = Cookie(None)) -> str:
    if evault_access_token == None:
        raise HTTPException(status_code=403, detail="Access token not found/expired.")
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
    return Response(
        status_code=200,
        media_type="application/json; charset=utf-8",
        content=json.dumps([asdict(repo) for repo in repos]),
    )


app.include_router(dashboard_router)
