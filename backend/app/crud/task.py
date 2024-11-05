import uuid
from typing import Optional, List
from backend.app.database import MongoDB
from backend.app.models.reminder import *
from datetime import datetime

class TaskCRUD:
    def __init__(self, db: MongoDB):
        self.collection = db.get_collection("tasks")

    async def create_task(self, user_id: str, task: CreateTask) -> Optional[str]:
        task_data = task.dict()
        task_data["id"] = str(uuid.uuid4())
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$push": {"tasks": task_data}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id is not None:
            return task_data["id"]
        return None

    async def get_task_by_id(self, user_id: str, task_id: str) -> Optional[Task]:
        task_data = await self.collection.find_one({"user_id": user_id})
        for reminder in task_data["tasks"]:
            if reminder["id"] == task_id:
                return Task.parse_obj(dict(reminder))
        return None

    async def get_all_tasks(self, user_id: str) -> List[Task]:
        tasks = await self.collection.find_one({"user_id": user_id})
        if tasks is None:
            return None
        return [Task.parse_obj(dict(task)) for task in tasks["tasks"]]

    async def update_task(self, user_id: str, update_task: UpdateTask) -> bool:
        result = await self.collection.update_one(
          {"user_id": user_id, "tasks.id": update_task.id},
        {"$set": {f"tasks.$.{k}": v for k, v in update_task.dict(exclude_unset=True).items()}}
        )
        return result.modified_count > 0

    async def delete_task(self, user_id: str, task_id: str) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"tasks": {"id": task_id}}}
        )
        return result.modified_count > 0