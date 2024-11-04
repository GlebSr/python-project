from enum import Enum

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from datetime import timedelta

from backend.app.models.product import Product


class FridgeItemCreate(BaseModel):
    product_id: str
    quantity: float
    production_date: datetime
    expiration_date: datetime
class FridgeItem(FridgeItemCreate):
    id: str

class Fridge(BaseModel):
    id: str
    user_id: str
    items: List[FridgeItem] = []