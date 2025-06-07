# E-Vault

# Getting Started

Install all project deps.

```sh
pip install -e . # idk why but it won't import without doing this...
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
- [Alchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20_poly1305.html) for XChaCha20-Poly1305
- [redis-py](https://redis.readthedocs.io/en/stable/index.html)
