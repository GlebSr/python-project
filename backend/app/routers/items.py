from fastapi import APIRouter
from typing import Union

router = APIRouter()

@router.get("/products")
def get_products():
    return {"test": "test1"}

@router.get("/items/{item_id}")
def read_item(item_id: int, s: Union[str, None] = None):
    return {"item_id": item_id, "q": s}