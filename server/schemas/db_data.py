from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    user_count: int = Field(..., examples=[100])
    device_count_range: tuple[int, int] = Field(..., examples=[(0, 5)])
    gesture_count_range: tuple[int, int] = Field(..., examples=[(0, 5)])
    log_count: int = Field(..., examples=[5])
