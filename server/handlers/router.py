from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from loguru import logger
from . import dashboard, auth, user


mux = FastAPI()
mux.add_middleware(
    # TODO: configure this for prod
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


routers = [dashboard.router, auth.router, user.router]

for router in routers:
    mux.include_router(router)
    logger.info(f"included router: {router.prefix}")


@mux.get("/api/healthcheck")
def healthcheck():
    return Response(status_code=status.HTTP_200_OK)
