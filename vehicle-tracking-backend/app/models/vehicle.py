from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String(50), unique=True, index=True, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    status = Column(String(20), default="active", nullable=False)  # active, inactive, maintenance
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    route = relationship("Route", back_populates="vehicles")
    users = relationship("User", back_populates="vehicle")
    gps_records = relationship("GPSTracking", back_populates="vehicle", cascade="all, delete-orphan")
