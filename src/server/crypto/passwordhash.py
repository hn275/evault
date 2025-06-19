import secrets
from argon2.profiles import RFC_9106_LOW_MEMORY
from argon2 import PasswordHasher


def hash(plaintext_password: str) -> str:
    """
    Hashes the plaintext password with a 32 byte salt, using Argon2ID,
    and the RFC_9106_LOW_MEMORY defined parameters.
    """
    return PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY).hash(
        plaintext_password,
        salt=secrets.token_bytes(32),
    )
