from dataclasses import asdict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.server.middlewares.auth import access_token_extractor
from src.server import cache
from starlette.status import HTTP_200_OK

router = APIRouter(
    prefix="/api/github/user",
    dependencies=[Depends(access_token_extractor)],
)


@router.get("")
def get_user_information(
    evault_access_token: str | None = Depends(access_token_extractor),
):
    d = cache.get_user_session(evault_access_token)
    return JSONResponse(status_code=HTTP_200_OK, content=asdict(d.user))
