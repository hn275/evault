from typing import Literal, Optional, Tuple, Dict
import redis as redispy
from ..pkg.types import GithubAuthToken, GitHubUser
from fastapi import HTTPException
import sqlalchemy as sql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import Repository


type SSLMode = Literal["require", "disable"]


class Database:
    engine: sql.Engine

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        db: str,
        port: int = 5432,
        ssl: SSLMode = "require",
    ) -> None:
        conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}?sslmode={ssl}"
        self.engine = sql.create_engine(conn_str, echo=True)
        print("Connected to database")

    def get_repository(self, repo_id: int) -> Optional[Repository]:
        with Session(self.engine) as s:
            return s.get(Repository, repo_id)

    def create_new_repository(self, repo_id: int, owner_id: int, digest: str):
        repo = Repository(id=repo_id, owner_id=owner_id, password=digest)

        with Session(self.engine) as s:
            try:
                s.add(repo)
                s.commit()
                s.refresh(repo)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Repository exists.",
                )


class Redis(redispy.Redis):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self.ping()
        print("Connected to redis")

    def create_user_session(
        self,
        evault_access_token: str,
        gh_token: GithubAuthToken,
        gh_user: GitHubUser,
        ttl: int,
    ):
        key = self._make_session_key(evault_access_token)
        self.hset(
            name=key,
            mapping={
                "user-id": gh_user.id,
                "user-name": gh_user.name,
                "user-login": gh_user.login,
                "user-email": gh_user.email,
                "user-type": gh_user.type,
                "user-avatar_url": gh_user.avatar_url,
                "github-access-token": gh_token.access_token,
                "github-access-token-type": gh_token.token_type,
                "github-access-token-scope": gh_token.scope,
            },
        )
        self.expire(key, ttl)

    def get_user_session(
        self, evault_access_token: str
    ) -> Tuple[GitHubUser, GithubAuthToken]:
        key = self._make_session_key(evault_access_token)
        d = self.hgetall(name=key)
        d: Dict[bytes, bytes] = d
        if d == {}:
            raise HTTPException(status_code=440, detail="Session expired.")

        gh_user = GitHubUser(
            id=int(d.get(b"user-id").decode()),
            name=d.get(b"user-name").decode(),
            login=d.get(b"user-login").decode(),
            email=d.get(b"user-email").decode(),
            type=d.get(b"user-type").decode(),
            avatar_url=d.get(b"user-avatar_url").decode(),
        )
        gh_token = GithubAuthToken(
            access_token=d.get(b"github-access-token").decode(),
            token_type=d.get(b"github-access-token-type").decode(),
            scope=d.get(b"github-access-token-scope").decode(),
        )

        return (gh_user, gh_token)

    def renew_user_session(self, evault_access_token: str, ttl: int):
        key = self._make_session_key(evault_access_token)
        ctr = self.exists(key)
        if ctr == 0:
            raise HTTPException(status_code=440, detail="Session expired.")

        self.expire(key, ttl)

    def cache_token_poll(
        self,
        session_id: str,
        evault_access_token: str,
        ttl: int,
    ):
        key = f"evault-token-poll:{session_id}"
        self.set(name=key, value=evault_access_token, ex=ttl)

    def get_token_poll(self, session_id: str) -> Optional[str]:
        t = self.getdel(f"evault-token-poll:{session_id}")
        if t:
            return t.decode()

        raise HTTPException(status_code=404)

    def cache_auth_url(self, session_id: str, auth_url: str, ttl: int):
        key = self._make_auth_url_key(session_id)
        self.set(name=key, value=auth_url, ex=ttl)

    def get_auth_url(self, session_id: str) -> str:
        key = self._make_auth_url_key(session_id)
        t = self.get(key)
        if not t:
            raise HTTPException(status_code=401)

        return t.decode()

    def renew_auth_url(self, session_id: str, ttl: int):
        key = self._make_auth_url_key(session_id)
        a = self.expire(key, ttl)
        print(f"renew auth: {a}")

    def remove_auth_url(self, session_id: str):
        key = self._make_auth_url_key(session_id)
        url_removed = self.delete(key)
        if url_removed != 1:
            raise HTTPException(status_code=401)

    def _make_session_key(self, session_id: str) -> str:
        return f"evault-session:{session_id}"

    def _make_auth_url_key(self, session_id: str) -> str:
        return f"evault-auth:{session_id}"
