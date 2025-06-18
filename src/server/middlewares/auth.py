from fastapi import Cookie, HTTPException
from evault.src.server.config import redis, EVAULT_SESSION_TOKEN_TTL


def access_token_extractor(evault_access_token: str | None = Cookie(None)) -> str:
    if evault_access_token == None:
        raise HTTPException(
            status_code=403,
            detail="Access token not found/expired.",
        )

    # extend the session
    redis.renew_user_session(
        evault_access_token,
        EVAULT_SESSION_TOKEN_TTL,
    )

    return evault_access_token
