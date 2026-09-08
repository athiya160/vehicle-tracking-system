from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Vehicle Tracking System API"
    API_V1_STR: str = ""
    
    # PostgreSQL / Database
    DATABASE_URL: str = "postgresql://postgres:postgrespassword@localhost:5432/vehicle_tracker"
    
    # JWT Security
    SECRET_KEY: str = "supersecretjwtkeyforvehicletrackingassessment2026!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # MQTT Broker Configuration
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_TOPIC: str = "vehicles/+/gps"
    MQTT_CLIENT_ID: str = "fastapi_vehicle_tracking_server"
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
