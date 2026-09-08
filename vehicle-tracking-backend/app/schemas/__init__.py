from app.schemas.auth import Token, TokenPayload, LoginRequest, UserRegisterRequest, UserResponse
from app.schemas.route import RouteCreate, RouteResponse
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.schemas.gps import GPSDataCreate, GPSLocationResponse, GPSHistoryItem

__all__ = [
    "Token",
    "TokenPayload",
    "LoginRequest",
    "UserRegisterRequest",
    "UserResponse",
    "RouteCreate",
    "RouteResponse",
    "VehicleCreate",
    "VehicleResponse",
    "GPSDataCreate",
    "GPSLocationResponse",
    "GPSHistoryItem",
]
