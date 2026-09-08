import json
import logging
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.database import SessionLocal
from app.schemas.gps import GPSDataCreate
from app.services.gps_service import GPSService

logger = logging.getLogger("mqtt_subscriber")
logging.basicConfig(level=logging.INFO)


class MQTTManager:
    def __init__(self):
        # Support paho-mqtt v2.0 callback api version
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=settings.MQTT_CLIENT_ID
            )
        except AttributeError:
            self.client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
            
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        rc_val = getattr(rc, "value", rc)
        if rc_val == 0:
            logger.info(f"MQTT Connected successfully to broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
            client.subscribe(settings.MQTT_TOPIC)
            logger.info(f"MQTT Subscribed to topic: {settings.MQTT_TOPIC}")
        else:
            logger.error(f"MQTT Connection failed with return code {rc}")

    def _on_disconnect(self, client, userdata, disconnect_flags=None, rc=None, properties=None):
        logger.warning(f"MQTT Disconnected from broker (rc: {rc})")

    def _on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            topic = msg.topic  # e.g., "vehicles/BUS-001/gps"
            logger.info(f"Received MQTT Message on {topic}: {payload_str}")

            parts = topic.split("/")
            if len(parts) >= 3 and parts[0] == "vehicles" and parts[2] == "gps":
                vehicle_number = parts[1]
            else:
                vehicle_number = None

            data = json.loads(payload_str)
            if not vehicle_number:
                vehicle_number = data.get("vehicle_id") or data.get("vehicle_number")

            if not vehicle_number:
                logger.warning("No vehicle identifier found in topic or payload")
                return

            timestamp_str = data.get("timestamp")
            if timestamp_str:
                try:
                    ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                except Exception:
                    ts = datetime.now(timezone.utc)
            else:
                ts = datetime.now(timezone.utc)

            gps_payload = GPSDataCreate(
                latitude=float(data["latitude"]),
                longitude=float(data["longitude"]),
                speed=float(data.get("speed", 0.0)),
                timestamp=ts
            )

            # Insert into database in a fresh session
            db = SessionLocal()
            try:
                GPSService.record_gps_data(db, vehicle_number, gps_payload)
                logger.info(f"Recorded GPS coordinate for {vehicle_number}: ({gps_payload.latitude}, {gps_payload.longitude})")
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error processing MQTT message on topic {msg.topic}: {str(e)}", exc_info=True)

    def start(self):
        try:
            logger.info(f"Attempting connection to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}...")
            self.client.connect_async(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            logger.warning(f"Could not connect to MQTT broker on startup: {e}. Live subscriber loop disabled.")

    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT Client stopped")
        except Exception as e:
            logger.error(f"Error stopping MQTT Client: {e}")


mqtt_manager = MQTTManager()
