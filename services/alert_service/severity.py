def categorize_severity(failure_probability: float) -> str:
    if failure_probability >= 0.75:
        return "CRITICAL"
    elif failure_probability >= 0.4:
        return "MEDIUM"
    elif failure_probability >= 0.2:
        return "LOW"
    else:
        return "NORMAL"
