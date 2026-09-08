# 📱 Vehicle Tracking System - Flutter Mobile App

Cross-platform mobile & web client for the real-time Vehicle Tracking System, built with **Flutter 3.x**, **flutter_bloc**, **flutter_map (OpenStreetMap)**, and **Dio**.

---

## ✨ Features

- 🔐 **JWT-Based Authentication**: Seamless login with bearer token persistence and auto-login.
- 📋 **Personalized Dashboard**: Displays current user assignment, assigned route, vehicle status, and live telemetry.
- 🗺️ **Live Interactive Map**: OpenStreetMap tiles with complete route polylines and live moving bus markers (no paid Google Maps API key required).
- ⏱️ **Real-Time Polling Engine**: Automatically updates live GPS coordinates, vehicle speed, and timestamp every 4 seconds.
- 🛡️ **Security Verification**: In-app button to test unauthorized vehicle access and verify that the backend returns `403 Forbidden`.
- ⚡ **Demo Quick-Fill Accounts**: One-tap login buttons for **User A** and **User B** for quick evaluator testing.

---

## 🏗️ Architecture

The app adheres to Clean Architecture and Bloc pattern:

```text
lib/
├── core/
│   ├── constants/       # API endpoints & dynamic base URL configuration
│   ├── network/         # Dio client with JWT interceptor
│   ├── storage/         # Token storage (SharedPreferences)
│   └── theme/           # Material 3 Theme palette
├── features/
│   ├── auth/            # Login, AuthBloc, user entity, auth repository
│   └── tracking/        # Dashboard, Map, TrackingBloc, GPS entities & models
├── shared/
│   └── widgets/         # StatusBadge, MetricCard, ErrorView
└── main.dart            # MultiBlocProvider setup & app entrypoint
```

---

## 🚀 Running the App

### 1. Prerequisites
- Flutter SDK 3.x+
- Backend running at `http://localhost:8000` (or via Docker Compose)

### 2. Install Dependencies
```bash
flutter pub get
```

### 3. Run on Chrome / Web
```bash
flutter run -d chrome
```

### 4. Run on Physical Android Device
Connect device via USB with USB Debugging enabled, then forward port:
```bash
adb reverse tcp:8000 tcp:8000
flutter run -d <DEVICE_ID>
```

Or specify your PC's Wi-Fi / LAN IP dynamically at runtime:
```bash
flutter run -d <DEVICE_ID> --dart-define=API_BASE_URL=http://<YOUR_PC_LAN_IP>:8000
```

### 5. Run on Windows Desktop
```bash
flutter run -d windows
```

---

## 🧪 Testing

Run Flutter unit and entity tests:

```bash
flutter test
```

---

## 👥 Demo Test Accounts

| Account | Username | Password | Assigned Route | Assigned Vehicle |
| :--- | :--- | :--- | :--- | :--- |
| **User A** | `usera` | `password123` | Route A (Bangalore $\to$ Hassan) | `BUS-001` |
| **User B** | `userb` | `password123` | Route B (Bangalore $\to$ Mysore) | `BUS-002` |
