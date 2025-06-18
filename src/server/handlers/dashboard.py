from dataclasses import asdict
from fastapi.responses import JSONResponse
from evault.src.server.config import redis, httpclient, db
from evault.src.server.validators import valid_user_repo_string
from evault.src.server.middlewares.auth import access_token_extractor
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from argon2.profiles import RFC_9106_LOW_MEMORY
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from argon2 import PasswordHasher
import secrets


router = APIRouter(
    prefix="/api/github/dashboard", dependencies=[Depends(access_token_extractor)]
)


@router.get("/repositories")
def get_user_repositories(evault_access_token: str = Depends(access_token_extractor)):
    user = redis.get_user_session(evault_access_token)
    assert user != None

    repos = httpclient.fetch_user_repositories(
        user.gh_token.token_type,
        user.gh_token.access_token,
    )

    body = [asdict(r) for r in repos]
    headers = {
        "Cache-Control": "max-age=120",
    }

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=body,
        headers=headers,
    )


@router.get("/repository/{repo_id}")
def get_repository(
    repo_id: int, repo: str, evault_access_token: str = Depends(access_token_extractor)
):
    if not valid_user_repo_string(repo):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid repository format."
        )

    db_repo = db.get_repository(repo_id)

    # if repo is provided, we need to check for ownership
    if repo != None and db_repo is None:
        [owner, repo_name] = repo.split("/")

        d = redis.get_user_session(evault_access_token)
        assert d != None

        remote_repository = httpclient.fetch_repository(
            d.gh_token.token_type,
            d.gh_token.access_token,
            owner,
            repo_name,
        )

        if d.user.id != remote_repository.owner.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not repository owner."
            )

    # if the code reaches here, user is owner
    if db_repo is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Repository not found."
        )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=jsonable_encoder(db_repo),
    )


@router.post("/repository/new")
def create_new_repository(
    repo_id: int,
    password: str,
    repo_fullname: str,
    evault_access_token: str = Depends(access_token_extractor),
):
    if not valid_user_repo_string(repo_fullname):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid repository format."
        )

    [owner, repo_name] = repo_fullname.split("/")

    d = redis.get_user_session(evault_access_token)
    assert d != None

    repository = httpclient.fetch_repository(
        d.gh_token.token_type,
        d.gh_token.access_token,
        owner,
        repo_name,
    )

    if d.user.id != repository.owner.id:
        raise HTTPException(status_code=403, detail="Not repository owner.")

    digest = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY).hash(
        password,
        salt=secrets.token_bytes(32),
    )

    db.create_new_repository(
        repo_id, repository.owner.id, digest, repository.full_name, None
    )
    return Response(status_code=HTTP_201_CREATED)
