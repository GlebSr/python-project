from enum import Enum

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from datetime import timedelta
class Unit(str, Enum):
    MILLILITERS = "milliliters"
    GRAMS = "grams"
    PIECES = "pieces"

class ProductCreate(BaseModel):
    code: int
    name: str
    expiration_period: int
    kcal: float
    protein: float
    fat: float
    carbs: float
    description: Optional[str] = None
    unit_type: Unit

class ProductUpdate(BaseModel):
    id: str
    name: Optional[str]
    expiration_period: Optional[datetime]
    kcal: Optional[float]
    protein: Optional[float]
    fat: Optional[float]
    carbs: Optional[float]
    description: Optional[str]
    unit_type: Optional[Unit]

class Product(ProductCreate):
    id: str