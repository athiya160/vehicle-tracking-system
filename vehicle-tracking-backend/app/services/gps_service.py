from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.gps import GPSTracking
from app.models.vehicle import Vehicle
from app.schemas.gps import GPSDataCreate, GPSLocationResponse, GPSHistoryItem


class GPSService:
    @staticmethod
    def record_gps_data(db: Session, vehicle_identifier: str | int, data: GPSDataCreate) -> GPSTracking:
        """
        Record a GPS coordinate for a vehicle (identified either by database ID or vehicle_number string).
        """
        if isinstance(vehicle_identifier, int):
            vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_identifier).first()
        else:
            vehicle = db.query(Vehicle).filter(Vehicle.vehicle_number == str(vehicle_identifier)).first()
        
        if not vehicle:
            raise ValueError(f"Vehicle '{vehicle_identifier}' not found in database")
        
        timestamp = data.timestamp or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
            
        gps_entry = GPSTracking(
            vehicle_id=vehicle.id,
            latitude=data.latitude,
            longitude=data.longitude,
            speed=data.speed,
            timestamp=timestamp
        )
        db.add(gps_entry)
        db.commit()
        db.refresh(gps_entry)
        return gps_entry

    @staticmethod
    def get_latest_location(db: Session, vehicle_id: int) -> Optional[GPSLocationResponse]:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return None

        latest_record = (
            db.query(GPSTracking)
            .filter(GPSTracking.vehicle_id == vehicle_id)
            .order_by(desc(GPSTracking.timestamp), desc(GPSTracking.id))
            .first()
        )
        if not latest_record:
            return None

        return GPSLocationResponse(
            vehicle_id=vehicle.id,
            vehicle_number=vehicle.vehicle_number,
            latitude=latest_record.latitude,
            longitude=latest_record.longitude,
            speed=latest_record.speed,
            timestamp=latest_record.timestamp,
        )

    @staticmethod
    def get_history(db: Session, vehicle_id: int, limit: int = 100) -> List[GPSHistoryItem]:
        records = (
            db.query(GPSTracking)
            .filter(GPSTracking.vehicle_id == vehicle_id)
            .order_by(desc(GPSTracking.timestamp), desc(GPSTracking.id))
            .limit(limit)
            .all()
        )
        return [
            GPSHistoryItem(
                id=r.id,
                latitude=r.latitude,
                longitude=r.longitude,
                speed=r.speed,
                timestamp=r.timestamp
            )
            for r in reversed(records)  # return chronological order
        ]
