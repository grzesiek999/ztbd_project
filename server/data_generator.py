import os
import random
import json
import csv
import uuid
from datetime import datetime, timedelta

from faker import Faker
from bson import ObjectId


fake = Faker()

USER_COUNT = 1000
DEVICE_COUNT_RANGE = (0, 5)
GESTURE_COUNT_RANGE = (0, 5)
LOG_COUNT = 20  # Liczba logów dla każdego gestu
SEED = 42

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
def generate_users_with_devices(user_count, device_types, gestures_list,
                                device_count_range, gesture_count_range):
    devices = []
    users = []

    def generate_unique_email():
        email_prefix = fake.user_name() + str(uuid.uuid4())
        email_domain = fake.free_email_domain()
        email = f"{email_prefix}@{email_domain}"
        return email

    for _ in range(user_count):
        user_id = str(ObjectId())
        user_devices = generate_devices_with_gestures(user_id, device_types=device_types, gestures_list=gestures_list,
                                                      device_count_range=device_count_range,
                                                      gesture_count_range=gesture_count_range)
        devices.extend(user_devices)
        user = {
            "_id": {
                "$oid": user_id,
            },
            "username": fake.user_name(),
            "email": generate_unique_email(),
            "password_hash": fake.sha256(),
            "created_at": {
                "$date": fake.date_time_this_decade().isoformat(timespec="seconds")+"Z",
            }
        }
        users.append(user)
    return users, devices


# Funkcja generująca urządzenia
def generate_devices_with_gestures(user_id, device_types, gestures_list,
                                   device_count_range, gesture_count_range):
    devices = []
    for _ in range(random.randint(*device_count_range)):  # Liczba urządzeń dla użytkownika
        device_type = random.choice(device_types)
        device = {
            "_id": {
                "$oid": str(ObjectId())
            },
            "device_name": fake.word(),
            "device_type": device_type,
            "device_gestures": generate_device_gestures(gestures_list, gesture_count_range),
            # Gesty przypisane do urządzenia
            "owner_id": {
                "$oid": user_id
            }
        }
        devices.append(device)
    return devices


# Funkcja generująca gesty przypisane do urządzenia
def generate_device_gestures(gestures, gesture_count_range=GESTURE_COUNT_RANGE):
    device_gestures = []
    available_gestures = random.sample(gestures, random.randint(*gesture_count_range))  # Losowanie gestów bez powtórzeń
    for gesture in available_gestures:
        device_gestures.append({
            "gesture_id": str(ObjectId()),
            "gesture_type": gesture["gesture_type"],
            "gesture_name": fake.word(),
            "gesture_description": gesture["description"]
        })
    return device_gestures


# Funkcja generująca dane do PostgreSQL (CSV)
def generate_postgres_csv_data(users_data, devices_data, logs_count):
    """ With logs for MongoDB and PostgreSQL"""
    users_csv_data = []
    gestures_csv_data = [[gesture["id"], gesture["gesture_type"], gesture["description"]] for gesture in gestures]
    device_types_csv_data = [[i + 1, device_type] for i, device_type in enumerate(device_types)]
    devices_csv_data = []
    device_gestures_csv_data = []
    gesture_logs_csv_data = []

    gesture_logs_json = []

    gesture_id_mapping = {gesture["gesture_type"]: i + 1 for i, gesture in enumerate(gestures)}

    user_id = 0
    device_id = 0
    device_gestures_id = 0
    log_id = 0

    for user in users_data:
        user_id += 1
        users_csv_data.append(
            [user_id, user["username"], user["email"], user["password_hash"], user["created_at"]["$date"]])

        devices = [device for device in devices_data if device["owner_id"] == user["_id"]]

        for device in devices:
            device_id += 1
            devices_csv_data.append(
                [device_id, device_types.index(device["device_type"]) + 1, device["device_name"], user_id])

            for gesture in device["device_gestures"]:
                device_gestures_id += 1
                gesture_id = gesture_id_mapping[gesture["gesture_type"]]
                device_gestures_csv_data.append(
                    [device_gestures_id, gesture_id, gesture["gesture_name"], device_id])

                # Generowanie logów
                for _ in range(logs_count):
                    data_log = (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(timespec="seconds")+"Z"
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
                        "device_id": {
                            "$oid": device["_id"]["$oid"],
                        }
                    }
                    gesture_logs_json.append(log)
                    # Generowanie logów do Posgtres'a
                    log_id += 1
                    log = [log_id, device_gestures_id, data_log]
                    gesture_logs_csv_data.append(log)

    return {
        'json': {
            'gesture_logs': gesture_logs_json,
        },
        'csv': {
            'users': users_csv_data,
            'gestures': gestures_csv_data,
            'device_types': device_types_csv_data,
            'devices': devices_csv_data,
            'device_gestures': device_gestures_csv_data,
            'gesture_logs': gesture_logs_csv_data
        }
    }


def generate_data(user_count, device_types, gestures_list,
                                device_count_range, gesture_count_range, log_count):
    users_data_json, devices_data_json = generate_users_with_devices(user_count=user_count, device_types=device_types, gestures_list=gestures_list,
                                device_count_range=device_count_range, gesture_count_range=gesture_count_range)
    data = generate_postgres_csv_data(users_data_json, devices_data_json, logs_count=log_count)

    data['json']['users'] = users_data_json
    data['json']['devices'] = devices_data_json
    return data


def write_csv(csv_dir, filename, data, headers):
    with open(f'{csv_dir}{filename}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


def write_json(json_dir, filename, data):
    with open(os.path.join(json_dir, f'{filename}.json'), 'w') as f:
        json.dump(data, f, indent=4)


def export_data(data):
    csv_dir = f'/{os.getenv("POSTGRES_DATA_DIR")}/'
    json_dir = f'/{os.getenv("MONGO_DATA_DIR")}'
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)

    # Zapis do plików JSON
    for json_filename, json_data in data['json'].items():
        write_json(json_dir, json_filename, json_data)

    # Nagłówki CSV
    csv_headers = {
        'users': ['user_id', 'username', 'email', 'password_hash', 'created_at'],
        'gestures': ['gesture_id', 'gesture_type', 'description'],
        'device_types': ['device_type_id', 'type_name'],
        'devices': ['device_id', 'device_type_id', 'device_name', 'user_id'],
        'device_gestures': ['device_gesture_id', 'gesture_id', 'gesture_name', 'device_id'],
        'gesture_logs': ['log_id', 'device_gesture_id', 'timestamp']
    }

    # Zapis do plików CSV
    for csv_filename, csv_data in data['csv'].items():
        write_csv(csv_dir, csv_filename, csv_data, csv_headers[csv_filename])


def generate_data_and_export(user_count=USER_COUNT, device_types=device_types, gestures_list=gestures,
                                device_count_range=DEVICE_COUNT_RANGE, gesture_count_range=GESTURE_COUNT_RANGE,
                                log_count=LOG_COUNT):
    data = generate_data(user_count=user_count, device_types=device_types, gestures_list=gestures_list,
                                device_count_range=device_count_range, gesture_count_range=gesture_count_range,
                                log_count=log_count)
    export_data(data)


# generate_data_and_export(user_count=USER_COUNT, device_types=device_types, gestures_list=gestures,
#                                  device_count_range=DEVICE_COUNT_RANGE, gesture_count_range=GESTURE_COUNT_RANGE)