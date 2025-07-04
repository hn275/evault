import dotenv
import os
from .utils import env_or_default

dotenv.load_dotenv()

GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
GITHUB_OAUTH_REDIRECT_URI = env_or_default(
    "GITHUB_OAUTH_REDIRECT_URI", "http://localhost:5173/auth/github"
)
GITHUB_OAUTH_STATE_TTL = 120  # 2 minutes

EVAULT_SESSION_TOKEN_TTL = (
    3000  # 5 minutes // TODO: change this back to 300 seconds (5 mins)
)
EVAULT_WEB_URL = env_or_default("EVAULT_WEB_URL", "http://localhost:5173")
EVAULT_TOKEN_POLL_TTL = 30
EVAULT_TOKEN_POLL_MAX_ATTEMPT = 10
EVAULT_DEBUG: bool = env_or_default("EVAULT_DEBUG", "0").lower() == "1"

REDIS_HOST = env_or_default("REDIS_HOST", "localhost")
REDIS_PORT_DEFAULT = 6379

PSQL_USER = os.environ["POSTGRES_USER"]
PSQL_PASSWORD = os.environ["POSTGRES_PASSWORD"]
PSQL_HOST = os.environ["POSTGRES_HOST"]
PSQL_PORT = env_or_default("POSTGRES_PORT", "5432")
PSQL_DBNAME = os.environ["POSTGRES_DBNAME"]
PSQL_SSLMODE = env_or_default("POSTGRES_SSL", "require")
assert PSQL_SSLMODE == "require" or PSQL_SSLMODE == "disable"
