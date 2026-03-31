from __future__ import annotations
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DataSource(Base):
    __tablename__ = "data_source"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=True)
    description = Column(String, nullable=True)


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint("latitude", "longitude", name="uq_lat_lon"),)


class WeatherReading(Base):
    __tablename__ = "weather_reading"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("data_source.id"), nullable=False)
    observed_at = Column(DateTime, nullable=False, index=True)
    temperature_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    condition = Column(String, nullable=True)

    location = relationship("Location")
    source = relationship("DataSource")
    __table_args__ = (UniqueConstraint("location_id", "source_id", "observed_at",
                                       name="uq_loc_src_time"),)
