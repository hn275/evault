from src.server.validators import valid_user_repo_string


def test_validate_user_repo_string():
    valid_input = [
        "username/repo",
        "user-name/repo_name",
        "user123/repo123",
        "user-name-123/repo-name_456",
    ]
    # Valid cases

    # Invalid cases
    invalid_input = [
        "user.name/repo.name",
        "username/",
        "/repo",
        "username/repo/",
        "username//repo",
        "username/repo//",
        "username/repo name",
        "username/repo@name",
        "user--name/repo",
        "-username/repo",
        "username-/repo",
    ]

    for user_repo in valid_input:
        assert valid_user_repo_string(user_repo), f"Failed for valid input: {user_repo}"

    for user_repo in invalid_input:
        assert not valid_user_repo_string(
            user_repo
        ), f"Failed for invalid input: {user_repo}"
