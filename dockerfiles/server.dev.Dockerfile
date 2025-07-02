FROM python:3.14-rc-bullseye

WORKDIR /evault_server

RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev 

RUN pip install uv

COPY server server
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "server/main.py"]
