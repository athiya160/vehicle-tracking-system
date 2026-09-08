import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, user, route, vehicle
from app.mqtt.subscriber import mqtt_manager

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing Database Tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("Starting MQTT Subscriber Service...")
    mqtt_manager.start()
    
    yield
    
    # Shutdown actions
    logger.info("Stopping MQTT Subscriber...")
    mqtt_manager.stop()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS for Flutter Web / Desktop / Mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(route.router, prefix=settings.API_V1_STR)
app.include_router(vehicle.router, prefix=settings.API_V1_STR)


@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "Vehicle Tracking System Backend",
        "docs": "/docs",
        "mqtt_broker": f"{settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}"
    }
