
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Predictive Maintenance Inference Service")

# Load model once at startup
MODEL_PATH = "ml/models/failure_model_v1.pkl"
model = joblib.load(MODEL_PATH)

class TelemetryInput(BaseModel):
    speed: float
    rpm: float
    fuel_level: float
    battery_temp: float
    stress_score: float

@app.get("/")
def health_check():
    return {"status": "Inference service running"}

@app.post("/predict_failure")
def predict_failure(data: TelemetryInput):
    
    features = np.array([[
        data.speed,
        data.rpm,
        data.fuel_level,
        data.battery_temp,
        data.stress_score
    ]])
    
    probability = model.predict_proba(features)[0][1]
    
    if probability > 0.75:
        risk = "HIGH"
    elif probability > 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    
    return {
        "failure_probability": round(float(probability), 4),
        "risk_level": risk
    }
