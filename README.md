# E-Vault

[![WebUI CI](https://github.com/hn275/evault/actions/workflows/webui-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/webui-ci.yml)
[![Server CI](https://github.com/hn275/evault/actions/workflows/server-ci.yml/badge.svg)](https://github.com/hn275/evault/actions/workflows/server-ci.yml)

# Getting Started

## Docker Compose

The recommended way to run the application is using `docker compose`

```sh
docker compose up
```

## Local

Install all project deps.

```sh
# NOTE: if running into importing issue, install the project as a module on
# your machine
pip install -e .

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
docker compose up
```

# Documentations

- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) - database migration
- [Alchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) - ORM (comes with Alembic)
- [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20_poly1305.html) for XChaCha20-Poly1305
- [redis-py](https://redis.readthedocs.io/en/stable/index.html)
- [GitHub REST API](https://docs.github.com/en/rest/repos?apiVersion=2022-11-28)
