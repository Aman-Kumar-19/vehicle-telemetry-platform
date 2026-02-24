# Vehicle Telemetry Data Platform

Backend system that simulates vehicle sensor data and exposes analytics APIs.

## Features
- Simulated CAN bus telemetry
- FastAPI ingestion service
- SQLite storage
- Latest vehicle state API

## Tech Stack
FastAPI + SQLAlchemy + SQLite + Python

## Endpoints
POST /ingest
GET /vehicle/{id}/latest
