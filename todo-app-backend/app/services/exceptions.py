class TaskNotFound(Exception):
    def __init__(self, task_id: str) -> None:
        """ "Exception сервис слоя"""
        self.id = task_id
        super().__init__(f"Задача {task_id} не найдена")
