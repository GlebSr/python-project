import json
import uuid

from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict
from fastapi import HTTPException
from ..database import MongoDB
from ..models.product import *
from ..utility import to_dict_with_id


class ProductCRUD:
    def __init__(self, db: MongoDB):
        self.collection = db.get_collection("products")

    async def create_product(self,user_id: str, product: ProductCreate) -> Optional[str]:
        product_data = product.dict()
        product_data["id"] = str(uuid.uuid4())
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$push": {"products": product_data}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id is not None:
            return product_data["id"]
        return None

    async def get_product_by_id(self, user_id: str, product_id: str) -> Optional[Product]:
        users_products = await self.collection.find_one({"user_id": user_id})
        for product_data in users_products["products"]:
            if product_data["id"] == str(product_id):
                return Product.parse_obj(dict(product_data))
        return None

    async def get_products_by_name(self, user_id: str, name: str) -> List[Product]:
        users_products = await self.collection.find_one({"user_id": user_id})
        if not users_products:
            return None
        products = []
        for product_data in users_products["products"]:
            if product_data["name"].lower().__contains__(name.lower()):
                products.append(Product.parse_obj(dict(product_data)))
        return products

    async def update_product(self, user_id: str, update_product: ProductUpdate) -> bool:
        result = await self.collection.update_one(
        {"user_id": user_id, "products.id": update_product.id},
        {"$set": {f"products.$.{k}": v for k, v in update_product.dict(exclude_unset=True).items()}}
        )
        return result.modified_count > 0

    async def delete_product(self, user_id: str, product_id: str) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"products": {"id": product_id}}}
        )
        return result.modified_count > 0