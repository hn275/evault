import dotenv, os
from shared.utils import env_or_default
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .storage import Redis
from .httpreqs import HttpClient
from .oauth import GitHubOauth

dotenv.load_dotenv()

GITHUB_OAUTH_CLIENT_ID = os.environ["GITHUB_OAUTH_CLIENT_ID"]
GITHUB_OAUTH_CLIENT_SECRET = os.environ["GITHUB_OAUTH_CLIENT_SECRET"]
GITHUB_OAUTH_REDIRECT_URI = env_or_default(
    "GITHUB_OAUTH_REDIRECT_URI", "http://localhost:5173/auth/github"
)
GITHUB_OAUTH_STATE_TTL = 120  # 2 minutes

EVAULT_SESSION_TOKEN_TTL = 300  # 5 minutes
EVAULT_WEB_URL = env_or_default("EVAULT_WEB_URL", "http://localhost:5173")
EVAULT_TOKEN_POLL_TTL = 30
EVAULT_TOKEN_POLL_MAX_ATTEMPT = 10

REDIS_HOST = env_or_default("REDIS_HOST", "localhost")
REDIS_PORT_DEFAULT = 6379

redis = Redis(REDIS_HOST, port=REDIS_PORT_DEFAULT)
redis.ping()

app = FastAPI()
app.add_middleware(
    # TODO: configure this for prod
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


httpclient = HttpClient()


oauth_client = GitHubOauth(
    client_id=GITHUB_OAUTH_CLIENT_ID,
    client_secret=GITHUB_OAUTH_CLIENT_SECRET,
    redirect_uri=GITHUB_OAUTH_REDIRECT_URI,
)
