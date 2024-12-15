from typing import List, Optional

from fastapi import APIRouter, Depends

from backend.app.models.reminder import Task, CreateTask, UpdateTask
from backend.app.crud.task import TaskCRUD
from backend.app.database import get_db

router = APIRouter()

@router.get("/{user_id}/all", response_model=Optional[List[Task]])
async def get_all_tasks(user_id: str, db=Depends(get_db)) -> Optional[List[Task]]:
    task_crud = TaskCRUD(db)
    tasks = await task_crud.get_all_tasks(user_id)
    if tasks is None:
        return None
    return tasks

@router.get("/{user_id}" ,response_model=Task)
async def get_tasks(user_id: str, task_id: str, db=Depends(get_db)) -> Task:
    task_crud = TaskCRUD(db)
    task = await task_crud.get_task_by_id(user_id, task_id)
    print(task)
    return task

@router.post("/{user_id}", response_model=Optional[str])
async def create_task(user_id: str, task: CreateTask, db=Depends(get_db)) -> Optional[str]:
    task_crud = TaskCRUD(db)
    task_id = await task_crud.create_task(user_id, task)
    if task_id is None:
        return None
    return task_id

@router.put("/{user_id}", response_model=bool)
async def update_task(user_id: str, task: UpdateTask, db=Depends(get_db)) -> bool:
    task_crud = TaskCRUD(db)
    success = await task_crud.update_task(user_id, task)
    return success

@router.delete("/{user_id}", response_model=bool)
async def delete_task(user_id: str, task_id: str, db=Depends(get_db)) -> bool:
    task_crud = TaskCRUD(db)
    success = await task_crud.delete_task(user_id, task_id)
    return success

