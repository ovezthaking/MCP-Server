# MCP Server - Model Context Protocol Server

A comprehensive **Model Context Protocol (MCP)** server implementation built with Python and FastMCP. This project demonstrates a production-ready MCP server with multiple tools and resources for data access, weather information, and cryptocurrency market data.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Development](#development)
- [Building & Publishing](#building--publishing)
- [Debugging](#debugging)
- [Requirements](#requirements)

---

## 🎯 Overview

This MCP Server provides a bridge between Claude Desktop and various data sources and services. It exposes resources (structured data access) and tools (functional operations) through the MCP protocol, enabling Claude to interact with:

- **Local Data**: Notes and user information from JSON and SQLite databases
- **External APIs**: Real-time cryptocurrency prices and weather data
- **Utility Functions**: Basic computational tools

The server runs via Server-Sent Events (SSE) and can be easily integrated into Claude Desktop or other MCP-compatible clients.

---

## ✨ Features

### Resources
- **`data://notes`** - Access stored notes from JSON file with full content and metadata
- **`data://users`** - Query user information directly from SQLite database

### Tools

#### Data Operations
- **`get_notes()`** - Retrieve all stored notes in JSON format
- **`query_users()`** - Fetch user database records with id, name, and email

#### Utility Functions
- **`sum(a: int, b: int)`** - Basic arithmetic operation
- **`get_weather(city: str, unit: str = "celsius")`** - Get weather information for any city

#### Cryptocurrency Services
- **`get_crypto_price(coin_id: str = "bitcoin")`** - Get current price, market cap, and 24h change for cryptocurrencies
  - Supports: bitcoin, ethereum, solana, cardano, and 300+ other coins
  - Returns: USD price, market cap, and percentage change
- **`get_top_coins(limit: int = 5)`** - Retrieve top cryptocurrencies sorted by market capitalization

---

## 📁 Project Structure

```
MCP-Server/
├── Dockerfile                 # Docker configuration for containerization
├── pyproject.toml            # Workspace configuration (uv workspace setup)
├── README.md                 # This file
├── my-mcp/                   # Main MCP server package
│   ├── pyproject.toml        # Package metadata and dependencies
│   ├── README.md             # Package-specific documentation
│   ├── data/
│   │   ├── notes.json        # Sample notes data
│   │   └── database.db       # SQLite database (users table)
│   └── src/
│       └── my_mcp/
│           ├── __init__.py   # Package initialization & entry point
│           └── server.py     # Main MCP server implementation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- [Claude Desktop](https://claude.ai/download) (for integration)

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd MCP-Server
```

#### 2. Install Dependencies
```bash
uv sync
```

#### 3. Run the Server
```bash
cd my-mcp
uv run my-mcp
```

The server will start on `http://0.0.0.0:8080` and listen for SSE connections.

---

## ⚙️ Configuration

### Connect to Claude Desktop

Choose your operating system:

#### macOS
Edit: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/MCP-Server/my-mcp",
        "run",
        "my-mcp"
      ]
    }
  }
}
```

#### Windows
Edit: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\OneDrive\\Dokumenty\\REPOS\\MCP-Server\\my-mcp",
        "run",
        "my-mcp"
      ]
    }
  }
}
```

#### Production Configuration (Published Server)
Once published to PyPI:

```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "uvx",
      "args": ["my-mcp"]
    }
  }
}
```

After updating the configuration, restart Claude Desktop to load the new server.

---

## 📖 Usage

### Using with Claude

Once connected to Claude Desktop, you can:

1. **Query Resources**: "Show me the notes stored in the server"
2. **Call Tools**: "What's the current price of Bitcoin?"
3. **Complex Operations**: "Get the top 10 cryptocurrencies and summarize them"

### Direct Server Testing

```bash
# Start the server
cd my-mcp
uv run my-mcp

# In another terminal, test the endpoints
# Resources and tools will be accessible via MCP protocol
```

---

## 📡 API Reference

### Resources

#### `data://notes`
Returns all notes from `data/notes.json`
```json
[
  {"id": 1, "title": "First note", "content": "Hello from MCP!"},
  {"id": 2, "title": "Second note", "content": "MCP resources work!"}
]
```

#### `data://users`
Returns user records from SQLite database
```json
[
  {"id": 1, "name": "John Doe", "email": "john@example.com"},
  {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]
```

### Tools

#### `query_users()`
- **Returns**: JSON array of user records
- **Example**:
  ```json
  [
    {"id": 1, "name": "John Doe", "email": "john@example.com"}
  ]
  ```

#### `get_notes()`
- **Returns**: JSON array of all notes
- **Example**:
  ```json
  [
    {"id": 1, "title": "First note", "content": "Hello from MCP!"}
  ]
  ```

#### `sum(a: int, b: int)`
- **Parameters**: Two integers
- **Returns**: Integer (sum of a and b)
- **Example**: `sum(5, 3)` → `8`

#### `get_weather(city: str, unit: str = "celsius")`
- **Parameters**:
  - `city` (required): City name
  - `unit` (optional): "celsius" or "fahrenheit" (default: "celsius")
- **Returns**: String with weather information
- **Example**: `get_weather("London")` → `"Weather in London: 22C"`

#### `get_crypto_price(coin_id: str = "bitcoin")`
- **Parameters**: `coin_id` - Cryptocurrency identifier (default: "bitcoin")
- **Returns**: JSON with price, market cap, and 24h change
- **Example**:
  ```json
  {
    "coin": "bitcoin",
    "price_usd": 45000,
    "market_cap_usd": 900000000000,
    "change_24h_percent": 2.5
  }
  ```

#### `get_top_coins(limit: int = 5)`
- **Parameters**: `limit` - Number of coins to return (default: 5)
- **Returns**: JSON array of top coins by market cap
- **Example**:
  ```json
  [
    {
      "rank": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "price_usd": 45000,
      "change_24h_percent": 2.5
    }
  ]
  ```

---

## 💻 Development

### Setup Development Environment

```bash
# Install all dependencies including dev tools
uv sync

# Navigate to the server package
cd my-mcp
```

### Project Dependencies

- **mcp** (>=1.26.0) - Model Context Protocol library
- **uv** - Fast Python package manager and installer
- Python 3.14+

### Code Style

The project follows Python best practices:
- Type hints for function arguments and returns
- Clear docstrings for all tools
- Organized resource and tool definitions

### File Structure

- **`server.py`** - Main MCP server logic with all resources and tools
  - FastMCP initialization
  - Resource definitions with `@mcp.resource()` decorator
  - Tool definitions with `@mcp.tool()` decorator
- **`__init__.py`** - Package entry point and imports
- **`data/`** - Static data files (JSON notes and SQLite database)

---

## 🏗️ Building & Publishing

### Prepare for Distribution

#### 1. Update Project Metadata

Edit `my-mcp/pyproject.toml`:
```toml
[project]
name = "my-mcp"
version = "0.1.0"
description = "A MCP server for data access and cryptocurrency information"
authors = [{name = "Your Name", email = "your@email.com"}]
```

#### 2. Sync Dependencies
```bash
uv sync
```

#### 3. Build Package
```bash
uv build
```

This creates distributions in `dist/`:
- Source tarball (`.tar.gz`)
- Wheel package (`.whl`)

#### 4. Publish to PyPI

```bash
uv publish
```

**Authentication Options**:
```bash
# Using token (recommended)
uv publish --token pypi-AgEIcHlwaS5vcmc...

# Using username/password
uv publish --username __token__ --password pypi-AgEIcHlwaS5vcmc...

# Environment variables
export UV_PUBLISH_TOKEN=pypi-AgEIcHlwaS5vcmc...
uv publish
```

---

## 🐛 Debugging

### Running the Server in Debug Mode

```bash
cd my-mcp
uv run my-mcp
```

The server logs will be output to the console.

### Viewing Claude Desktop Logs

#### macOS
```bash
tail -f ~/Library/Logs/Claude/mcp.log
```

#### Windows
```
%APPDATA%\Claude\logs\
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Server won't connect | Verify Claude config path and restart Claude Desktop |
| Module not found errors | Run `uv sync` to install all dependencies |
| Database errors | Ensure `data/database.db` exists with proper schema |
| API rate limits | CoinGecko API has free rate limits; consider caching |

### Testing Tools

To manually test a tool's functionality:

```python
# In Python REPL
from my_mcp.server import get_crypto_price, get_top_coins
print(get_crypto_price("ethereum"))
print(get_top_coins(10))
```

---

## 📋 Requirements

### System Requirements
- Python 3.14 or higher
- 50MB free disk space
- Internet connection (for crypto/weather APIs)

### Runtime Dependencies
- `mcp` - Model Context Protocol implementation
- `httpx` - HTTP client for API calls (implicit via mcp)

### Optional Dependencies
- `uv` - For development and package management (recommended)
- Docker - For containerized deployment

---

## 📄 License

[Add your license information here]

## 👤 Author

**Oliwer Urbaniak**  
📧 oliwerx12@gmail.com

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please feel free to check the issues page.

---

## 📞 Support

For issues or questions:
1. Check the [Debugging](#debugging) section
2. Review server logs
3. Open an issue in the repository

---

## 🔗 Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [CoinGecko API](https://www.coingecko.com/en/api)

---

**Last Updated**: 29 march 2026  
**Version**: 0.1.0