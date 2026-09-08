import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

# Mock mqtt_manager so tests don't try connecting to a live broker
from unittest.mock import MagicMock, patch
import app.main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.gps import GPSTracking

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def mock_mqtt_and_engine():
    with patch("app.mqtt.subscriber.mqtt_manager.start"), \
         patch("app.mqtt.subscriber.mqtt_manager.stop"), \
         patch("app.main.engine", test_engine):
        yield


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    
    # Populate test seed
    route_a = Route(
        name="Route A",
        start_location="Bangalore",
        end_location="Hassan",
        route_coordinates=[{"lat": 12.9716, "lng": 77.5946}, {"lat": 13.0068, "lng": 76.1004}]
    )
    route_b = Route(
        name="Route B",
        start_location="Bangalore",
        end_location="Mysore",
        route_coordinates=[{"lat": 12.9716, "lng": 77.5946}, {"lat": 12.2958, "lng": 76.6394}]
    )
    db.add_all([route_a, route_b])
    db.commit()

    bus_1 = Vehicle(vehicle_number="BUS-001", route_id=route_a.id, status="active")
    bus_2 = Vehicle(vehicle_number="BUS-002", route_id=route_b.id, status="active")
    db.add_all([bus_1, bus_2])
    db.commit()

    user_a = User(
        username="usera",
        email="usera@example.com",
        password_hash=get_password_hash("password123"),
        route_id=route_a.id,
        vehicle_id=bus_1.id
    )
    user_b = User(
        username="userb",
        email="userb@example.com",
        password_hash=get_password_hash("password123"),
        route_id=route_b.id,
        vehicle_id=bus_2.id
    )
    db.add_all([user_a, user_b])
    db.commit()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    from app.main import app
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client
    app.dependency_overrides.clear()

