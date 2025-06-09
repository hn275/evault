from dataclasses import dataclass
import time, json
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


def get_access_token() -> Optional[str]:
    r = session.get(f"{SERVER}/api/auth?device_type=cli")
    assert r.status_code == 200

    authURL = r.content.decode()

    print(f"To authenticate, go to {authURL}")

    s = parse_qs(urlparse(authURL).query).get("session_id")
    assert s != None

    session_id = s[0]

    max_attempts = 10
    attempt = 0

    poll_url = f"{SERVER}/api/auth/poll?{urlencode({"session_id": session_id})}"

    while attempt <= max_attempts:
        attempt += 1

        r = session.get(poll_url)
        if r.status_code == 403:
            print("Authentication request timed out.")
            exit(1)

        assert r.status_code == 200
        d = json.loads(r.json())

        if d.get("status") == "pending":
            time.sleep(5)
            continue

        assert d["status"] == "ok"
        access_token = d.get("access_token")

        assert access_token != None
        return access_token

    return None


def check_credentials(
    credentials_path: pathlib.Path,
) -> Optional[str]:
    print("Checking credentials...")
    return None
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
    access_token = check_credentials(CREDENTIALS_PATH)
    if access_token == None:
        print("Authenticating...")
        access_token = get_access_token()
        print("\tSuccess! Access token issued.")
        with open(CREDENTIALS_PATH, "w") as f:
            f.write(access_token)

    print(f"\tAuthentication success")

    try:
        repos = parse_remotes()
        print(repos)
    except IOError as e:
        print(f"Failed to validate remote repositories: {e}")
        exit(1)
