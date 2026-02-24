from sqlalchemy.orm import Session
from .models import TelemetryRecord, Alert

def fleet_overview(db: Session):
    records = db.query(TelemetryRecord).all()
    alerts = db.query(Alert).all()

    if not records:
        return {"message": "no data"}

    avg_speed = sum(r.speed for r in records) / len(records)
    avg_fuel = sum(r.fuel_level for r in records) / len(records)

    vehicle_ids = {r.vehicle_id for r in records}

    return {
        "total_vehicles": len(vehicle_ids),
        "total_records": len(records),
        "active_alerts": len(alerts),
        "average_speed": round(avg_speed, 2),
        "average_fuel_level": round(avg_fuel, 2)
    }

def vehicle_utilization(vehicle_id, db: Session):
    records = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.vehicle_id == vehicle_id)
        .all()
    )

    if not records:
        return {"message": "no data"}

    driving = sum(1 for r in records if r.speed > 5)
    idle = sum(1 for r in records if r.speed <= 5)

    distance = sum(r.speed for r in records) / 3600  # simple estimate

    return {
        "vehicle_id": vehicle_id,
        "driving_points": driving,
        "idle_points": idle,
        "estimated_distance_km": round(distance, 2)
    }
