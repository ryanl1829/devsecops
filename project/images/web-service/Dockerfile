FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY . /app

CMD ["sh", "-c", \
     "uv run gunicorn web_service:app --bind 0.0.0.0:8000 --timeout 120"]