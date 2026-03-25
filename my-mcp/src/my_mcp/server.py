from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path
import sqlite3
import httpx

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
    """Get users from database"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return json.dumps([{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows], indent=2)


@mcp.tool()
def get_notes() -> str:
    """Get notes from data"""
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


@mcp.tool()
def get_crypto_price(coin_id: str = "bitcoin") -> str:
    """Get current price, market cap and 24h change for a cryptocurrency.
    Use coin ids like: bitcoin, ethereum, solana, cardano
    """
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': coin_id,
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_change': 'true'
    }
    response = httpx.get(url, params=params)
    data = response.json()

    if coin_id not in data:
        return f'Coin "{coin_id}" not found.'

    coin = data[coin_id]
    return json.dumps({
        'coin': coin_id,
        'price_usd': coin['usd'],
        'market_cap_usd': coin['usd_market_cap'],
        'change_24h_percent': coin['usd_24h_change']
    }, indent=2)


@mcp.tool()
def get_top_coins(limit: int = 5) -> str:
    """Get top cryptocurrencies by market cap"""
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1
    }

    response = httpx.get(url, params=params)
    data = response.json()

    result = []
    for coin in data:
        result.append({
            'rank': coin['market_cap_rank'],
            'name': coin['name'],
            'symbol': coin['symbol'].upper(),
            'price_usd': coin['current_price'],
            'change_24h_percent': coin['price_change_percentage_24h']
        })

    return json.dumps(result, indent=2)


def main():
    """Entry point for the direct execution server."""
    mcp.run("sse")


if __name__ == "__main__":
    main()