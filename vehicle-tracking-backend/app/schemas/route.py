from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class LatLng(BaseModel):
    lat: float
    lng: float


class RouteCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_location: str
    end_location: str
    route_coordinates: List[Dict[str, float]] = []


class RouteResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_location: str
    end_location: str
    route_coordinates: List[Dict[str, Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True
