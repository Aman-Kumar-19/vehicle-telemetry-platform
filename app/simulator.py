import random
import time
import requests

API_URL = "http://127.0.0.1:8000/ingest"

def generate_data(vehicle_id=1):
    return {
        "vehicle_id": vehicle_id,
        "speed": random.uniform(0, 120),
        "rpm": random.uniform(800, 5000),
        "fuel_level": random.uniform(5, 100),
        "battery_temp": random.uniform(60, 95)
    }

def start_simulation(vehicle_count=5):
    while True:
        for vid in range(1, vehicle_count + 1):
            data = generate_data(vid)
            try:
                requests.post(API_URL, json=data)
                print(f"Vehicle {vid} →", data)
            except:
                print("API not ready")
        time.sleep(1)
