from pydantic import BaseModel
from datetime import datetime

class TelemetryCreate(BaseModel):
    vehicle_id: int
    speed: float
    rpm: float
    fuel_level: float
    battery_temp: float

class TelemetryResponse(BaseModel):
    vehicle_id: int
    speed: float
    rpm: float
    fuel_level: float
    battery_temp: float
    timestamp: datetime

    class Config:
        from_attributes = True
