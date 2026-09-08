from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GPSDataCreate(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    speed: float = Field(default=0.0, ge=0.0)
    timestamp: Optional[datetime] = None


class GPSLocationResponse(BaseModel):
    vehicle_id: int
    vehicle_number: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    class Config:
        from_attributes = True


class GPSHistoryItem(BaseModel):
    id: int
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    class Config:
        from_attributes = True
