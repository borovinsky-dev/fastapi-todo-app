class BaseExceptionId(Exception):
    def __init__(self, id: str, name_obj: str) -> None:
        self.id = id
        self.name_obj = name_obj
        super().__init__(f"{name_obj} {id} не найдена")


class TaskNotFound(BaseExceptionId):
    def __init__(self, id: str) -> None:
        super().__init__(id, "Задача")


class CategoryNotFound(BaseExceptionId):
    def __init__(self, id: str) -> None:
        super().__init__(id, "Категория")
