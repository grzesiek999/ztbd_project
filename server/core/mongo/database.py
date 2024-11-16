from motor.motor_asyncio import AsyncIOMotorClient
import os

# client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
# db = client.get_database(os.getenv("MONGO_DB_NAME"))
client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[str(os.getenv("MONGO_DB_NAME", "gesture_control"))]


async def close_mongo_connection():
    client.close()


def get_db():
    return db
