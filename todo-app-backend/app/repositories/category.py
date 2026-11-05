from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import CategoryORM


class CategoryRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[CategoryORM]:
        return self.session.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.session.get(CategoryORM, category_id)

    def create(self, category_name: str) -> CategoryORM:
        new_category = CategoryORM(name=category_name)
        self.session.add(new_category)
        self.session.flush()
        return new_category

    def delete(self, category: CategoryORM) -> None:
        self.session.delete(category)
        self.session.flush()
