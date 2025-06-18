# E-Vault

[![WebUI CI](https://github.com/hn275/evault/actions/workflows/webui-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/webui-ci.yml)
[![Server CI](https://github.com/hn275/evault/actions/workflows/server-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/server-ci.yml)

# Getting Started

Install all project deps.

```sh
# install all deps
pip install -r requirements.txt
```

Migrate database to the latest revision.

```sh
alembic upgrade head
```

Start server

```sh
fastapi dev src/server/main.py
```

There's a Docker Compose `compose.yml` file for Redis + PostGreSQL server.
Mapping to the ports 5432 and 6379 respectively.

```sh
docker compose up -d
```

# Documentations

- [GitHub REST API](https://docs.github.com/en/rest/repos?apiVersion=2022-11-28)
