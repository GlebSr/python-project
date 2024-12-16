import uuid

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.app.models.fridge import *
from backend.app.crud.fridge import FridgeCRUD
from backend.app.database import get_db

router = APIRouter()

@router.get("/{user_id}/expired", response_model=List[FridgeItem])
async def get_expired_items(user_id: str, db=Depends(get_db)) -> List[FridgeItem]:
    fridge_crud = FridgeCRUD(db)
    return await fridge_crud.get_expired_items_in_fridge(user_id)

@router.get("/{user_id}/suggest_recipes")
async def suggest_recipes(user_id: str, db=Depends(get_db)):
    return {"recipes": ["Recipe 1", "Recipe 2", "Recipe 3"]}

@router.get("/{user_id}", response_model=Fridge)
async def get_fridge(user_id: str, db=Depends(get_db)) -> Fridge:
    fridge_crud = FridgeCRUD(db)
    fridge = await fridge_crud.get_fridge_by_user_id(user_id)
    if fridge is None:
        return None
    print(fridge)
    return fridge

@router.post("/{user_id}/items", response_model=Optional[str])
async def add_item_to_fridge(user_id: str, fridge_item: FridgeItemCreate, db=Depends(get_db)) -> Optional[str]:
    fridge_crud = FridgeCRUD(db)
    item_id = await fridge_crud.add_item_to_fridge(user_id, fridge_item)
    if item_id is None:
        return None
    return item_id

@router.put("/{user_id}/items")
async def update_fridge_item(user_id: str, update_data: FridgeItem, db=Depends(get_db)):
    fridge_crud = FridgeCRUD(db)
    success = await fridge_crud.update_item_in_fridge(user_id, update_data)
    if not success:
        return None

@router.delete("/{user_id}", response_model=Optional[bool])
async def remove_fridge_item(user_id: str, item_id: str, db=Depends(get_db)) -> Optional[bool]:
    fridge_crud = FridgeCRUD(db)
    success = await fridge_crud.remove_item_from_fridge(user_id, item_id)
    if not success:
        return False
    return True
