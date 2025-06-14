from blake3 import blake3
import sys

KEY_LENGTH = 32  # 32 bytes = 256 bits

_KDF_CONTEXT_STRING = "evault 2069-04-20 00:04:20 evault key construction v0"


def derive_repo_key(
    server_secret: bytes,
    repo_id: int,
    repo_password: str,
    key_len: int = KEY_LENGTH,
) -> bytes:
    int64_bytelen = 8  # 64 bits integer
    key_material = (
        server_secret
        + repo_id.to_bytes(int64_bytelen, sys.byteorder)
        + repo_password.encode()
    )
    return blake3(key_material, derive_key_context=_KDF_CONTEXT_STRING).digest(
        length=key_len
    )
