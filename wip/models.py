from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ItemModel(BaseModel):
    name: str
    expiry_date: datetime
    image: str  # Base64 encoded image
    category: str
    notes: Optional[str] = None


class Items(BaseModel):
    items: List[ItemModel]


class UploadItem(BaseModel):
    # image: str
    id: Optional[int] = None
    src: str
    filename: str
    filesize: int


class Images(BaseModel):
    images: List[UploadItem]
