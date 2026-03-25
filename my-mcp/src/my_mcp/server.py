from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path
import sqlite3

mcp = FastMCP(name="Tool Example", port=8080, host="0.0.0.0")

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DB_PATH = DATA_DIR / "database.db"

@mcp.resource("data://notes")
def notes_resource() -> str:
    with open(DATA_DIR / "notes.json", "r") as f:
        return json.dumps(json.load(f), indent=2)

@mcp.resource("data://users")
def users_resource() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return json.dumps([{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows], indent=2)

@mcp.tool()
def query_users() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return json.dumps([{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows], indent=2)

@mcp.tool()
def get_notes() -> str:
    with open(DATA_DIR / "notes.json", "r") as f:
        return json.dumps(json.load(f), indent=2)

@mcp.tool()
def sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get weather for a city."""
    # This would normally call a weather API
    return f"Weather in {city}: 22degrees{unit[0].upper()}"


def main():
    """Entry point for the direct execution server."""
    mcp.run("sse")


if __name__ == "__main__":
    main()