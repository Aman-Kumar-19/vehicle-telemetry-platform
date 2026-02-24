
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

from ml.feature_engineering.transform import calculate_stress_score

app = FastAPI(title="Predictive Maintenance Inference Service")

MODEL_PATH = "ml/models/failure_model_v2.pkl"
model = joblib.load(MODEL_PATH)

class TelemetryInput(BaseModel):
    speed: float
    rpm: float
    fuel_level: float
    battery_temp: float

@app.get("/")
def health_check():
    return {"status": "Inference service running"}

@app.post("/predict_failure")
def predict_failure(data: TelemetryInput):

    df = pd.DataFrame([data.dict()])

    # Apply same feature engineering used in training
    df = calculate_stress_score(df)

    features = df[["speed", "rpm", "fuel_level", "battery_temp", "stress_score"]]

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
