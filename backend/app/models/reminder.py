from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class PriorityLevel(int, Enum):
    High = 1
    Middle = 2
    Low = 3

class Status(str, Enum):
    Pause = "pause"
    InProgress = "inprogress"
class CreateReminder(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime                # Дата и время напоминания
    custom_interval: Optional[timedelta] = None     # Если frequency = CUSTOM, задается интервал

class UpdateReminder(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    custom_interval: Optional[timedelta]
class Reminder(CreateReminder):
    id: str


class CreateTask(BaseModel):
    description: Optional[str] = None
    title: str
    priority: PriorityLevel                 # Низкий, средний или высокий
    due_date: Optional[datetime] = None # Дедлайн задачи
    status: Optional[Status] = Status.InProgress                      # В ожидании, выполнено и т.п.
    subtasks: Optional[list[str]] = [] # Список подзадач (можно расширить на отдельную модель)

class UpdateTask(BaseModel):
    description: Optional[str] = None
    id: str
    title: Optional[str]
    priority: Optional[PriorityLevel]
    due_date: Optional[datetime] = None
    status: Optional[Status] = None
    subtasks: Optional[list[str]] = None
class Task(CreateTask):
    id: str
