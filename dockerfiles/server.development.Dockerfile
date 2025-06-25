FROM rust:1.87.0-slim-bullseye

WORKDIR /evault_server
COPY src/ src/
COPY Cargo.lock .
COPY Cargo.toml .
COPY migrations/ migrations/

RUN apt update && apt upgrade -y && apt install -y pkg-config libssl-dev
RUN cargo install cargo-watch --locked

EXPOSE 8000
CMD ["cargo", "watch", "-x", "run --bin server"]
