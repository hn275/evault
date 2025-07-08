from dataclasses import asdict
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from ..github import client as httpclient
from .. import cache
from .. import database as db
from ..validators import valid_user_repo_string
from ..middlewares.auth import access_token_extractor
from ..crypto import passwordhash


router = APIRouter(
    prefix="/api/github/dashboard",
    dependencies=[
        Depends(access_token_extractor),
    ],
)


@router.get("/repositories")
def get_user_repositories(
    evault_access_token: str = Depends(access_token_extractor),
):
    user = cache.get_user_session(evault_access_token)
    repos = httpclient.fetch_user_repositories(
        user.gh_token.token_type,
        user.gh_token.access_token,
    )

    body = [asdict(r) for r in repos]
    headers = {
        "Cache-Control": "max-age=120",
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=body,
        headers=headers,
    )


@router.get("/repository/{repo_id}")
def get_repository(
    repo_id: int,
    repo: str,
    evault_access_token: str = Depends(access_token_extractor),
):
    if not valid_user_repo_string(repo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repository format.",
        )

    db_repo = db.get_repository(repo_id)

    # if repo is provided, we need to check for ownership
    if db_repo is None:
        [owner, repo_name] = repo.split("/")

        user_session = cache.get_user_session(evault_access_token)

        remote_repository = httpclient.fetch_repository(
            user_session.gh_token.token_type,
            user_session.gh_token.access_token,
            owner,
            repo_name,
        )

        if user_session.user.id != remote_repository.owner.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not repository owner.",
            )

    # if the code reaches here, user is owner
    if db_repo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found.",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(db_repo),
    )


@router.post("/repository/new")
def create_new_repository(
    repo_id: int,
    password: str,
    repo_fullname: str,
    evault_access_token: str = Depends(access_token_extractor),
):
    # TODO: sanitize password
    if not valid_user_repo_string(repo_fullname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid repository format.",
        )

    [owner, repo_name] = repo_fullname.split("/")

    d = cache.get_user_session(evault_access_token)

    repository = httpclient.fetch_repository(
        d.gh_token.token_type,
        d.gh_token.access_token,
        owner,
        repo_name,
    )

    if d.user.id != repository.owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not repository owner.",
        )

    if repo_fullname != repository.full_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid repository.",
        )

    digest = passwordhash.hash(password)
    db.create_new_repository(
        repo_id=repo_id,
        owner_id=repository.owner.id,
        repo_password=digest,
        name=repository.full_name,
        bucket_addr=None,
    )
    return Response(status_code=status.HTTP_201_CREATED)
