import motor.motor_asyncio
from beanie import init_beanie
from app.models.sensor import SensorData
from app.models.user import User  # <-- Import User
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    await init_beanie(
        database=client.tara_db, 
        document_models=[SensorData, User]  # <-- Daftarkan di sini
    )