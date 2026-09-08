from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.route import RouteResponse
from app.schemas.vehicle import VehicleResponse
from app.schemas.gps import GPSLocationResponse, GPSHistoryItem
from app.services.auth_service import get_current_user
from app.services.tracking_service import TrackingService
from app.services.gps_service import GPSService

router = APIRouter(prefix="/me", tags=["Current User Assignments & Tracking"])


@router.get("/route", response_model=RouteResponse)
def get_my_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    route = TrackingService.get_user_route(db, current_user)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No route assigned to current user"
        )
    return route


@router.get("/vehicle", response_model=VehicleResponse)
def get_my_vehicle(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = TrackingService.get_user_vehicle(db, current_user)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vehicle assigned to current user"
        )
    return vehicle


@router.get("/vehicle/location", response_model=GPSLocationResponse)
def get_my_vehicle_location(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = TrackingService.get_user_vehicle(db, current_user)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vehicle assigned to current user"
        )
    
    location = GPSService.get_latest_location(db, vehicle.id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No GPS telemetry data available yet for vehicle '{vehicle.vehicle_number}'"
        )
    return location


@router.get("/vehicle/history", response_model=List[GPSHistoryItem])
def get_my_vehicle_history(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    vehicle = TrackingService.get_user_vehicle(db, current_user)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vehicle assigned to current user"
        )
    
    return GPSService.get_history(db, vehicle.id, limit=limit)
