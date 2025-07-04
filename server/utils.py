import os


def env_or_default(key: str, default_value: str) -> str:
    value = os.environ.get(key)
    if value == None:
        print(
            f"[WARN] environment variable not set for '{key}', "
            f"using default value '{default_value}'"
        )
        return default_value
    return value
