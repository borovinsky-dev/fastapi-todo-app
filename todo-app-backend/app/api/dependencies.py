from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskService


def get_task_service(db: Session = Depends(get_db)):
    """Функия для инъекции зависимости TaskService"""
    return TaskService(db)
