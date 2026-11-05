from sqlalchemy.orm import Session


from app.repositories.task import TaskRepo
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from .exceptions import TaskNotFound


class TaskService:
    def __init__(self, session: Session):
        self.db_session = session
        self.task_repo = TaskRepo(session)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repo.get_all()

        return [
            TaskSchema(id=task.id, title=task.title, completed=task.completed)
            for task in tasks_orm
        ]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repo.create(task_create.title)
        self.db_session.commit()
        self.db_session.refresh(task_orm)
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:

        try:
            task_for_update = self.task_repo.get_by_id(task_id=task_id)
        except Exception:
            raise TaskNotFound(task_id)
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db_session.commit()
        self.db_session.refresh(task_for_update)
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        try:
            task_for_delete = self.task_repo.get_by_id(task_id)
        except Exception:
            raise TaskNotFound(task_id)
        self.task_repo.delete(task_for_delete)
        self.db_session.commit()
