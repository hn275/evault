from typing import Optional
import redis as redispy
from shared.types import GithubAuthToken, GitHubUser


class Database:
    def __init__(self) -> None:
        pass

    def save_credentials(self, access_token: str):
        pass


class Redis(redispy.Redis):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)

    def cache_user(
        self,
        evault_access_token: str,
        gh_token: GithubAuthToken,
        gh_user: GitHubUser,
        ttl: int,
    ):
        key = f"evault-access-token:{evault_access_token}"
        self.hset(
            name=key,
            mapping={
                "user-id": gh_user.id,
                "user-name": gh_user.name,
                "user-login": gh_user.login,
                "user-email": gh_user.email,
                "user-type": gh_user.type,
                "github-access-token": gh_token.access_token,
                "github-access-token-type": gh_token.token_type,
                "github-access-token-scope": gh_token.scope,
            },
        )
        self.expire(key, ttl)

    def cache_token_poll(self, session_id: str, evault_access_token: str, ttl: int):
        key = f"evault-token-poll:{session_id}"
        self.set(name=key, value=evault_access_token, ex=ttl)

    def get_token_poll(self, session_id: str) -> Optional[str]:
        t = self.getdel(f"evault-token-poll:{session_id}")
        if t:
            return t.decode()

        return None
