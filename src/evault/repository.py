import re, pathlib
from typing import List, Optional


# REPO PARSER
# Regex pattern to match username/repo from Git URLs
GIT_URL_PATTERN = re.compile(
    r"(?:https?://[^/]+/|git@[^:]+:)([^/]+)/([^/\s]+?)(?:\.git)?/?$"
)


def extract_username_repo(git_url: str) -> Optional[str]:
    """
    Extract username and repository name from Git clone URLs.

    Supports both SSH and HTTPS formats:
    - https://github.com/username/repo.git
    - https://github.com/username/repo
    - git@github.com:username/repo.git
    - git@github.com:username/repo
    """
    match = re.match(GIT_URL_PATTERN, git_url.strip())
    if match:
        username = match.group(1)
        repo = match.group(2)
        return f"{username}/{repo}"
    return None


type Remote = tuple[str, str]


def parse_remotes() -> List[Remote]:
    out = []
    remote_regex = re.compile(r'\[remote "([^"]+)"\]')
    url_regex = re.compile(r"\s*url\s*=\s*(.+)")
    config_file = pathlib.Path(".git/config")

    with open(config_file, "r") as file:
        while True:
            line = file.readline()
            if line == "":
                break

            matched = remote_regex.match(line)
            if not matched:
                continue

            remote_name = matched.group(1)
            line = file.readline()
            if line == "":
                raise IOError(f"invalid {config_file} file")

            url_matched = url_regex.match(line)
            if not url_matched:
                raise IOError(
                    f"invalid repository url for remote '{remote_name}' in {config_file} file"
                )
            url_matched = url_matched.group(1)

            remote_url = extract_username_repo(url_matched)
            if remote_url == None:
                raise IOError(
                    f"invalid repository url for remote '{remote_name}' in {config_file} file"
                )
            out.append((remote_name, remote_url))

    return out
