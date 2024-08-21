from pydantic import BaseModel
from typing import List


class Recipie(BaseModel):
    rpie_title: str
    rpie_text: str


class Recipies(BaseModel):
    recipies: List[Recipie]
