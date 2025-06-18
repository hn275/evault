from dataclasses import asdict
from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse
from evault.src.server.config import redis
from evault.src.server.middlewares.auth import access_token_extractor
from starlette.status import HTTP_200_OK

router = APIRouter(
    prefix="/api/github/user",
    dependencies=[Depends(access_token_extractor)],
)


@router.get("")
def get_user_information(
    evault_access_token: str | None = Depends(access_token_extractor),
):
    d = redis.get_user_session(evault_access_token)
    return JSONResponse(status_code=HTTP_200_OK, content=asdict(d.user))
