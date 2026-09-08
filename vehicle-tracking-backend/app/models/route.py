from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    start_location = Column(String(100), nullable=False)
    end_location = Column(String(100), nullable=False)
    route_coordinates = Column(JSON, nullable=False, default=list)  # list of {"lat": float, "lng": float}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    vehicles = relationship("Vehicle", back_populates="route")
    users = relationship("User", back_populates="route")
