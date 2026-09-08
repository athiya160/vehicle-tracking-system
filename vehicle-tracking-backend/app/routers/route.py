from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.route import Route
from app.schemas.route import RouteResponse, RouteCreate
from app.services.auth_service import get_current_user, verify_route_access
from app.services.tracking_service import TrackingService

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.get("", response_model=List[RouteResponse])
def list_routes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.route_id:
        return db.query(Route).filter(Route.id == current_user.route_id).all()
    return db.query(Route).all()


@router.get("/{route_id}", response_model=RouteResponse)
def get_route_by_id(
    route: Route = Depends(verify_route_access)
):
    """
    Returns route details with coordinate points.
    Strictly verifies user's assigned route (403 Forbidden if mismatched).
    """
    return route
