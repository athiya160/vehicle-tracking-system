from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.route import Route
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_01_UNAUTHORIZED if hasattr(status, 'HTTP_01_UNAUTHORIZED') else 401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenPayload(sub=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user


def verify_vehicle_access(vehicle_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {vehicle_id} not found"
        )
    
    # Strict Authorization Rule: User must be directly assigned to vehicle OR assigned to the vehicle's route
    is_direct_vehicle_match = (current_user.vehicle_id is not None and current_user.vehicle_id == vehicle.id)
    is_route_vehicle_match = (current_user.route_id is not None and current_user.route_id == vehicle.route_id)

    if not (is_direct_vehicle_match or is_route_vehicle_match):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this vehicle"
        )
    return vehicle


def verify_route_access(route_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Route:
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    if current_user.route_id != route.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this route"
        )
    return route
