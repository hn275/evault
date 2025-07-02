FROM python:3.14-rc-bullseye

WORKDIR /evault_server

RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev 

RUN pip install uv

COPY . .

RUN uv sync

CMD ["uv", "run", "fastapi", "dev", "server/main.py"]
