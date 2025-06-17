from src.pkg.types import GitHubUser, GithubAuthToken, UserSession
from copy import deepcopy

test_data = {
    "device_type": "web",
    "user.id": 1,
    "user.name": "Test User 1",
    "user.avatar_url": "",
    "user.login": "testuser1",
    "user.type": "User",
    "gh_token.access_token": "usertoken1",
    "gh_token.token_type": "bearer",
    "gh_token.scope": "",
}

test_user = GitHubUser(
    id=1,
    name="Test User 1",
    avatar_url="",
    login="testuser1",
    type="User",
)

test_token = GithubAuthToken(
    access_token="usertoken1",
    token_type="bearer",
    scope="",
)

test_session = UserSession("web", user=test_user, gh_token=test_token)


def test_user_session_marshalling():
    s = deepcopy(test_session)
    assert s.make_flat_map() == test_data

    f = deepcopy(test_data)
    s1 = UserSession.from_flat_map(f)
    assert s1 == s
    assert s1.csrf_token == None

    f["csrf_token"] = "foobarbaz"
    s1 = UserSession.from_flat_map(f)
    assert s1 != s
    assert s1.csrf_token == f["csrf_token"]
