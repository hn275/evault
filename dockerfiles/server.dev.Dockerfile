FROM python:3.14-rc-bullseye

WORKDIR /evault

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .
COPY server server

RUN uv sync

CMD ["uv", "run", "fastapi", "dev", "server/main.py"]
