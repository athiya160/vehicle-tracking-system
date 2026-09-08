from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    vehicle_number: str
    route_id: Optional[int] = None
    status: str = "active"


class VehicleResponse(BaseModel):
    id: int
    vehicle_number: str
    route_id: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
