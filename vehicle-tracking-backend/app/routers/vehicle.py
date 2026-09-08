from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleResponse, VehicleCreate
from app.schemas.gps import GPSLocationResponse, GPSHistoryItem, GPSDataCreate
from app.services.auth_service import get_current_user, verify_vehicle_access
from app.services.gps_service import GPSService
from app.services.tracking_service import TrackingService

router = APIRouter(prefix="/vehicles", tags=["Vehicles & Authorization"])


@router.get("", response_model=List[VehicleResponse])
def list_vehicles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns vehicles accessible to the user (the user's assigned vehicle or vehicles on their assigned route).
    """
    if current_user.vehicle_id:
        return db.query(Vehicle).filter(Vehicle.id == current_user.vehicle_id).all()
    elif current_user.route_id:
        return db.query(Vehicle).filter(Vehicle.route_id == current_user.route_id).all()
    return []


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(
    vehicle: Vehicle = Depends(verify_vehicle_access)
):
    """
    Requires strict backend authorization: if current_user is not assigned to this vehicle, returns 403.
    """
    return vehicle


@router.get("/{vehicle_id}/location", response_model=GPSLocationResponse)
def get_vehicle_location(
    vehicle_id: int,
    vehicle: Vehicle = Depends(verify_vehicle_access),
    db: Session = Depends(get_db)
):
    """
    Returns latest GPS location for the requested vehicle.
    Enforces strict backend authorization (403 Forbidden on unassigned vehicle).
    """
    location = GPSService.get_latest_location(db, vehicle.id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No GPS telemetry found for vehicle {vehicle.vehicle_number}"
        )
    return location


@router.get("/{vehicle_id}/history", response_model=List[GPSHistoryItem])
def get_vehicle_history(
    vehicle_id: int,
    limit: int = 100,
    vehicle: Vehicle = Depends(verify_vehicle_access),
    db: Session = Depends(get_db)
):
    """
    Returns GPS history for the requested vehicle.
    Enforces strict backend authorization (403 Forbidden on unassigned vehicle).
    """
    return GPSService.get_history(db, vehicle.id, limit=limit)


@router.post("/{vehicle_id}/location", response_model=GPSLocationResponse, status_code=status.HTTP_201_CREATED)
def record_vehicle_location_rest(
    vehicle_id: int,
    data: GPSDataCreate,
    vehicle: Vehicle = Depends(verify_vehicle_access),
    db: Session = Depends(get_db)
):
    """
    Allows recording GPS location via REST for simulation / testing purposes.
    """
    GPSService.record_gps_data(db, vehicle.id, data)
    location = GPSService.get_latest_location(db, vehicle.id)
    return location
