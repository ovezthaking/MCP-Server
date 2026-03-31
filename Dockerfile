FROM python:3.14-slim
LABEL authors="ovezo"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock .env ./
COPY my-mcp/ ./my-mcp/

RUN uv sync --frozen --no-dev --package my-mcp

ENV PORT=8080 \
	HOST=0.0.0.0 \
	DB_PATH=data/app.db

EXPOSE 8080

CMD ["uv", "run", "--package", "my-mcp", "my-mcp"]