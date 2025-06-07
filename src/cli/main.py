import time
from urllib.parse import urlencode
import json
import requests
import argparse
from repository import parse_remotes
from shared.types import AuthToken, AuthData, GitHubUser


SERVER = "http://127.0.0.1:8000"

# ARG PARSER
ALLOW_COMMANDS = ["push", "pull", "check"]
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=ALLOW_COMMANDS)


def get_access_token() -> GitHubUser:
    r = requests.get(f"{SERVER}/api/auth?device_type=cli")
    print(r.headers)
    assert r.status_code == 200

    authURL = r.content.decode()
    print(f"received url: {authURL}")

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

    # get user information from server
    r = requests.get(f"{SERVER}/api/auth/user?{urlencode(auth_content.__dict__)}")
    assert r.status_code == 200

    d = r.json()

    return GitHubUser(
        id=d["id"],
        name=d["name"],
        login=d["login"],
        type=d["type"],
    )


if __name__ == "__main__":
    args = parser.parse_args()
    cmd = args.command.lower()

    # Authentication
    access_token = get_access_token()
    print(access_token)

    try:
        repos = parse_remotes()
        print(repos)
    except IOError as e:
        print(f"Failed to validate remote repositories: {e}")
        exit(1)
