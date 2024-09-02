from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class ItemModel(BaseModel):
    name: str
    expiry_date: str
    picture_id: int
    category: str
    notes: Optional[str] = None
    image: Optional[str] = None


class Items(BaseModel):
    items: List[ItemModel]


class UploadItem(BaseModel):
    # image: str
    id: Optional[int] = None
    src: str
    filename: str
    filesize: int
    initial: bool


class Images(BaseModel):
    images: List[UploadItem]
