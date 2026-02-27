from datetime import datetime
from .severity import categorize_severity


def evaluate_risk(vehicle_id: int, failure_probability: float):
    severity = categorize_severity(failure_probability)

    return {
        "vehicle_id": vehicle_id,
        "failure_probability": round(failure_probability, 3),
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat(),
    }
