from typing import List

from pydantic import BaseModel


class ItemModel(BaseModel):
    id: int
    title: str
    description: str
    price: int
    quantity: int


# class ItemsModels(BaseModel):
#     __pydantic_root_model__ = List[ItemModel]