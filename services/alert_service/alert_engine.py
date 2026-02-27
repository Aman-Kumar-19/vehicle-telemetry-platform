from .risk_evaluator import evaluate_risk


def process_inference(vehicle_id: int, failure_probability: float):
    """
    Main entry point for alert engine.
    """
    risk_record = evaluate_risk(vehicle_id, failure_probability)

    if risk_record["severity"] in ["LOW", "MEDIUM", "CRITICAL"]:
        return {
            "alert_triggered": True,
            "risk": risk_record
        }

    return {
        "alert_triggered": False,
        "risk": risk_record
    }
