import secrets
from src.server.crypto.kdf import derive_repo_key, KEY_LENGTH
from random import randint


password = "password"
server_secret = secrets.token_bytes(32)


def test_derive_repo_key_length():
    key = derive_repo_key(
        server_secret=server_secret,
        repo_id=123,
        repo_password=password,
    )
    assert len(key) == KEY_LENGTH

    key = derive_repo_key(
        server_secret=server_secret,
        repo_id=123,
        repo_password=password,
        key_len=10,
    )
    assert len(key) == 10


def test_derive_repo_key_uniqueness():
    s = set()
    for i in range(0xFFFF):
        key = derive_repo_key(
            server_secret=server_secret,
            repo_id=i,
            repo_password=password,
        )
        s.add(key)
        assert len(s) == i + 1


def test_derive_repo_key_same_password_different_repo():
    for _ in range(0xFFFF):
        id1 = randint(0, 0xFFFFFF)
        id2 = randint(0, 0xFFFFFF)

        while id2 == id1:
            id2 = randint(0, 0xFFFFFF)

        key1 = derive_repo_key(
            server_secret=server_secret,
            repo_id=id1,
            repo_password=password,
        )

        key2 = derive_repo_key(
            server_secret=server_secret,
            repo_id=id2,
            repo_password=password,
        )
        assert key1 != key2


def test_derive_repo_key_different_password_same_repo():
    for i in range(0xFFFF):
        key1 = derive_repo_key(
            server_secret=server_secret,
            repo_id=123,
            repo_password=password,
        )

        password2 = password + str(i)
        key2 = derive_repo_key(
            server_secret=server_secret,
            repo_id=123,
            repo_password=password2,
        )
        assert key1 != key2
