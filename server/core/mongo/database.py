from pymongo import MongoClient
import os

client: MongoClient = None
db = None


def connect_to_mongo():
    global client, db
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[str(os.getenv("MONGO_DB_NAME", "gesture_control"))]


def close_mongo_connection():
    client.close()


def get_db():
    return db
