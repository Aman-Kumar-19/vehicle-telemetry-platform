from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    model = Column(String)

class TelemetryRecord(Base):
    __tablename__ = "telemetry_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    speed = Column(Float)
    rpm = Column(Float)
    fuel_level = Column(Float)
    battery_temp = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer)
    alert_type = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
