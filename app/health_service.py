def evaluate_vehicle_health(record):
    issues = []

    if record.battery_temp > 90:
        issues.append(("battery_overheat", "high"))

    if record.fuel_level < 10:
        issues.append(("low_fuel", "medium"))

    if record.rpm > 5500:
        issues.append(("engine_stress", "high"))

    if not issues:
        return {"status": "healthy", "issues": []}

    return {
        "status": "warning",
        "issues": [issue[0] for issue in issues],
        "details": issues
    }
