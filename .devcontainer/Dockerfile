FROM python:3.13-slim-bullseye

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /workspace
COPY . .