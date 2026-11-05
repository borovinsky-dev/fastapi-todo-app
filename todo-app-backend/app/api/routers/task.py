from fastapi import APIRouter, Depends, status, HTTPException

from app.services.task import TaskService
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from app.api.dependencies import get_task_service

from app.services.exceptions import TaskNotFound

router = APIRouter(prefix="/tasks", tags=["tasks"])


# HTTP-методы или роуты


@router.get("")
def get_tasks(
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskSchema]:
    return task_service.list_tasks()


# добавление 2 способами(более консерватиный через insert и через add)
@router.post("", status_code=status.HTTP_201_CREATED)
def create_tasks(
    payload: TaskCreateSchema, task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}", responses={404: {"description": "Task not found"}})
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str, task_service: TaskService = Depends(get_task_service)
) -> None:
    try:
        return task_service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
