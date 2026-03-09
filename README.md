# 🚗 Vehicle Telemetry Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Status](https://img.shields.io/badge/Project-Active-success)
![Architecture](https://img.shields.io/badge/Architecture-Microservice--Inspired-orange)

A production-style backend system that simulates fleet telemetry, analyzes vehicle health, predicts failure risk, and generates intelligent alerts.

This project demonstrates **telemetry ingestion, predictive analytics, alerting systems, and observability patterns** used in modern fleet platforms.

---

# 📌 Project Overview

The platform simulates vehicle telemetry data and processes it through a pipeline consisting of:

1. Telemetry generation
2. API ingestion
3. Data persistence
4. Health evaluation
5. Risk inference
6. Alert generation

This mirrors real-world fleet management and predictive maintenance systems.

----
# 📁 Project Structure
```
vehicle-telemetry-platform
│
├── app/
│ ├── main.py                      # FastAPI application entry point
│ ├── database.py                  # Database connection and session management
│ ├── models.py                    # SQLAlchemy database models
│ ├── schemas.py                   # Pydantic request/response schemas
│ ├── alerts.py                    # Alert creation utilities
│ ├── analytics_service.py         # Fleet analytics logic
│ ├── health_service.py            # Vehicle health evaluation logic
│ ├── logging_config.py            # Structured logging configuration
│ └── simulator.py                 # API simulator helper
│
├── services/
│ ├── telemetry_simulator.py       # Generates realistic vehicle telemetry
│ │
│ ├── inference_service/
│ │ └── main.py                    # ML inference microservice
│ │
│ └── alert_service/
│ ├── init.py
│ ├── alert_engine.py              # Intelligent alert processing
│ ├── risk_evaluator.py            # Risk score calculation
│ └── severity.py                  # Severity classification (Low/Medium/Critical)
│
├── ml/
│ ├── feature_engineering/
│ │ └── transform.py               # Feature transformation pipeline
│ │
│ ├── models/
│ │ ├── failure_model_v1.pkl       # Initial ML model
│ │ ├── failure_model_v2.pkl       # Improved ML model
│ │ ├── metadata_v2.json           # Model metadata
│ │ └── metrics_v1.json            # Training metrics
│ │
│ └── training_pipeline/
│ ├── config.json                  # Training configuration
│ ├── generate_dataset.py          # Dataset generation script
│ ├── historical_vehicle_data.csv
│ └── train.py                     # Model training pipeline
│
├── Dockerfile                     # Container build instructions
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignored files
├── inference.log                  # Inference service logs
└── README.md                      # Project documentation
```

---

# 🏗 System Architecture

```mermaid
flowchart TD

A[Telemetry Simulator] --> B[Ingestion API]
B --> C[(Database)]
C --> D[Inference Service]
D --> E[Alert Engine]

```

---

# 🔄 Data Flow
```mermaid
sequenceDiagram

participant Simulator
participant API
participant DB
participant Inference
participant Alerts

Simulator->>API: Generate telemetry
API->>DB: Store telemetry record
API->>Inference: Evaluate vehicle health
Inference->>Alerts: Compute risk score
Alerts->>DB: Store alert if risk detected
```
-----

# 🚀 Deployment Architecture
```mermaid
flowchart LR

Client[Client / Dashboard]
Client --> API[FastAPI Backend]

API --> Simulator[Telemetry Simulator]
API --> Alerts[Alert Engine]
API --> DB[(Database)]
```
----
## 🚀 Quick Start

### 1. Clone the repository
```text
git clone https://github.com/Aman-Kumar-19/vehicle-telemetry-platform.git

cd vehicle-telemetry-platform
```
### 2. Install dependencies
```text
pip install -r requirements.txt
```
### 3. Run the API
```text
uvicorn app.main:app --reload
```
### 4. Open API docs
```
http://127.0.0.1:8000/docs
```
------------
## Environment Setup

Python version: 3.10+

Dependencies installed via:
```
pip install -r requirements.txt
```
----
## 🐳 Docker Deployment

Build image:
```
docker build -t telemetry-platform .
```
Run container:
```
docker run -p 8000:8000 telemetry-platform
```
---
# API Documentation Section
## 📡 API Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| /ingest | POST | Store telemetry |
| /simulate/{vehicle_id} | POST | Generate simulated telemetry |
| /vehicle/{vehicle_id}/health | GET | Latest vehicle health |
| /vehicle/{vehicle_id}/history | GET | Telemetry history |
| /alerts | GET | All alerts |
| /alerts/{vehicle_id} | GET | Vehicle alerts |
| /analytics/fleet-overview | GET | Fleet analytics |
| /metrics | GET | System metrics |
| /health | GET | Service health |

----
# 📊 Example API Response

Simulate Telemetry
```
POST /simulate/1
```
Example response:
```json
{
  "status": "simulated",
  "telemetry": {
    "speed": 72,
    "rpm": 3100,
    "engine_temp": 94,
    "battery_voltage": 12.4
  },
  "risk": {
    "risk_score": 0.62,
    "severity": "Medium"
  }
}
```
----
# 🧩 Component Responsibilities

## Telemetry Simulator
Location
```
services/telemetry_simulator.py
```
Responsibilities:
- Generate realistic vehicle telemetry
- Simulate RPM and speed correlation
- Simulate engine temperature behavior
- Inject probabilistic failures

## Ingestion API
Location
```
app/main.py
```
Responsibilities:
- Accept telemetry data
- Persist telemetry records
- Trigger health evaluation
- Trigger alert processing
- Provide analytics endpoints

## Database Layer
Stores two main entities.

 Telemetry Records
```
vehicle_id
speed
rpm
engine_temp
battery_voltage
timestamp
```
 Alerts
 ```
vehicle_id
severity
message
timestamp
```

## Inference Service
Responsible for evaluating vehicle health.

Modules:
```
app/health_service.py
services/alert_service/risk_evaluator.py
```
Responsibilities:
- Analyze telemetry signals
- Detect anomalies
- Generate risk score inputs

## Alert Engine

Location
```
services/alert_service/
```
Modules:
```
alert_engine.py
risk_evaluator.py
severity.py
```
Responsibilities:
- Compute risk score
- Categorize severity
- Generate alerts

Severity Levels:
```
Low
Medium
Critical
```
## 🤖 Machine Learning Pipeline

The ML system predicts potential vehicle failures using telemetry features.

Pipeline:

Dataset → Feature Engineering → Model Training → Inference Service

Location:
```
ml/training_pipeline/train.py
ml/models/failure_model_v2.pkl
```

----
## Contributing

Contributions are welcome.

1. Fork the repo
2. Create a branch
3. Submit a PR
