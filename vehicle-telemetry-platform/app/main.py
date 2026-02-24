from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Vehicle, TelemetryRecord, Alert
from .schemas import TelemetryCreate, TelemetryResponse
from .health_service import evaluate_vehicle_health
from .alerts import create_alerts
from .analytics_service import fleet_overview, vehicle_utilization

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Telemetry Platform")

@app.get("/")
def root():
    return {"message": "Vehicle Telemetry API running"}

@app.post("/ingest")
def ingest(data: TelemetryCreate, db: Session = Depends(get_db)):
    record = TelemetryRecord(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)

    health = evaluate_vehicle_health(record)
    create_alerts(data.vehicle_id, health, db)

    return {"status": "stored", "health": health}


@app.get("/vehicle/{vehicle_id}/latest", response_model=TelemetryResponse)
def get_latest(vehicle_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.vehicle_id == vehicle_id)
        .order_by(TelemetryRecord.timestamp.desc())
        .first()
    )
    return record

@app.get("/vehicle/{vehicle_id}/health")
def get_health(vehicle_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.vehicle_id == vehicle_id)
        .order_by(TelemetryRecord.timestamp.desc())
        .first()
    )
    return evaluate_vehicle_health(record)

@app.get("/vehicle/{vehicle_id}/history")
def get_history(vehicle_id: int, db: Session = Depends(get_db)):
    return (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.vehicle_id == vehicle_id)
        .order_by(TelemetryRecord.timestamp.desc())
        .limit(50)
        .all()
    )

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).all()

@app.get("/alerts/{vehicle_id}")
def get_vehicle_alerts(vehicle_id: int, db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.vehicle_id == vehicle_id).all()

@app.get("/analytics/fleet-overview")
def get_fleet_overview(db: Session = Depends(get_db)):
    return fleet_overview(db)

@app.get("/analytics/utilization/{vehicle_id}")
def get_utilization(vehicle_id: int, db: Session = Depends(get_db)):
    return vehicle_utilization(vehicle_id, db)
