from typing import List

from pydantic import BaseModel


class DataItem(BaseModel):
    id: int
    name: str
    description: str
    category: str


class DataResponse(BaseModel):
    items: List[DataItem]
    total: int
