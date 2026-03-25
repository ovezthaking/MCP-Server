FROM python:3.14-slim
LABEL authors="ovezo"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY my-mcp/ ./my-mcp/

RUN uv sync --frozen --no-dev --package my-mcp

EXPOSE 8080

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "--package", "my-mcp", "my-mcp"]