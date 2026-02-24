
import pandas as pd
import numpy as np

np.random.seed(42)

ROWS = 25000

def generate_data(n):
    data = []
    
    for _ in range(n):
        speed = np.random.uniform(0, 130)
        rpm = np.random.uniform(800, 6500)
        fuel = np.random.uniform(3, 100)
        temp = np.random.uniform(60, 110)
        
        stress_score = 0
        
        if rpm > 5000:
            stress_score += 2
        if temp > 95:
            stress_score += 2
        if fuel < 10:
            stress_score += 1
        if speed > 110:
            stress_score += 1
        
        failure_prob = min(stress_score * 0.2, 0.95)
        failure = np.random.rand() < failure_prob
        
        data.append([
            speed,
            rpm,
            fuel,
            temp,
            stress_score,
            int(failure)
        ])
    
    return pd.DataFrame(
        data,
        columns=[
            "speed",
            "rpm",
            "fuel_level",
            "battery_temp",
            "stress_score",
            "failure"
        ]
    )

df = generate_data(ROWS)
df.to_csv("ml/training_pipeline/historical_vehicle_data.csv", index=False)

print("Dataset generated successfully with shape:", df.shape)
