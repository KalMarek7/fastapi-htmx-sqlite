from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional


class ItemModel(BaseModel):
    name: str
    expiry_date: datetime
    image: str  # Base64 encoded image
    category: str
    notes: Optional[str] = None


class Items(BaseModel):
    items: List[ItemModel]
