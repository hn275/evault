from cli.repository import extract_username_repo


def test_extract_username_repo():
    # Test cases
    test_urls = [
        ("https://github.com/torvalds/linux.git", "torvalds/linux"),
        ("https://github.com/torvalds/linux", "torvalds/linux"),
        ("git@github.com:torvalds/linux.git", "torvalds/linux"),
        ("git@github.com:torvalds/linux", "torvalds/linux"),
        ("https://gitlab.com/user/my-project.git", "user/my-project"),
        ("git@gitlab.com:user/my-project.git", "user/my-project"),
        ("https://bitbucket.org/atlassian/stash.git", "atlassian/stash"),
        ("git@bitbucket.org:atlassian/stash.git", "atlassian/stash"),
        (
            "https://github.com/username/repo-with-dashes.git",
            "username/repo-with-dashes",
        ),
        (
            "git@github.com:username/repo_with_underscores.git",
            "username/repo_with_underscores",
        ),
    ]

    print()
    for case in test_urls:
        (url, expected) = case
        result = extract_username_repo(url)
        print(f"✓ {url} → {result}")
        assert result != None
        assert result == expected
