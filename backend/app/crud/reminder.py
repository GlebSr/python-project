import uuid
from typing import Optional, List
from backend.app.database import MongoDB
from backend.app.models.reminder import *
from datetime import datetime
import backend.app.utility as utility

class ReminderCRUD:
    def __init__(self, db: MongoDB):
        self.collection = db.get_collection("reminders")

    async def create_reminder(self, user_id: str, reminder: CreateReminder) -> Optional[str]:
        reminder_data = reminder.dict()
        reminder_data["id"] = str(uuid.uuid4())
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$push": {"reminders": reminder_data}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id is not None:
            return reminder_data["id"]
        return None

    async def get_reminder_by_id(self, user_id: str, reminder_id: str) -> Optional[Reminder]:
        reminder_datas = await self.collection.find_one({"user_id": user_id})
        for reminder in reminder_datas["reminders"]:
            if reminder["id"] == reminder_id:
                return Reminder.parse_obj(dict(reminder))
        return None

    async def get_all_reminders(self, user_id: str) -> List[Reminder]:
        reminders = await self.collection.find_one({"user_id": user_id})
        if reminders is None:
            return None
        return [Reminder.parse_obj(dict(reminder)) for reminder in reminders["reminders"]]

    async def update_reminder(self, user_id: str, update_reminder: UpdateReminder) -> bool:
        result = await self.collection.update_one(
          {"user_id": user_id, "reminders.id": update_reminder.id},
        {"$set": {f"reminders.$.{k}": v for k, v in update_reminder.dict(exclude_unset=True).items()}}
        )
        return result.modified_count > 0

    async def delete_reminder(self, user_id: str, reminder_id: str) -> bool:
        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"reminders": {"id": reminder_id}}}
        )
        return result.modified_count > 0
