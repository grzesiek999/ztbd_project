import json
import requests

json_file_path = 'data/json/users.json'


def load_user_ids_from_file(file_path, n):
    with open(file_path, 'r') as file:
        users = json.load(file)

    user_ids = [str(user['_id']['$oid']) for user in users[:n]]
    return user_ids


def test_api_find_users(user_ids):
    url = "http://127.0.0.1:8081/mongo/users/bulk/find"
    payload = {"user_ids": user_ids}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Query executed successfully. Time taken:", response.json())
    else:
        print("Error:", response.status_code, response.text)


user_ids = load_user_ids_from_file(json_file_path, n=9500)
test_api_find_users(user_ids)
