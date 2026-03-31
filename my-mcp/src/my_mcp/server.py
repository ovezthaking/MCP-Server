from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Prompt, UserMessage, AssistantMessage, Message
import httpx
import json
import os
from dotenv import load_dotenv
from my_mcp.db.session import SessionLocal
from my_mcp.db.models import WeatherReading, Location

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
mcp = FastMCP(name="DataTools", host=HOST, port=PORT)

# ---------- TOOLS ----------


@mcp.tool()
def readings_for_city(city: str, hours: int = 6) -> List[Dict[str, Any]]:
    """Return recent weather readings for `city` over the past `hours` hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    with SessionLocal() as s:
        loc = s.query(Location).filter_by(name=city).one_or_none()
        if not loc:
            return []
        q = (s.query(WeatherReading)
               .filter(WeatherReading.location_id == loc.id,
                       WeatherReading.observed_at >= cutoff)
               .order_by(WeatherReading.observed_at.desc()))
        rows = q.all()
        return [
            {
                "observed_at": r.observed_at.isoformat(),
                "temperature_c": r.temperature_c,
                "humidity_pct": r.humidity_pct,
                "condition": r.condition,
            } for r in rows
        ]


@mcp.tool()
def average_temp(city: str, hours: int = 6) -> Optional[float]:
    """Average temperature (°C) for `city` for the past `hours` hours."""
    data = readings_for_city(city=city, hours=hours)
    temps = [d["temperature_c"] for d in data if d["temperature_c"] is not None]
    if not temps:
        return None
    return sum(temps) / len(temps)


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


# ---------- RESOURCES ----------


@mcp.resource("weather://latest")
def latest_weather() -> str:
    """Dynamic resource: latest weather reading across all locations."""
    with SessionLocal() as s:
        r = (s.query(WeatherReading)
               .order_by(WeatherReading.observed_at.desc())
               .first())
        if not r:
            return "No readings yet"
        return (
            f"Latest reading: {r.observed_at.isoformat()} "
            f"temp={r.temperature_c}°C humidity={r.humidity_pct}% "
            f"loc_id={r.location_id}"
        )


# ---------- PROMPTS ----------


@mcp.prompt("weather_summary")
def weather_summary(city: str, hours: int = 6) -> List[Message]:
    """
    Summarize weather for the past N hours.
    Variables:
      - city: City name found in DB (e.g., 'Kraków')
      - hours: Lookback window
    """
    # Prompt messages shown to the client/LLM
    msgs: List[Message] = [
        UserMessage(
            content=(
                f"Provide a concise summary of the last {hours} hours of weather in {city}. "
                "If there are no readings, say so. Be precise with times and averages."
            )
        )
    ]
    return msgs


def main():
    mcp.run("sse")


if __name__ == "__main__":
    main()
