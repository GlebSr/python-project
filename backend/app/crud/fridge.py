import uuid

from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict

from ..database import MongoDB
from ..models.fridge import *
from ..utility import to_dict_with_id


class FridgeCRUD:
    def __init__(self, db: MongoDB):
        self.collection = db.get_collection("fridges")

    async def add_item_to_fridge(self, user_id: str, fridge_item_create: FridgeItemCreate) -> Optional[str]:
        item_data = fridge_item_create.dict()
        item_data["id"] = str(uuid.uuid4())
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$push": {"items": item_data}},
            upsert=True  # Создать документ, если не существует
        )
        if result.modified_count > 0 or result.upserted_id is not None:
            return  item_data["id"]
        return None

    async def get_fridge_by_user_id(self, user_id: str) -> Optional[Fridge]:
        fridge_data = await self.collection.find_one({"user_id": user_id})
        return Fridge.parse_obj(to_dict_with_id(fridge_data)) if fridge_data else None

    async def update_item_in_fridge(self, user_id: str, update_item: FridgeItem) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id, "items.id": update_item.id},
            {"$set": {f"items.$.{k}": v for k, v in update_item.dict(exclude_unset=True).items()}}
        )
        return result.modified_count > 0

    async def remove_item_from_fridge(self, user_id: str, item_id: str) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"items": {"id": item_id}}}
        )
        return result.modified_count > 0

    async def get_expired_items_in_fridge(self, user_id: str) -> List[FridgeItem]:
        fridge_data = await self.collection.find_one({"user_id": user_id})
        if not fridge_data or "items" not in fridge_data:
            return []

        expired_items = []
        for item in fridge_data["items"]:
            if "expiration_date" in item and item["expiration_date"] < datetime.now():
                expired_items.append(FridgeItem.parse_obj(item))
        return expired_items