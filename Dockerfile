FROM python:3.14-slim
LABEL authors="ovezo"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY my-mcp/src ./src/

RUN uv sync --frozen --no-dev

EXPOSE 8080

CMD ["uv", "run", "my-mcp"]