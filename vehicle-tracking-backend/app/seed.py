import logging
from datetime import datetime, timezone, timedelta
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.gps import GPSTracking

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

ROUTE_A_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 12.9854, "lng": 77.5385}, # Rajajinagar
    {"lat": 13.0035, "lng": 77.4782}, # Nelamangala Toll
    {"lat": 13.0076, "lng": 77.1011}, # Kunigal Bypass
    {"lat": 12.9822, "lng": 76.7214}, # Channarayapatna
    {"lat": 13.0068, "lng": 76.1004}, # Hassan City
]

ROUTE_B_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 12.8711, "lng": 77.4560}, # Kengeri
    {"lat": 12.7163, "lng": 77.2813}, # Bidadi
    {"lat": 12.5960, "lng": 77.0422}, # Ramanagara
    {"lat": 12.5230, "lng": 76.8970}, # Channapatna
    {"lat": 12.4172, "lng": 76.6948}, # Mandya
    {"lat": 12.2958, "lng": 76.6394}, # Mysore Suburb
]

ROUTE_C_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 13.0035, "lng": 77.4782}, # Nelamangala
    {"lat": 13.0068, "lng": 76.1004}, # Hassan City
    {"lat": 12.8950, "lng": 75.7876}, # Sakleshpur
    {"lat": 12.8703, "lng": 75.2070}, # Bantwal
    {"lat": 12.9141, "lng": 74.8560}, # Mangalore City
]

ROUTE_D_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 12.8452, "lng": 77.6602}, # Electronic City
    {"lat": 12.7409, "lng": 77.8253}, # Hosur
    {"lat": 12.5266, "lng": 78.2140}, # Krishnagiri
    {"lat": 12.9165, "lng": 79.1325}, # Vellore
    {"lat": 12.9784, "lng": 79.9723}, # Sriperumbudur
    {"lat": 13.0827, "lng": 80.2707}, # Chennai Central
]

ROUTE_E_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 13.3409, "lng": 77.1010}, # Tumkur
    {"lat": 14.2251, "lng": 76.3980}, # Chitradurga
    {"lat": 14.4644, "lng": 75.9218}, # Davanagere
    {"lat": 14.7952, "lng": 75.3991}, # Haveri
    {"lat": 15.3647, "lng": 75.1240}, # Hubli Junction
]

ROUTE_F_COORDS = [
    {"lat": 12.9716, "lng": 77.5946}, # Bangalore Majestic
    {"lat": 12.7409, "lng": 77.8253}, # Hosur
    {"lat": 12.1277, "lng": 78.1579}, # Dharmapuri
    {"lat": 11.6643, "lng": 78.1460}, # Salem
    {"lat": 11.3410, "lng": 77.7172}, # Erode
    {"lat": 11.0168, "lng": 76.9558}, # Coimbatore Gandhipuram
]


def seed_database():
    logger.info("Initializing tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Route definitions config
        routes_config = [
            ("Route A", "Bangalore to Hassan Express", "Bangalore", "Hassan", ROUTE_A_COORDS, "BUS-001", "usera", "usera@example.com"),
            ("Route B", "Bangalore to Mysore Superfast", "Bangalore", "Mysore", ROUTE_B_COORDS, "BUS-002", "userb", "userb@example.com"),
            ("Route C", "Bangalore to Mangalore Express", "Bangalore", "Mangalore", ROUTE_C_COORDS, "BUS-003", "userc", "userc@example.com"),
            ("Route D", "Bangalore to Chennai Intercity", "Bangalore", "Chennai", ROUTE_D_COORDS, "BUS-004", "userd", "userd@example.com"),
            ("Route E", "Bangalore to Hubli-Dharwad Superfast", "Bangalore", "Hubli", ROUTE_E_COORDS, "BUS-005", "usere", "usere@example.com"),
            ("Route F", "Bangalore to Coimbatore Express", "Bangalore", "Coimbatore", ROUTE_F_COORDS, "BUS-006", "userf", "userf@example.com"),
        ]

        now = datetime.now(timezone.utc)

        for r_name, r_desc, r_start, r_end, r_coords, v_num, u_name, u_email in routes_config:
            # 1. Seed or get Route
            route = db.query(Route).filter(Route.name == r_name).first()
            if not route:
                route = Route(
                    name=r_name,
                    description=r_desc,
                    start_location=r_start,
                    end_location=r_end,
                    route_coordinates=r_coords
                )
                db.add(route)
                db.commit()
                db.refresh(route)
                logger.info(f"Created {r_name}")
            else:
                route.route_coordinates = r_coords
                route.description = r_desc
                db.commit()

            # 2. Seed or get Vehicle
            vehicle = db.query(Vehicle).filter(Vehicle.vehicle_number == v_num).first()
            if not vehicle:
                vehicle = Vehicle(
                    vehicle_number=v_num,
                    route_id=route.id,
                    status="active"
                )
                db.add(vehicle)
                db.commit()
                db.refresh(vehicle)
                logger.info(f"Created Vehicle {v_num}")

            # 3. Seed or get User
            user = db.query(User).filter(User.username == u_name).first()
            if not user:
                user = User(
                    username=u_name,
                    email=u_email,
                    password_hash=get_password_hash("password123"),
                    route_id=route.id,
                    vehicle_id=vehicle.id
                )
                db.add(user)
                db.commit()
                logger.info(f"Created User {u_name} (assigned {r_name} & {v_num})")

            # 4. Seed Initial Telemetry
            if db.query(GPSTracking).filter(GPSTracking.vehicle_id == vehicle.id).count() == 0:
                for idx, pt in enumerate(r_coords[:3]):
                    gps = GPSTracking(
                        vehicle_id=vehicle.id,
                        latitude=pt["lat"],
                        longitude=pt["lng"],
                        speed=40.0 + (idx * 3.5),
                        timestamp=now - timedelta(minutes=(3 - idx) * 5)
                    )
                    db.add(gps)
                db.commit()
                logger.info(f"Seeded initial GPS records for {v_num}")

        logger.info("Database seeding completed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
