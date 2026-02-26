# services/telemetry_simulator.py

import random
from datetime import datetime


class TelemetrySimulator:
    def __init__(self):
        self.speed = 0
        self.rpm = 800
        self.engine_temp = 75
        self.battery_voltage = 12.6
        self.last_rpm = 800

    def update_speed(self):
        delta = random.uniform(-5, 8)
        self.speed = max(0, min(140, self.speed + delta))

    def calculate_rpm(self):
        gear_ratio = 40
        base_rpm = 800
        self.rpm = base_rpm + self.speed * gear_ratio
        self.rpm = min(self.rpm, 6500)

    def update_temperature(self):
        load_factor = self.rpm / 6000
        temp_rise = load_factor * 3
        cooling = 1.2
        self.engine_temp += temp_rise - cooling
        self.engine_temp = max(70, min(125, self.engine_temp))

    def update_battery(self):
        drain = random.uniform(0.0005, 0.002)
        self.battery_voltage -= drain
        self.battery_voltage = max(11.5, self.battery_voltage)

    def calculate_failure_probability(self):
        prob = 0.01

        if self.engine_temp > 110:
            prob += 0.15

        if self.rpm > 5500:
            prob += 0.1

        if abs(self.rpm - self.last_rpm) > 1500:
            prob += 0.1

        if self.battery_voltage < 11.8:
            prob += 0.1

        self.last_rpm = self.rpm
        return min(prob, 0.9)

    def generate(self):
        self.update_speed()
        self.calculate_rpm()
        self.update_temperature()
        self.update_battery()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "speed": round(self.speed, 2),
            "rpm": int(self.rpm),
            "engine_temp": round(self.engine_temp, 2),
            "battery_voltage": round(self.battery_voltage, 3),
            "failure_probability": round(self.calculate_failure_probability(), 3),
        }
