from datetime import datetime, timezone
from app.services.gps_service import GPSService
from app.schemas.gps import GPSDataCreate
from app.models.vehicle import Vehicle


def test_gps_service_recording_and_retrieval(db_session):
    bus1 = db_session.query(Vehicle).filter(Vehicle.vehicle_number == "BUS-001").first()

    # Record 3 GPS points
    points = [
        (12.9716, 77.5946, 30.0),
        (12.9854, 77.5385, 45.0),
        (13.0035, 77.4782, 50.0),
    ]

    for lat, lng, speed in points:
        GPSService.record_gps_data(
            db_session,
            bus1.id,
            GPSDataCreate(latitude=lat, longitude=lng, speed=speed, timestamp=datetime.now(timezone.utc))
        )

    # Latest location check
    latest = GPSService.get_latest_location(db_session, bus1.id)
    assert latest is not None
    assert latest.latitude == 13.0035
    assert latest.longitude == 77.4782
    assert latest.speed == 50.0
    assert latest.vehicle_number == "BUS-001"

    # History check
    history = GPSService.get_history(db_session, bus1.id)
    assert len(history) == 3
    assert history[0].latitude == 12.9716
    assert history[-1].latitude == 13.0035


def test_gps_service_recording_by_vehicle_number_string(db_session):
    # Tests that MQTT subscriber can record by string vehicle number e.g. "BUS-002"
    GPSService.record_gps_data(
        db_session,
        "BUS-002",
        GPSDataCreate(latitude=12.2958, longitude=76.6394, speed=60.0)
    )

    bus2 = db_session.query(Vehicle).filter(Vehicle.vehicle_number == "BUS-002").first()
    latest = GPSService.get_latest_location(db_session, bus2.id)
    assert latest is not None
    assert latest.latitude == 12.2958
    assert latest.speed == 60.0
