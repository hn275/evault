from typing import Optional, Tuple
import redis as redispy
from shared.types import GithubAuthToken, GitHubUser
from fastapi import HTTPException


class Database:
    def __init__(self) -> None:
        pass

    def save_credentials(self, access_token: str):
        pass


class Redis(redispy.Redis):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)

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
    ) -> Optional[Tuple[GitHubUser, GithubAuthToken]]:
        key = self._make_session_key(evault_access_token)
        d = self.hgetall(name=key)
        if d == {}:
            return None

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
            raise HTTPException(status_code=403, detail="Session expired.")

        self.expire(key, ttl)

    def cache_token_poll(self, session_id: str, evault_access_token: str, ttl: int):
        key = f"evault-token-poll:{session_id}"
        self.set(name=key, value=evault_access_token, ex=ttl)

    def get_token_poll(self, session_id: str) -> Optional[str]:
        t = self.getdel(f"evault-token-poll:{session_id}")
        if t:
            return t.decode()

        return None

    def _make_session_key(self, session_id: str) -> str:
        return f"evault-session:{session_id}"
