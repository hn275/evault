from fastapi import Cookie, HTTPException, status
from evault.src.server.config import EVAULT_SESSION_TOKEN_TTL
from src.server import cache


def access_token_extractor(
    evault_access_token: str | None = Cookie(None),
) -> str:
    if evault_access_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access token not found/expired.",
        )

    # extend the session
    cache.renew_user_session(
        evault_access_token,
        EVAULT_SESSION_TOKEN_TTL,
    )

    return evault_access_token
