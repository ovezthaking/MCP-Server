from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Tool Example", port=8080)


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