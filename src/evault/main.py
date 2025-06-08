from dataclasses import dataclass
import os
from typing import Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs
import requests, argparse, pathlib
from repository import parse_remotes
from shared.types import GithubAuthToken, AuthDataDevice, GitHubUser


CREDENTIALS_PATH = pathlib.Path("/tmp/evault/evault-access-token")
SERVER = "http://127.0.0.1:8000"

# ARG PARSER
ALLOW_COMMANDS = ["push", "pull", "check"]
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=ALLOW_COMMANDS)

session = requests.Session()


@dataclass
class Credentials:
    evault_access_tok: str
    user_login: str


def get_credentials() -> Credentials:
    """
    returns a tuple of (evault-access-token, user-login)
    """
    r = requests.get(f"{SERVER}/api/auth")
    assert r.status_code == 200

    authURL = r.content.decode()

    print(
        f"To authenticate, go to the url "
        f"https://github.com/login/device and enter the code {authURL}"
    )

    s = parse_qs(urlparse(authURL).query).get("session_id")
    assert s != None

    session_id = s[0]

    max_attempts = 10
    attempt = 0
    auth_content: Optional[AuthDataDevice] = None

    poll_url = f"{SERVER}/api/token?{urlencode({"session_id": session_id})}"
    headers = {"Accept": "application/json"}

    while attempt <= max_attempts:
        attempt += 1

        r = requests.get(
            poll_url,
            headers=headers,
        )
    assert r.status_code == 200

    d = r.json()
    auth_content = AuthDataDevice(
        device_code=d["device_code"],
        expires_in=d["expires_in"],
        interval=d["interval"],
    )
    user_code = d["user_code"]

    # get user information from server
    r = requests.get(f"{SERVER}/api/auth/device?{urlencode(auth_content.__dict__)}")
    assert r.status_code == 200

    print("\tSuccess! Access token issued.")

    d = r.json()
    return Credentials(
        evault_access_tok=d["evault-access-token"], user_login=d["user-login"]
    )


def check_credentials(
    credentials_path: pathlib.Path,
) -> Optional[Credentials]:
    """
    returns the evault-access-token if it's not expired, None otherwise
    """
    print("Checking credentials...")
    try:
        with open(credentials_path, "r") as file:
            token = file.read()
            print("\tExisting credentials found, revalidating token...")
            r = session.get(
                f"{SERVER}/api/auth/check?{urlencode({'token': token, 'device_type': 'cli'})}"
            )

            if r.status_code == 403:
                print("\r\tSession expired.")
                # os.remove(CREDENTIALS_PATH)
                return None
            elif r.status_code != 200:
                raise Exception(f"Server error: {r.status_code}")

            d = r.json()
            print("\r\tSuccess! Token refreshed")
            return Credentials(
                evault_access_tok=d["evault-access-token"], user_login=d["user-login"]
            )

    except FileNotFoundError as e:
        print("\r\tToken not found / Not authenticated.")
        return None


if __name__ == "__main__":
    args = parser.parse_args()
    cmd = args.command.lower()

    # Authentication
    credentials = check_credentials(CREDENTIALS_PATH)
    if credentials == None:
        print("Authenticating...")
        credentials = get_credentials()
        with open(CREDENTIALS_PATH, "w") as f:
            f.write(credentials.evault_access_tok)

    token, user_login = credentials.evault_access_tok, credentials.user_login
    print(f"\tUser authenticated: {user_login}")
    print()

    try:
        repos = parse_remotes()
        print(repos)
    except IOError as e:
        print(f"Failed to validate remote repositories: {e}")
        exit(1)
