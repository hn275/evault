import redis
from shared.utils import env_or_default


REDIS_HOST = env_or_default("REDIS_HOST", "localhost")
REDIS_PORT_DEFAULT = 6379


class Cache:
    engine: redis.Redis

    def __init__(self, redis_host: str, redis_port: int = REDIS_PORT_DEFAULT) -> None:
        self.engine = redis.Redis(host=redis_host, port=redis_port)
        self.engine.ping()

    def cache_user_token(
        self, evault_access_tok: str, github_access_tok: str, exp: int
    ) -> None:
        cache_name = f"evault_access_token:{evault_access_tok}"
        self.engine.set(name=cache_name, value=github_access_tok, ex=exp)
