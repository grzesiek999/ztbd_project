from pydantic import BaseModel


class ImportRequest(BaseModel):
    user_count: int
    device_count_range: tuple[int, int]
    gesture_count_range: tuple[int, int]
    log_count: int
