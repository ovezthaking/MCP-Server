# MCP-Server

MCP-Server is a small Python workspace built around a FastMCP server. The main package lives in `my-mcp/` and exposes a server named `DataTools` that combines local weather data from SQLite with live cryptocurrency tools from CoinGecko.

## What it includes

- MCP tools for querying weather readings and calculating averages from the local database
- MCP tools for fetching crypto prices and top coins from CoinGecko
- A dynamic MCP resource at `weather://latest`
- A weather summary prompt for client-side LLM workflows
- SQLite persistence with SQLAlchemy models and Alembic migrations
- Docker support for running the server in a container

## Repository layout

```text
.
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── my-mcp/
    ├── alembic.ini
    ├── migrations/
    ├── data/
    ├── pyproject.toml
    ├── README.md
    └── src/my_mcp/
        ├── server.py
        └── db/
```

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)

## Setup

Install dependencies from the workspace root:

```bash
uv sync
```

The server uses environment variables from `.env` when available. The most important ones are:

- `HOST` - bind address for the MCP server, for example `0.0.0.0`
- `PORT` - SSE port, for example `8080`
- `DB_PATH` - path to the SQLite database, defaulting to `data/app.db`

## Database

The database schema is managed with Alembic and stored in SQLite.

Run migrations from the package directory:

```bash
cd my-mcp
uv run alembic upgrade head
```

If you want sample data, you can seed the database with:

```bash
cd my-mcp
uv run python -m my_mcp.db.seed
```

## Run locally

Start the server from the repository root:

```bash
uv run --package my-mcp my-mcp
```

By default the server runs over SSE and listens on the host and port defined by `HOST` and `PORT`.

## Docker

Build the image:

```bash
docker build -t mcp-server .
```

Run it:

```bash
docker run --rm -p 8080:8080 -e HOST=0.0.0.0 -e PORT=8080 -e DB_PATH=data/app.db mcp-server
```

## MCP tools and resource

### Tools

- `readings_for_city(city, hours=6)` - returns recent weather readings for a city
- `average_temp(city, hours=6)` - returns the average temperature for a city
- `get_crypto_price(coin_id="bitcoin")` - returns price, market cap, and 24h change for a coin
- `get_top_coins(limit=5)` - returns the top cryptocurrencies by market cap

### Resource

- `weather://latest` - returns the newest weather reading in the database

### Prompt

- `weather_summary(city, hours=6)` - prepares a concise weather summary prompt for a client or LLM

## Client configuration

For SSE-based clients, point them at the running server URL, for example:

```text
http://localhost:8080/sse
```

For Claude Desktop or similar tools, use a command-based config that launches `uv run --package my-mcp my-mcp` from this repository.

## Notes

- The crypto tools call the public CoinGecko API, so internet access is required.
- The database file is created automatically if it does not exist.
- Alembic is already configured to use `sqlite:///./data/app.db` inside `my-mcp/alembic.ini`.