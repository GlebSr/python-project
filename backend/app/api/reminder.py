from typing import List, Optional

from fastapi import APIRouter, Depends
from pip._vendor.requests import Session

from backend.app.models.reminder import Reminder, CreateReminder, UpdateReminder
from backend.app.crud.reminder import ReminderCRUD
from backend.app.database import get_db

router = APIRouter()

@router.get("/{user_id}/all", response_model=List[Reminder])
async def get_reminders(user_id: str, db=Depends(get_db)) -> List[Reminder]:
    reminder_crud = ReminderCRUD(db)
    reminders = await reminder_crud.get_all_reminders(user_id)
    if reminders is None:
        return None
    return reminders

@router.get("/{user_id}", response_model=Reminder)
async def get_reminder(user_id: str, reminder_id: str, db=Depends(get_db)) -> Reminder:
    reminder_crud = ReminderCRUD(db)
    reminder = await reminder_crud.get_reminder_by_id(user_id, reminder_id)
    if reminder is None:
        return None
    return reminder

@router.post("/{user_id}", response_model=Optional[str])
async def create_reminder(user_id: str, reminder: CreateReminder, db=Depends(get_db)) -> Optional[str]:
    reminder_crud = ReminderCRUD(db)
    reminder_id = await reminder_crud.create_reminder(user_id, reminder)
    if reminder_id is None:
        return None
    return reminder_id

@router.put("/{user_id", response_model=bool)
async def update_reminder(user_id: str, reminder: UpdateReminder, db=Depends(get_db)) -> bool:
    reminder_crud = ReminderCRUD(db)
    success = await reminder_crud.update_reminder(user_id, reminder)
    return success

@router.delete("/{user_id}", response_model=bool)
async def delete_reminder(user_id: str, reminder_id: str, db=Depends(get_db)) -> bool:
    reminder_crud = ReminderCRUD(db)
    success = await reminder_crud.delete_reminder(user_id, reminder_id)
    return success