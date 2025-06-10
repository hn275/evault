#!make
-include .env

# create and run dbs
make-local-dbs:
	@docker compose up -d

# run alembic migrations
run-migrations:
	@alembic upgrade head

local-frontend-dev:
	@npm run dev --prefix webui

local-backend-dev:
	@fastapi dev src/server/main.py