from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import TaskORM


class TaskRepo:
    def __init__(self, session: Session) -> None:
        self.db_session = session

    def get_all(self) -> list[TaskORM]:
        return self.db_session.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM:
        return self.db_session.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db_session.add(new_task)
        self.db_session.flush()
        return new_task

    def delete(self, task: TaskORM) -> None:
        self.db_session.delete(task)
        self.db_session.flush()
