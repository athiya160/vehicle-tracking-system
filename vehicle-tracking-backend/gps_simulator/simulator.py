import time
import json
import random
import os
import logging
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gps_simulator")

# Simulated Route Waypoints
BUS_001_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (12.9800, 77.5600),
    (12.9854, 77.5385),  # Rajajinagar
    (12.9950, 77.5100),
    (13.0035, 77.4782),  # Nelamangala Toll
    (13.0050, 77.3000),
    (13.0076, 77.1011),  # Kunigal Bypass
    (12.9950, 76.9000),
    (12.9822, 76.7214),  # Channarayapatna
    (12.9900, 76.4000),
    (13.0068, 76.1004),  # Hassan City
]

BUS_002_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (12.9100, 77.5200),
    (12.8711, 77.4560),  # Kengeri
    (12.7800, 77.3500),
    (12.7163, 77.2813),  # Bidadi
    (12.6500, 77.1500),
    (12.5960, 77.0422),  # Ramanagara
    (12.5230, 76.8970),  # Channapatna
    (12.4800, 76.7800),
    (12.4172, 76.6948),  # Mandya
    (12.3500, 76.6600),
    (12.2958, 76.6394),  # Mysore Suburb
]

BUS_003_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (13.0035, 77.4782),  # Nelamangala
    (13.0068, 76.1004),  # Hassan
    (12.8950, 75.7876),  # Sakleshpur
    (12.8703, 75.2070),  # Bantwal
    (12.9141, 74.8560),  # Mangalore
]

BUS_004_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (12.8452, 77.6602),  # Electronic City
    (12.7409, 77.8253),  # Hosur
    (12.5266, 78.2140),  # Krishnagiri
    (12.9165, 79.1325),  # Vellore
    (12.9784, 79.9723),  # Sriperumbudur
    (13.0827, 80.2707),  # Chennai Central
]

BUS_005_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (13.3409, 77.1010),  # Tumkur
    (14.2251, 76.3980),  # Chitradurga
    (14.4644, 75.9218),  # Davanagere
    (14.7952, 75.3991),  # Haveri
    (15.3647, 75.1240),  # Hubli Junction
]

BUS_006_PATH = [
    (12.9716, 77.5946),  # Bangalore Majestic
    (12.7409, 77.8253),  # Hosur
    (12.1277, 78.1579),  # Dharmapuri
    (11.6643, 78.1460),  # Salem
    (11.3410, 77.7172),  # Erode
    (11.0168, 76.9558),  # Coimbatore
]

FLEET = [
    {"vehicle_number": "BUS-001", "path": BUS_001_PATH, "idx": 0, "base_speed": 42.0},
    {"vehicle_number": "BUS-002", "path": BUS_002_PATH, "idx": 0, "base_speed": 48.0},
    {"vehicle_number": "BUS-003", "path": BUS_003_PATH, "idx": 0, "base_speed": 45.0},
    {"vehicle_number": "BUS-004", "path": BUS_004_PATH, "idx": 0, "base_speed": 55.0},
    {"vehicle_number": "BUS-005", "path": BUS_005_PATH, "idx": 0, "base_speed": 52.0},
    {"vehicle_number": "BUS-006", "path": BUS_006_PATH, "idx": 0, "base_speed": 50.0},
]


def create_mqtt_client(broker_host: str, broker_port: int) -> mqtt.Client:
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"gps_simulator_{random.randint(1000, 9999)}"
        )
    except AttributeError:
        client = mqtt.Client(client_id=f"gps_simulator_{random.randint(1000, 9999)}")
    
    logger.info(f"Connecting GPS Simulator to MQTT broker at {broker_host}:{broker_port}...")
    client.connect(broker_host, broker_port, keepalive=60)
    client.loop_start()
    return client


def run_simulator():
    broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
    broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))
    interval = float(os.getenv("SIMULATION_INTERVAL", 4.0))

    client = create_mqtt_client(broker_host, broker_port)

    logger.info(f"GPS Telemetry Simulator is running for {len(FLEET)} vehicles. Publishing updates...")

    try:
        while True:
            for bus in FLEET:
                path = bus["path"]
                idx = bus["idx"]
                v_num = bus["vehicle_number"]

                lat, lng = path[idx]
                jitter_lat = lat + random.uniform(-0.0004, 0.0004)
                jitter_lng = lng + random.uniform(-0.0004, 0.0004)
                speed = round(bus["base_speed"] + random.uniform(-5.0, 5.0), 1)

                payload = {
                    "vehicle_number": v_num,
                    "latitude": round(jitter_lat, 6),
                    "longitude": round(jitter_lng, 6),
                    "speed": speed,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

                topic = f"vehicles/{v_num}/gps"
                client.publish(topic, json.dumps(payload), qos=1)
                logger.info(f"[SIMULATOR] Published to {topic}: {payload}")

                # Advance waypoint index
                bus["idx"] = (idx + 1) % len(path)

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Stopping GPS Simulator...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run_simulator()
