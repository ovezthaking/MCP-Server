from datetime import datetime, timedelta

from my_mcp.db.models import DataSource, Location, WeatherReading
from my_mcp.db.session import SessionLocal


def run():
    with SessionLocal() as s:
        # upsert DataSource
        src = s.query(DataSource).filter_by(name="open-meteo").one_or_none()
        if not src:
            src = DataSource(name="open-meteo",
                             url="https://open-meteo.com",
                             description="Downloaded sample forecast/obs")
            s.add(src)
            s.flush()

        # upsert a Location
        krk = s.query(Location).filter_by(name="Kraków").one_or_none()
        if not krk:
            krk = Location(name="Kraków", latitude=50.0647, longitude=19.9450)
            s.add(krk)
            s.flush()

        # add a few readings
        base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        readings = [
            WeatherReading(location_id=krk.id, source_id=src.id,
                           observed_at=base - timedelta(hours=i),
                           temperature_c=18.0 + i * 0.2,
                           humidity_pct=55.0 - i,
                           condition="partly cloudy")
            for i in range(6)
        ]
        s.add_all(readings)
        s.commit()


if __name__ == "__main__":
    run()
