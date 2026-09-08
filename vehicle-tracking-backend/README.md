# 🚌 Vehicle Tracking System - Backend

Production-ready backend API service for real-time bus and fleet telemetry tracking, powered by **FastAPI**, **PostgreSQL**, **Eclipse Mosquitto (MQTT)**, and **Docker Compose**.

---

## 🏗️ Architecture & Data Pipeline

```text
                     ┌─────────────────────┐
                     │   GPS Simulator     │
                     │  (BUS-001/BUS-002)  │
                     └──────────┬──────────┘
                                │ MQTT publish (`vehicles/{id}/gps`)
                                ▼
                     ┌─────────────────────┐
                     │   Mosquitto Broker  │
                     │     (Port 1883)     │
                     └──────────┬──────────┘
                                │ MQTT subscribe (`vehicles/+/gps`)
                                ▼
┌──────────────┐       ┌─────────────────────┐
│ Flutter App  │◄─────►│   FastAPI Backend   │
│ (flutter_map │ REST  │  - Auth (JWT/Bcrypt)│
│  + BLoC)     │ (8000)│  - Strict Authz     │
└──────────────┘       │  - Live & History   │
                       └──────────┬──────────┘
                                  │ SQLAlchemy ORM
                                  ▼
                       ┌─────────────────────┐
                       │   PostgreSQL DB     │
                       │  - users            │
                       │  - routes           │
                       │  - vehicles         │
                       │  - gps_tracking     │
                       └─────────────────────┘
```

---

## 🔒 Strict Backend Authorization Model

Route and vehicle assignments are **strictly validated on the backend** at the dependency level. Clients cannot access telemetry for vehicles or routes they do not own:

```text
JWT Bearer Token
       │
       ▼
Authenticated User
  ├── route_id
  └── vehicle_id
       │
       ▼
Requested Resource (/vehicles/{id}/location or /routes/{id})
       │
  ┌────┴────────────────────────┐
  │ Matches user assignment?     │
  └────┬───────────────────┬────┘
      YES                  NO
       │                   │
       ▼                   ▼
  200 OK + Telemetry    403 Forbidden ("You are not authorized...")
```

---

## 🚀 Quick Start with Docker Compose

To start the entire backend stack (PostgreSQL, Mosquitto, FastAPI Backend, Seed data, and GPS Simulator):

```bash
docker compose up --build
```

### Services Started:
- **FastAPI Backend**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432` (`user: postgres`, `password: postgrespassword`, `db: vehicle_tracker`)
- **Mosquitto MQTT Broker**: `localhost:1883`
- **GPS Simulator**: Continuously streams realistic coordinates for `BUS-001` and `BUS-002`.

---

## 💻 Manual / Local Development Setup

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for tests)
- Eclipse Mosquitto broker

### 2. Install Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Start MQTT Broker
Option A (Local Python-based Broker - No Mosquitto installation required):
```bash
python run_local_broker.py
```
Option B (Mosquitto):
```bash
mosquitto -v
```

### 5. Seed Database
Seeds default routes, buses (`BUS-001`, `BUS-002`), and users (`usera`, `userb`):
```bash
python -m app.seed
```

### 6. Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Run GPS Simulator
```bash
python gps_simulator/simulator.py
```

---

## 👥 Default Seed Credentials

| User | Username | Password | Assigned Route | Assigned Vehicle |
| :--- | :--- | :--- | :--- | :--- |
| **User A** | `usera` | `password123` | Route A (Bangalore $\to$ Hassan) | `BUS-001` |
| **User B** | `userb` | `password123` | Route B (Bangalore $\to$ Mysore) | `BUS-002` |

---

## 📡 REST API Reference

### 🔑 Authentication
- `POST /auth/register` - Create user account
- `POST /auth/login` - Authenticate & receive JWT
- `GET /auth/me` - Authenticated user profile

### 📍 Current User Endpoints (Recommended for Mobile App)
- `GET /me/route` - Returns user's assigned route metadata & full polyline coordinates
- `GET /me/vehicle` - Returns assigned vehicle status
- `GET /me/vehicle/location` - Returns latest real-time GPS coordinate & speed
- `GET /me/vehicle/history` - Returns historical GPS breadcrumbs

### 🚌 Direct Vehicle Endpoints (Strictly Authorized)
- `GET /vehicles` - Lists user's accessible vehicles
- `GET /vehicles/{id}` - Vehicle info (*403 if unassigned*)
- `GET /vehicles/{id}/location` - Latest location (*403 if unassigned*)
- `GET /vehicles/{id}/history` - Historical telemetry (*403 if unassigned*)
- `POST /vehicles/{id}/location` - Record GPS point via REST

---

## 🧪 Automated Testing

Execute unit, integration, and security authorization test suite:

```bash
pytest
```
