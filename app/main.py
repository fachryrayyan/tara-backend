import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_mqtt import FastMQTT, MQTTConfig
from app.routers.sensor import manager  # Import WebSocket manager
import os
from dotenv import load_dotenv

from app.database import init_db
from app.models.sensor import SensorData
from app.routers import sensor, auth  # Import router auth

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()

app = FastAPI(title="Tara Backend - OAuth2 Protected API", lifespan=lifespan)

app.include_router(auth.router)    # Endpoint /auth/register dan /auth/login
app.include_router(sensor.router)  # Endpoint /sensor/

# 1. Konfigurasi MQTT untuk HiveMQ Cloud
mqtt_config = MQTTConfig(
    host=os.getenv("MQTT_HOST"),  # Ganti dengan Host Cluster HiveMQ Cloud kamu
    port=int(os.getenv("MQTT_PORT")),                                # Port standar SSL/TLS
    username=os.getenv("MQTT_USERNAME"),             # Username yang dibuat di HiveMQ Cloud
    password=os.getenv("MQTT_PASSWORD"),         # Password yang dibuat di HiveMQ Cloud
    ssl=True,                                 # Wajib True untuk HiveMQ Cloud
    keepalive=60
)

fast_mqtt = FastMQTT(config=mqtt_config)

# 2. PASTIIN BARIS INI ADA! (Ini yang mendaftarkan endpoint ke Swagger)
app.include_router(sensor.router)

@fast_mqtt.on_connect()
def connect_handler(client, flags, rc, properties):
    print(">>> KONEKSI KE HIVEMQ BERHASIL! <<<")
    # Daftarkan subscription saat koneksi terbentuk
    fast_mqtt.client.subscribe("tara/sensor")

@fast_mqtt.subscribe("tara/sensor")
async def message_handler(client, topic, payload, qos, properties):
    print("=== PESAN DITERIMA DARI HIVEMQ ===")
    try:
        # Decode payload JSON
        data_dict = json.loads(payload.decode())
        print(f"Data Payload: {data_dict}")

        # Simpan ke MongoDB via Beanie
        sensor_entry = SensorData(**data_dict)
        await sensor_entry.insert()
        print("-> Berhasil disimpan ke MongoDB!")

    except json.JSONDecodeError:
        print("-> Error: Format payload bukan JSON yang valid!")
    except Exception as e:
        print("-> Error simpan ke MongoDB:", e)