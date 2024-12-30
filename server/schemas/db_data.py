from pydantic import BaseModel, Field


class ImportRequest(BaseModel):
    user_count: int = Field(..., examples=[100])
    device_count_range: tuple[int, int] = Field(..., examples=[(2, 2)])
    gesture_count_range: tuple[int, int] = Field(..., examples=[(3, 3)])
    log_count: int = Field(..., examples=[5])
