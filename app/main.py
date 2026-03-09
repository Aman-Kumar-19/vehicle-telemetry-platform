import time
import logging
from fastapi import Request
from app.logging_config import setup_logging, get_logger
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Vehicle, TelemetryRecord, Alert
from .schemas import TelemetryCreate, TelemetryResponse
from .health_service import evaluate_vehicle_health
from .alerts import create_alerts
from .analytics_service import fleet_overview, vehicle_utilization
from services.telemetry_simulator import TelemetrySimulator
from services.alert_service.alert_engine import process_inference

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Telemetry Platform")
# Initialize Telemetry Simulator (Phase 3)
simulator = TelemetrySimulator()
setup_logging()
logger = get_logger("vehicle-platform")

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

@app.post("/simulate/{vehicle_id}")
def simulate_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    # Generate realistic telemetry
    simulated_data = simulator.generate()

    # Convert into DB model
    record = TelemetryRecord(
        vehicle_id=vehicle_id,
        speed=simulated_data["speed"],
        rpm=simulated_data["rpm"],
        engine_temp=simulated_data["engine_temp"],
        battery_voltage=simulated_data["battery_voltage"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # Evaluate health
    health = evaluate_vehicle_health(record)

    # Phase 4: Intelligent Alert Engine
    alert_result = process_inference(
    vehicle_id,
    simulated_data["failure_probability"]
    )

    return {
      "status": "simulated",
      "telemetry": simulated_data,
      "health": health,
      "alert_engine": alert_result
      }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(
        f"Completed: {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Duration: {duration}ms"
    )
    return response


@app.get("/metrics")
def metrics():
    logger.info("Metrics endpoint accessed")
    return {
        "total_requests": request_count
    }


# -----------------------------
# ✅ Health Check Endpoint
# -----------------------------
@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "service": "vehicle-telemetry-platform"
    }
