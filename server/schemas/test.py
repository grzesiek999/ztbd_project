from typing import List

from pydantic import BaseModel, Field


class SamplesCount(BaseModel):
    samples_count: int = Field(..., examples=[10])


class SamplesAndRowsCount(SamplesCount):
    rows_count: int = Field(..., examples=[100])


class ExecutionTime(BaseModel):
    postgres_execution_times: List[float] = Field(..., examples=[13.45, 10.10])
    mongo_execution_times: List[float] = Field(..., examples=[15.12, 8.56])
