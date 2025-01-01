import os
import pandas as pd


def get_users_id_map() -> pd.DataFrame:
    data_dir = os.getenv("DATA_DIR", "data")
    users_id_map_file = os.getenv("USER_ID_MAP_FILE", "users_id_map.csv")
    users_id_map = pd.read_csv(f"/{data_dir}/{users_id_map_file}")
    return users_id_map


def get_devices_id_map() -> pd.DataFrame:
    data_dir = os.getenv("DATA_DIR", "data")
    devices_id_map_file = os.getenv("DEVICES_ID_MAP_FILE", "devices_id_map.csv")
    devices_id_map = pd.read_csv(f"/{data_dir}/{devices_id_map_file}")
    return devices_id_map


def get_random_ids(df_ids: pd.DataFrame, rows_count: int = None) -> tuple:
    # Check if rows_count is greater than the number of available rows
    if rows_count is None:
        selected_rows = df_ids
    elif rows_count > len(df_ids):
        raise ValueError("rows_count is greater than the number of available rows in the users_id_map")
    else:
        selected_rows = df_ids.sample(n=rows_count, replace=False)

    postgres_ids = selected_rows['postgres_id'].tolist()
    mongo_ids = selected_rows['mongo_id'].tolist()

    return postgres_ids, mongo_ids
