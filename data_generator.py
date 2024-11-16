import os
import random
import json
import csv
from datetime import datetime, timedelta
from faker import Faker
from bson import ObjectId

# Inicjalizacja biblioteki Faker
fake = Faker()

# Parametry konfiguracyjne
USER_COUNT = 10000
DEVICE_COUNT_RANGE = (0, 5)
GESTURE_COUNT_RANGE = (0, 5)
LOG_COUNT = 20  # Liczba logów dla każdego gestu
SEED = 42
CSV_DIR = 'data/csv/'
JSON_DIR = 'data/json/'

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

# Definicja gestów i urządzeń
gestures = [
    {"id": 1, "gesture_type": "Right Swipe", "description": "Swipe to the right"},
    {"id": 2, "gesture_type": "Left Swipe", "description": "Swipe to the left"},
    {"id": 3, "gesture_type": "Wave Up", "description": "Waving hand up"},
    {"id": 4, "gesture_type": "Wave Down", "description": "Waving hand down"},
    {"id": 5, "gesture_type": "Double Tap", "description": "Tap twice"}
]

device_types = ["Light", "Appliance", "Camera", "Thermostat"]


# Funkcja generująca dane użytkowników
def generate_users():
    users = []
    for _ in range(USER_COUNT):
        user = {
            "_id": {
                "$oid": str(ObjectId()),
            },
            "username": fake.user_name(),
            "email": fake.email(),
            "password_hash": fake.sha256(),
            "created_at": {
                "$date": fake.date_this_decade().isoformat(),
            },
            "devices": generate_devices()  # Generowanie urządzeń dla użytkownika
        }
        users.append(user)
    return users


# Funkcja generująca urządzenia
def generate_devices():
    devices = []
    for _ in range(random.randint(*DEVICE_COUNT_RANGE)):  # Liczba urządzeń dla użytkownika
        device_type = random.choice(device_types)
        device = {
            "device_id": str(ObjectId()),
            "device_name": fake.word(),
            "device_type": device_type,
            "device_gestures": generate_device_gestures()  # Gesty przypisane do urządzenia
        }
        devices.append(device)
    return devices


# Funkcja generująca gesty przypisane do urządzenia
def generate_device_gestures():
    device_gestures = []
    available_gestures = random.sample(gestures, random.randint(*GESTURE_COUNT_RANGE))  # Losowanie gestów bez powtórzeń
    for gesture in available_gestures:
        device_gestures.append({
            "gesture_id": str(ObjectId()),
            "gesture_type": gesture["gesture_type"],
            "gesture_name": fake.word(),
            "gesture_description": gesture["description"]
        })
    return device_gestures


# Funkcja generująca dane do PostgreSQL (CSV)
def generate_postgres_csv_data(users_data):
    users_csv_data = []
    gestures_csv_data = [[gesture["id"], gesture["gesture_type"], gesture["description"]] for gesture in gestures]
    device_types_csv_data = [[i + 1, device_type] for i, device_type in enumerate(device_types)]
    devices_csv_data = []
    user_gestures_csv_data = []
    gesture_logs_csv_data = []

    gesture_logs_json = []

    gesture_id_mapping = {gesture["gesture_type"]: i + 1 for i, gesture in enumerate(gestures)}

    user_id = 0
    device_id = 0
    user_gestures_id = 0
    log_id = 0

    for user in users_data:
        user_id += 1
        users_csv_data.append(
            [user_id, user["username"], user["email"], user["password_hash"], user["created_at"]["$date"]])

        for device in user["devices"]:
            device_id += 1
            devices_csv_data.append(
                [device_id, device_types.index(device["device_type"]) + 1, device["device_name"], user_id])

            for gesture in device["device_gestures"]:
                user_gestures_id += 1
                gesture_id = gesture_id_mapping[gesture["gesture_type"]]
                user_gestures_csv_data.append(
                    [user_gestures_id, user_id, gesture_id, gesture["gesture_name"], device_id])

                # Generowanie logów
                for _ in range(LOG_COUNT):
                    data_log = (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
                    # Generowanie logów do MongoDB
                    log = {
                        "_id": {
                            "$oid": str(ObjectId()),
                        },
                        "user_id": {
                            "$oid": user["_id"]["$oid"],
                        },
                        "gesture_id": gesture["gesture_id"],
                        "timestamp": {
                            "$date": data_log,
                        },
                        "device_id": device["device_id"]
                    }
                    gesture_logs_json.append(log)
                    # Generowanie logów do Posgtres'a
                    log_id += 1
                    log = [log_id, user_id, gesture_id, data_log, device_id]
                    gesture_logs_csv_data.append(log)

    return gesture_logs_json, users_csv_data, gestures_csv_data, device_types_csv_data, devices_csv_data, user_gestures_csv_data, gesture_logs_csv_data


# Generowanie danych do MongoDB
users_data = generate_users()

# Zapis danych do pliku JSON (MongoDB)
with open(f'{JSON_DIR}users.json', 'w') as f:
    json.dump(users_data, f, indent=4)

# Generowanie danych do PostgreSQL i logów do MongoDB
gesture_logs_json, users_csv_data, gestures_csv_data, device_types_csv_data, devices_csv_data, user_gestures_csv_data, gesture_logs_csv_data = generate_postgres_csv_data(
    users_data)

# Zapis logów do pliku JSON (MongoDB)
with open(f'{JSON_DIR}gesture_logs.json', 'w') as f:
    json.dump(gesture_logs_json, f, indent=4)


# Zapis danych do plików CSV (PostgreSQL)
def write_csv(filename, data, headers):
    with open(f'{CSV_DIR}{filename}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


write_csv('users', users_csv_data, ['user_id', 'username', 'email', 'password_hash', 'created_at'])
write_csv('gestures', gestures_csv_data, ['gesture_id', 'gesture_type', 'description'])
write_csv('device_types', device_types_csv_data, ['device_type_id', 'type_name'])
write_csv('devices', devices_csv_data, ['device_id', 'device_type_id', 'device_name', 'user_id'])
write_csv('device_gestures', user_gestures_csv_data,
          ['device_gesture_id', 'user_id', 'gesture_id', 'gesture_name', 'device_id'])
write_csv('gesture_logs', gesture_logs_csv_data, ['log_id', 'user_id', 'gesture_id', 'timestamp', 'device_id'])
