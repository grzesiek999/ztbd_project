from pydantic import BaseModel
from typing import List

class IdListRequest(BaseModel):
    id_list: List[int]