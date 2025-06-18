from typing import Literal, Optional
from fastapi import HTTPException, status
import sqlalchemy as sql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from .models import Repository, User
from loguru import logger
from src.server.config import (
    PSQL_DBNAME,
    PSQL_HOST,
    PSQL_PORT,
    PSQL_USER,
    PSQL_PASSWORD,
    PSQL_SSLMODE,
    EVAULT_DEBUG,
)


type SSLMode = Literal["require", "disable"]

c = (
    f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}"
    f"@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DBNAME}"
    f"?sslmode={PSQL_SSLMODE}"
)
_engine: sql.Engine = sql.create_engine(c, echo=EVAULT_DEBUG)
logger.info("Connected to database")


def get_repository(repo_id: int) -> Repository | None:
    with Session(_engine) as s:
        return s.get(Repository, repo_id)


def create_new_repository(
    repo_id: int,
    owner_id: int,
    digest: str,
    name: str,
    bucket_addr: str | None,
):
    repo = Repository(
        id=repo_id,
        owner_id=owner_id,
        password=digest,
        name=name,
        bucket_addr=bucket_addr,
    )

    with Session(_engine) as s:
        try:
            s.add(repo)
            s.commit()
            s.refresh(repo)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Repository exists.",
            )


def create_or_update_user(
    user_id: int,
    login: str,
    name: str,
    email: str | None,
):
    stmt = (
        insert(User)
        .values(id=user_id, login=login, name=name, email=email)
        .on_conflict_do_update(
            constraint="users_pkey",
            set_=dict(login=login, name=name, email=email),
        )
        .returning(User)
    )

    with Session(_engine) as s:
        result = s.execute(stmt)
        s.commit()
        return result.scalar_one()


def get_user(user_id: int) -> User | None:
    with Session(_engine) as s:
        return s.get(User, user_id)
