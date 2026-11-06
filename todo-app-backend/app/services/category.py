from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepo
from app.schemas.category import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
from .exceptions import CategoryNotFound


class CategoryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.category_repo = CategoryRepo(session)

    def list_categories(self) -> list[CategorySchema]:
        list_categories = self.category_repo.get_all()
        return [CategorySchema.model_validate(category) for category in list_categories]

    def create_category(self, payload: CategoryCreateSchema) -> CategorySchema:
        new_category = self.category_repo.create(category_name=payload.name)
        self.session.commit()
        self.session.refresh(new_category)
        return CategorySchema.model_validate(new_category)

    def update_category(
        self, category_id: str, payload: CategoryUpdateSchema
    ) -> CategorySchema:
        category_orm = self.category_repo.get_by_id(category_id)
        if category_orm is None:
            raise CategoryNotFound(id=category_id)
        if payload.name is not None:
            category_orm.name = payload.name
        self.session.commit()
        self.session.refresh(category_orm)
        return CategorySchema.model_validate(category_orm)

    def delete_category(self, category_id: str) -> None:
        category_orm = self.category_repo.get_by_id(category_id=category_id)
        if category_orm is None:
            raise CategoryNotFound(id=category_id)
        self.category_repo.delete(category_orm)
        self.session.commit()
