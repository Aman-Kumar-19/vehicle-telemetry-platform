from sqlalchemy.orm import Session
from .models import Alert

def create_alerts(vehicle_id, health_result, db: Session):
    if health_result["status"] == "healthy":
        return

    for issue, severity in health_result["details"]:
        alert = Alert(
            vehicle_id=vehicle_id,
            alert_type=issue,
            severity=severity
        )
        db.add(alert)

    db.commit()
