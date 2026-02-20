from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Vehicle, TelemetryRecord
from .schemas import TelemetryCreate, TelemetryResponse

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
    return {"status": "stored"}

@app.get("/vehicle/{vehicle_id}/latest", response_model=TelemetryResponse)
def get_latest(vehicle_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.vehicle_id == vehicle_id)
        .order_by(TelemetryRecord.timestamp.desc())
        .first()
    )
    return record
