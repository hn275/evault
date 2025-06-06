import time
from urllib.parse import urlencode
import json
import requests
import argparse
from repository import parse_remotes
from shared.types import AuthToken, AuthData


SERVER = "http://127.0.0.1:8000"
AUTH_MAX_RETRY_ATTEMPT = 10

# ARG PARSER
ALLOW_COMMANDS = ["push", "pull", "check"]
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=ALLOW_COMMANDS)


def get_access_token() -> AuthToken:
    r = requests.get(f"{SERVER}/api/auth?device_type=cli")
    assert r.status_code == 200

    data = r.json()
    client_id, authURL = data["client-id"], data["auth-url"]

    r = requests.post(authURL, headers={"Accept": "application/json"})
    assert r.status_code == 200

    data = r.json()
    auth_content = AuthData(
        device_code=data["device_code"],
        user_code=data["user_code"],
        verification_uri=data["verification_uri"],
        expires_in=data["expires_in"],
        interval=data["interval"],
    )

    print(
        f"To authenticate, go to https://github.com/login/device and enter the code {auth_content.user_code}"
    )

    # polls github for access token
    p = {
        "client_id": client_id,
        "device_code": auth_content.device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    headers = {"Accept": "application/json"}

    url = f"https://github.com/login/oauth/access_token?{urlencode(p)}"

    # TODO: change this to time based instead of retry based (somehow)
    # can leverage the math MAX_TIME / interval?
    attempt = 0
    while True:
        assert attempt <= AUTH_MAX_RETRY_ATTEMPT
        attempt += 1

        r = requests.post(url, headers=headers)

        assert r.status_code == 200
        data = r.json()

        if "error" in data:
            if data["error"] == "authorization_pending":
                time.sleep(auth_content.interval)
                continue
            else:
                raise Exception(data["error_description"])

        return AuthToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            scope=data["scope"],
        )


if __name__ == "__main__":
    args = parser.parse_args()
    cmd = args.command.lower()
    cred_file = open("evault-credentials.json", "w")

    # Authentication
    access_token = get_access_token()
    r = requests.get(f"{SERVER}/api/auth/user?{urlencode(access_token.__dict__)}")
    assert r.status_code == 200

    credentials = {
        "user": r.json(),
        "token": access_token.__dict__,
    }
    d = json.dumps(credentials)
    cred_file.write(d)

    try:
        repos = parse_remotes()
        print(repos)
    except IOError as e:
        print(f"Failed to validate remote repositories: {e}")
        exit(1)
