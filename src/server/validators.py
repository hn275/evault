import re


def valid_user_repo_string(user_user: str) -> bool:
    """validate_user_repo_string checks if the provided string is a valid GitHub username/repo format."""
    # GitHub username/repo pattern: alphanumeric, hyphens, underscores
    # Cannot start or end with hyphen, cannot have consecutive hyphens
    pattern = re.compile(r"^(?!-)(?!.*--)[a-zA-Z0-9-]{1,39}(?<!-)/[a-zA-Z0-9._-]+$")
    return bool(re.match(pattern, user_user))
