from redis import Redis
from loguru import logger
from fastapi import HTTPException, status
from .config import REDIS_HOST, REDIS_PORT_DEFAULT
from .types import UserSession


_redis = Redis(REDIS_HOST, port=REDIS_PORT_DEFAULT, decode_responses=True)

_redis.ping()
logger.info("Connected to redis")


def create_user_session(
    evault_access_token: str,
    user_session: UserSession,
    ttl: int,
):
    key = _make_session_key(evault_access_token)
    data = user_session.make_flat_map()
    _redis.hset(name=key, mapping=data)
    _redis.expire(key, ttl)


def get_user_session(evault_access_token: str) -> UserSession:
    key = _make_session_key(evault_access_token)
    d = _redis.hgetall(name=key)
    if d == {}:
        raise HTTPException(status_code=440, detail="Session expired.")

    m = {}
    for key, val in d.items():
        m[key] = val

    m["user.id"] = int(m["user.id"])
    return UserSession.from_flat_map(m)


def renew_user_session(evault_access_token: str, ttl: int):
    key = _make_session_key(evault_access_token)
    ctr = _redis.exists(key)
    if ctr == 0:
        raise HTTPException(status_code=440, detail="Session expired.")

    _redis.expire(key, ttl)


def cache_token_poll(session_id: str, evault_access_token: str, ttl: int):
    key = f"evault-token-poll:{session_id}"
    _redis.set(name=key, value=evault_access_token, ex=ttl)


def get_token_poll(session_id: str) -> str | None:
    t = _redis.getdel(f"evault-token-poll:{session_id}")
    if t:
        return t

    return None


def cache_auth_url(session_id: str, auth_url: str, ttl: int):
    key = _make_auth_url_key(session_id)
    _redis.set(name=key, value=auth_url, ex=ttl)


def get_auth_url(session_id: str) -> str:
    key = _make_auth_url_key(session_id)
    t = _redis.get(key)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login link expired.",
        )

    return t.decode()


def renew_auth_url(session_id: str, ttl: int):
    key = _make_auth_url_key(session_id)
    a = _redis.expire(key, ttl)
    print(f"renew auth: {a}")


def remove_auth_url(session_id: str):
    key = _make_auth_url_key(session_id)
    url_removed = _redis.delete(key)
    if url_removed != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def _make_session_key(session_id: str) -> str:
    return f"evault-session:{session_id}"


def _make_auth_url_key(session_id: str) -> str:
    return f"evault-auth:{session_id}"
