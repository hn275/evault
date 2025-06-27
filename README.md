# E-Vault

[![WebUI CI](https://github.com/hn275/evault/actions/workflows/webui-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/webui-ci.yml)
[![Server CI](https://github.com/hn275/evault/actions/workflows/server-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/server-ci.yml)

# Getting Started

Note: that there is a CI for Python 3.12 and 3.13, any other versions are not tested and may not work.

1. Install all project deps. Reminder to activate your virtual environment.

```sh
uv sync
```

2. Migrate database to the latest revision.

```sh
alembic upgrade head
```

3. Start server

```sh
uv run fastapi dev server/main.py
```

There's a Docker Compose `compose.yml` file for Redis + PostGreSQL server.
Mapping to the ports 5432 and 6379 respectively.

```sh
docker compose up -d
```

# Documentations

- [GitHub REST API](https://docs.github.com/en/rest/repos?apiVersion=2022-11-28)
