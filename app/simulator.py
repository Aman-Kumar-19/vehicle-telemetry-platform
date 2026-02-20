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

def start_simulation():
    while True:
        data = generate_data()
        try:
            requests.post(API_URL, json=data)
            print("Sent:", data)
        except:
            print("API not ready")
        time.sleep(1)
