import json
import csv
import os
import random
from faker import Faker
from typing import List, Dict, Any, Tuple


def init_faker(seed: int = None) -> Faker:
    """Initializes the Faker instance with an optional seed for deterministic data generation."""
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)
    return fake


def generate_gestures(fake: Faker, count: int) -> List[Dict[str, Any]]:
    """Generates gesture documents for the gestures collection."""
    gestures = []
    for i in range(count):
        gestures.append({
            "_id": f"gesture_id_{i + 1}",
            "gesture_name": fake.word(),
            "description": fake.sentence()
        })
    return gestures


def generate_devices(fake: Faker, user_id: str, device_count_range: Tuple[int, int], available_gestures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generates device documents for the user's devices, ensuring no duplicate gestures per device."""
    devices = []
    for i in range(random.randint(*device_count_range)):
        gesture_pool = available_gestures.copy()
        device_gestures = []
        num_gestures = random.randint(0, len(gesture_pool))  # Randomly choose between 0 and max available gestures
        for _ in range(num_gestures):
            if gesture_pool:
                gesture = gesture_pool.pop(random.randrange(len(gesture_pool)))  # Ensure unique gestures per device
                device_gestures.append({
                    "gesture_id": gesture["_id"],
                    "gesture_name": gesture["gesture_name"]
                })
        devices.append({
            "device_id": f"device_id_{user_id}_{i + 1}",  # Unique device ID for each user
            "device_name": fake.word(),
            "device_type": fake.random_element(elements=("Light", "Appliance")),
            "user_gestures": device_gestures
        })
    return devices


def generate_users(fake: Faker, user_count: int, device_count_range: Tuple[int, int], gestures: List[Dict[str, Any]]) -> \
List[Dict[str, Any]]:
    """Generates user documents for the users collection."""
    users = []
    for i in range(user_count):
        user_id = f"user_id_{i + 1}"
        users.append({
            "_id": user_id,
            "username": fake.user_name(),
            "email": fake.email(),
            "password_hash": fake.sha256(),
            "created_at": fake.date_time().isoformat(),
            "devices": generate_devices(fake, user_id, device_count_range, gestures)
        })
    return users


def generate_gesture_logs(fake: Faker, users: List[Dict[str, Any]], log_count: int) -> List[Dict[str, Any]]:
    """Generates gesture log documents for the gesture_logs collection."""
    logs = []
    for i in range(log_count):
        user = random.choice(users)
        device = random.choice(user["devices"])
        while not device["user_gestures"]:  # Ensure device has at least one gesture
            device = random.choice(user["devices"])
        gesture = random.choice(device["user_gestures"])
        logs.append({
            "_id": f"log_id_{i + 1}",
            "user_id": user["_id"],
            "gesture_id": gesture["gesture_id"],
            "timestamp": fake.date_time().isoformat(),
            "device_id": device["device_id"]
        })
    return logs


def generate_mongodb_data(user_count: int, device_count_range: Tuple[int, int], gesture_count: int, log_count: int,
                          seed: int = None) -> Dict[str, List[Dict[str, Any]]]:
    """Generates data for MongoDB collections."""
    fake = init_faker(seed)
    gestures = generate_gestures(fake, gesture_count)
    users = generate_users(fake, user_count, device_count_range, gestures)
    logs = generate_gesture_logs(fake, users, log_count)
    return {
        "users": users,
        "gestures": gestures,
        "gesture_logs": logs
    }


def save_json(data: Dict[str, List[Dict[str, Any]]], path: str):
    """Saves generated data to a JSON file."""
    for collection_name, documents in data.items():
        with open(f"{path}/{collection_name}.json", "w") as f:
            json.dump(documents, f, indent=4)


def generate_postgresql_data(mongo_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """Converts MongoDB data to PostgreSQL data format."""
    fake = init_faker()  # Initialize Faker instance
    postgresql_data = {
        "users": [],
        "gestures": [],
        "devices": [],
        "user_gestures": [],
        "gesture_logs": []
    }

    for user in mongo_data["users"]:
        postgresql_data["users"].append({
            "user_id": user["_id"],
            "username": user["username"],
            "email": user["email"],
            "password_hash": user["password_hash"],
            "created_at": user["created_at"]
        })
        for device in user["devices"]:
            postgresql_data["devices"].append({
                "device_id": device["device_id"],
                "device_name": device["device_name"],
                "user_id": user["_id"],
                "device_type": device["device_type"]
            })
            for gesture in device["user_gestures"]:
                postgresql_data["user_gestures"].append({
                    "user_gesture_id": fake.uuid4(),
                    "user_id": user["_id"],
                    "gesture_id": gesture["gesture_id"],
                    "device_id": device["device_id"],
                    "created_at": fake.date_time().isoformat()
                })

    for gesture in mongo_data["gestures"]:
        postgresql_data["gestures"].append({
            "gesture_id": gesture["_id"],
            "gesture_name": gesture["gesture_name"],
            "description": gesture["description"]
        })

    for log in mongo_data["gesture_logs"]:
        postgresql_data["gesture_logs"].append({
            "log_id": log["_id"],
            "user_id": log["user_id"],
            "gesture_id": log["gesture_id"],
            "timestamp": log["timestamp"],
            "device_id": log["device_id"]
        })

    return postgresql_data


def save_csv(data: Dict[str, List[Dict[str, Any]]], path: str):
    """Saves generated data to CSV files for PostgreSQL."""
    for table_name, rows in data.items():
        with open(f"{path}/{table_name}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    # Set parameters for data generation
    USER_COUNT = 10
    DEVICE_COUNT_RANGE = (1, 3)
    GESTURE_COUNT = 5
    LOG_COUNT = 20
    SEED = 42
    CSV_DIR = 'data/csv/'
    JSON_DIR = 'data/json/'

    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(CSV_DIR, exist_ok=True)

    # Generate data for MongoDB
    mongo_data = generate_mongodb_data(USER_COUNT, DEVICE_COUNT_RANGE, GESTURE_COUNT, LOG_COUNT, SEED)
    save_json(mongo_data, JSON_DIR)

    # Generate data for PostgreSQL
    postgresql_data = generate_postgresql_data(mongo_data)
    save_csv(postgresql_data, CSV_DIR)
