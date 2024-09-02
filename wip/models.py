from typing import List, Optional
from pydantic import BaseModel
import datetime


class ItemModel(BaseModel):
    picture_id: int
    name: str
    expiry_date: datetime.date
    category: str
    notes: Optional[str] = None
    image: Optional[str] = None
    item_id: Optional[int] = None


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
