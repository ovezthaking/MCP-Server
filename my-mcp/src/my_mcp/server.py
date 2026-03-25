from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path

mcp = FastMCP(name="Tool Example", port=8080, host="0.0.0.0")

DATA_DIR = Path(__file__).parent.parent.parent / "data"

@mcp.resource("data://notes")
def get_notes_resource() -> str:
    with open(DATA_DIR / "notes.json", "r") as f:
        return json.dumps(json.load(f), indent=2)

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