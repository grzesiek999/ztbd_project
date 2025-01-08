from pymongo import MongoClient, ASCENDING
import os

client: MongoClient = None
db = None


def connect_to_mongo():
    global client, db
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[str(os.getenv("MONGO_DB_NAME", "gesture_control"))]
    if 'users' not in db.list_collection_names():
        users_collection = db['users']
        users_collection.create_index([('email', ASCENDING)], unique=True)
    if 'devices' not in db.list_collection_names():
        devices_collection = db['devices']
        devices_collection.create_index([('device_type', ASCENDING)])
        devices_collection.create_index([('device_gestures.gesture_type', ASCENDING)])
        devices_collection.create_index([('owner_id', ASCENDING)])


def close_mongo_connection():
    client.close()


def get_db():
    return db
