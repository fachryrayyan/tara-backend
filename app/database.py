import motor.motor_asyncio
from beanie import init_beanie
from app.models.sensor import SensorData
from app.models.user import User  # <-- Import User


MONGO_DETAILS = "mongodb+srv://fachryrayyan30_db_user:ClOVXiiMV1KivyFX@test.xzmyn4j.mongodb.net/"

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    await init_beanie(
        database=client.tara_db, 
        document_models=[SensorData, User]  # <-- Daftarkan di sini
    )