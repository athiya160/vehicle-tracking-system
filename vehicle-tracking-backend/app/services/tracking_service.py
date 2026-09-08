from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.route import Route
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.route import RouteCreate, RouteResponse
from app.schemas.vehicle import VehicleCreate, VehicleResponse


class TrackingService:
    @staticmethod
    def get_user_route(db: Session, user: User) -> Optional[Route]:
        if not user.route_id:
            return None
        return db.query(Route).filter(Route.id == user.route_id).first()

    @staticmethod
    def get_user_vehicle(db: Session, user: User) -> Optional[Vehicle]:
        if user.vehicle_id:
            return db.query(Vehicle).filter(Vehicle.id == user.vehicle_id).first()
        elif user.route_id:
            # Fallback to the first vehicle assigned to this route
            return db.query(Vehicle).filter(Vehicle.route_id == user.route_id).first()
        return None

    @staticmethod
    def create_route(db: Session, route_in: RouteCreate) -> Route:
        route = Route(
            name=route_in.name,
            description=route_in.description,
            start_location=route_in.start_location,
            end_location=route_in.end_location,
            route_coordinates=route_in.route_coordinates
        )
        db.add(route)
        db.commit()
        db.refresh(route)
        return route

    @staticmethod
    def create_vehicle(db: Session, vehicle_in: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(
            vehicle_number=vehicle_in.vehicle_number,
            route_id=vehicle_in.route_id,
            status=vehicle_in.status
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle
