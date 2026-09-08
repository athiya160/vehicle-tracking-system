# 🚍 Velocity Fleet — Full-Stack Real-Time Vehicle Tracking System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Frontend-Flutter_3.x-02569B.svg?style=flat&logo=flutter&logoColor=white)](https://flutter.dev)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL_%2F_SQLite-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT_Mosquitto-660066.svg?style=flat&logo=eclipsemosquitto&logoColor=white)](https://mosquitto.org/)
[![Docker](https://img.shields.io/badge/Container-Docker_Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Backend_Tests-11_Passed-brightgreen.svg)]()
[![Flutter Analyze](https://img.shields.io/badge/Flutter_Analyze-0_Issues-brightgreen.svg)]()

> A production-ready, full-stack vehicle tracking application featuring **MQTT-driven telemetry ingestion**, **JWT role-based authorization**, **live OpenStreetMap visualization with route polylines & historical breadcrumbs**, and dynamic **BLoC-managed Flutter frontend**.

---

## 📸 Application Screenshots

| 🔐 Login & 1-Tap Operator Auth | 📊 Live Telemetry & Speedometer |
|:---:|:---:|
| <img src="docs/screenshots/login_screen.png" width="450" alt="Login Screen"/> | <img src="docs/screenshots/dashboard_telemetry.png" width="450" alt="Live Telemetry Dashboard"/> |
| **Operator authentication with 1-tap test accounts** | **Live speed gauge, ETA, remaining distance, & ping status** |

| 🗺️ Interactive Live Map & Breadcrumbs | 🛡️ RBAC 403 Forbidden Security Check |
|:---:|:---:|
| <img src="docs/screenshots/live_map_tracking.png" width="450" alt="Live Map Tracking"/> | <img src="docs/screenshots/rbac_403_forbidden.png" width="450" alt="RBAC 403 Forbidden"/> |
| **OpenStreetMap with bus pin, polyline, and GPS history** | **Backend blocks unauthorized vehicle queries with HTTP 403** |

---

## 🎥 Video Demonstration
* **Video Walkthrough Link:** [Google Drive / Loom Video Submission Link](https://drive.google.com/) *(Add your recorded video link here)*
* **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📐 System Architecture

```mermaid
flowchart TD
    subgraph IoT_Layer["📡 IoT Simulation Layer"]
        SIM["GPS Simulator\n(simulator.py)"]
        BROKER["MQTT Broker\n(Mosquitto / Port 1883)"]
        SIM -->|Publish topic: vehicles/BUS-001/gps| BROKER
    end

    subgraph Backend_Layer["⚡ FastAPI Backend Layer (Port 8000)"]
        SUB["MQTT Subscriber Background Client"]
        ROUTER["REST API Routers\n(/auth, /me, /vehicles)"]
        SEC["JWT & RBAC Security Layer\n(Enforces HTTP 403 Forbidden)"]
        DB[(PostgreSQL / SQLite\nSQLAlchemy Engine)]

        BROKER -->|Ingest GPS Telemetry| SUB
        SUB -->|Persist Coordinates & Speed| DB
        ROUTER --> SEC
        SEC --> DB
    end

    subgraph Frontend_Layer["📱 Flutter Client Layer (Web & Mobile)"]
        BLOC["BLoC State Management"]
        DASH["Telemetry Dashboard\n(Speedometer, ETA, Distance)"]
        MAP["Interactive OpenStreetMap\n(Bus Pin, Route Polyline, Breadcrumbs)"]

        BLOC --> DASH
        BLOC --> MAP
    end

    Frontend_Layer <-->|HTTP REST / JWT Bearer Tokens| ROUTER
```

---

## 📋 Assessment Requirements Compliance Matrix

| Requirement | Implementation Details | Status |
| :--- | :--- | :---: |
| **Multiple User Login** | Secure bcrypt hashing, JWT issuance via `/auth/login`, dedicated credentials for `usera` through `userf` | ✅ Complete |
| **Relational Database** | Configured for **PostgreSQL** with automatic fallback to **SQLite** using SQLAlchemy ORM | ✅ Complete |
| **User → Route Assignment** | Relational mapping: `usera` → Route A, `userb` → Route B, `userc` → Route C, etc. | ✅ Complete |
| **User → Vehicle Assignment** | Relational mapping: `usera` → `BUS-001`, `userb` → `BUS-002`, `userc` → `BUS-003` | ✅ Complete |
| **MQTT GPS Ingestion** | Async MQTT subscriber ingesting `latitude`, `longitude`, `speed`, and `timestamp` from `vehicles/{id}/gps` | ✅ Complete |
| **Live Vehicle Location** | Polling `/me/vehicle/location` returns latest GPS coordinates and dynamic telemetry | ✅ Complete |
| **Historical GPS Breadcrumbs** | `/vehicles/{id}/history` returns complete chronological breadcrumb path | ✅ Complete |
| **Flutter Interactive Map** | OpenStreetMap (flutter_map), customized vehicle marker, planned route polyline, historical trail | ✅ Complete |
| **RBAC Security (403)** | Strict backend dependency check returns **HTTP 403 Forbidden** when querying unauthorized vehicles | ✅ Complete |
| **Bonus: Speedometer Gauge** | Dynamic analog/digital speedometer displaying real-time speed in km/h | ✅ Complete |
| **Bonus: Remaining Distance/ETA**| Haversine calculation computing remaining route distance and estimated arrival time | ✅ Complete |
| **Bonus: Docker Compose** | Multi-service `docker-compose.yml` for Mosquitto MQTT, PostgreSQL DB, and FastAPI backend | ✅ Complete |

---

## 🔑 Pre-Seeded Test Credentials

| Username | Password | Assigned Vehicle | Assigned Route | Start Point → End Point |
| :--- | :--- | :--- | :--- | :--- |
| **`usera`** | `password123` | `BUS-001` | Route A | Bangalore ➔ Mysore |
| **`userb`** | `password123` | `BUS-002` | Route B | Bangalore ➔ Chennai |
| **`userc`** | `password123` | `BUS-003` | Route C | Bangalore ➔ Mangalore |
| **`userd`** | `password123` | `BUS-004` | Route D | Bangalore ➔ Hyderabad |
| **`usere`** | `password123` | `BUS-005` | Route E | Bangalore ➔ Goa |
| **`userf`** | `password123` | `BUS-006` | Route F | Bangalore ➔ Coimbatore |

---

## 🚀 Quickstart Guide

### 1. Backend Setup & Run

```bash
cd vehicle-tracking-backend

# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Mosquitto Broker (or local broker script)
python run_local_broker.py

# 4. In a new terminal, launch the FastAPI server
python -m uvicorn app.main:app --reload

# 5. In a new terminal, run the GPS Simulator
python gps_simulator/simulator.py
```

* Swagger API Documentation: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
* Run Automated Tests:
  ```bash
  pytest -v
  ```

---

### 2. Flutter Client Setup & Run

```bash
cd vehicle-tracking-flutter

# 1. Get Flutter dependencies
flutter pub get

# 2. Run static analysis & tests
flutter analyze
flutter test

# 3. Run application (Web / Chrome)
flutter run -d chrome

# 4. Or run on Android Device / Emulator
flutter run
```

---

## 🐳 Docker Deployment (One-Click)

To launch the full backend stack (PostgreSQL + Mosquitto MQTT + FastAPI Backend) in containers:

```bash
cd vehicle-tracking-backend
docker compose up --build -d
```

---

## 🛡️ Security & Role-Based Access Control (RBAC)

The backend enforces strict authorization via FastAPI dependency injection:
* Endpoint: `GET /vehicles/{vehicle_id}/location`
* If `usera` (assigned to `BUS-001`) attempts to access `/vehicles/BUS-002/location`, the backend immediately rejects the request:
  ```json
  {
    "detail": "Unauthorized: You do not have permission to access vehicle BUS-002."
  }
  ```
  *(HTTP Status: `403 Forbidden`)*

---

## 📂 Repository Structure

```text
vehicle-tracking-system/
├── README.md                      # Master fullstack documentation
├── docs/                          # Screenshots & architecture diagrams
│   └── screenshots/
├── vehicle-tracking-backend/      # FastAPI Backend, Database, MQTT & Tests
│   ├── app/                       # Core, Models, Routers, Schemas, Services
│   ├── gps_simulator/             # Realistic route GPS generator
│   ├── mosquitto/                 # MQTT Broker configuration
│   ├── tests/                     # 11 automated pytest test cases
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── vehicle-tracking-flutter/      # Flutter Mobile & Web Application
    ├── lib/                       # BLoC, Data Models, Repositories, Screens, Widgets
    ├── test/                      # Flutter widget & unit tests
    └── pubspec.yaml               # Flutter package configuration
```
