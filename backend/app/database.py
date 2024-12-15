import os
from typing import Any, Mapping

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.collection import Collection

#Почему-то не видит из env файла
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "control_db")
MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "pass")
print(DATABASE_NAME)

class MongoDB:
    client: AsyncIOMotorClient = None

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI, username=MONGO_INITDB_ROOT_USERNAME, password=MONGO_INITDB_ROOT_PASSWORD)
        self.db = self.client[DATABASE_NAME]
        self.products = self.db["products"]
        self.fridges = self.db["fridges"]


    async def close(self):
        if self.client:
            await self.client.close()

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection[Mapping[str, Any] | Any]:
        return self.db[collection_name]


mongodb = MongoDB()

def get_db() -> MongoDB:
    return mongodb