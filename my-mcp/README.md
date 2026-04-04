# my-mcp

This is the packaged MCP server inside the workspace. The main implementation lives in `src/my_mcp/server.py` and exposes the same `DataTools` server documented in the repository root README.

## Features

- Weather tools backed by SQLite and SQLAlchemy
- Crypto tools backed by CoinGecko
- A `weather://latest` resource
- A `weather_summary` prompt

## Run

From this directory:

```bash
uv run my-mcp
```

## Database

The package uses Alembic migrations and stores data in SQLite. The default database path is `data/app.db`, and you can override it with `DB_PATH`.

## Development

Useful commands:

```bash
uv sync
uv run alembic upgrade head
uv run python -m my_mcp.db.seed
uv build
```