from urllib.parse import urlencode
from src.pkg.types import DeviceType
from src.server.config import (
    GITHUB_OAUTH_CLIENT_ID,
    GITHUB_OAUTH_CLIENT_SECRET,
    GITHUB_OAUTH_REDIRECT_URI,
)


def make_login_url(
    oauth_state: str,
    session_id: str,
    device_type: DeviceType,
) -> str:
    p = {
        "session_id": session_id,
        "device_type": device_type,
    }
    redirect_url = f"{GITHUB_OAUTH_REDIRECT_URI}?{urlencode(p)}"

    p = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "redirect_uri": redirect_url,
        "state": oauth_state,
        "scope": "repo read:user",
    }

    return f"https://github.com/login/oauth/authorize?{urlencode(p)}"


def make_cli_login_url() -> str:
    p = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
    }
    return f"https://github.com/login/device/code?{urlencode(p)}"


def make_cli_poll_url(device_code: str) -> str:
    p = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    return f"https://github.com/login/oauth/access_token?{urlencode(p)}"


def make_web_access_tok_url(code: str) -> str:
    p = {
        "client_id": GITHUB_OAUTH_CLIENT_ID,
        "client_secret": GITHUB_OAUTH_CLIENT_SECRET,
        "code": code,
    }
    return f"https://github.com/login/oauth/access_token?{urlencode(p)}"
