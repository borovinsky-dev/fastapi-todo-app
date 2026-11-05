from fastapi import FastAPI, status, Depends, HTTPException
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.api.routers.task import router as task_router
from app.db.session import get_db, engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения")
    Base.metadata.create_all(bind=engine)
    yield
    print("Закрытие приложения")


# настройки для FastAPI и cors для нашего frontend
app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)


# # crud_views с категориями


# def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
#     return CategorySchema(id=category_orm.id, name=category_orm.name)


# @app.get("/categories")
# def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
#     category_from_db = db.scalars(select(CategoryORM)).all()
#     return [category_orm_to_model(category) for category in category_from_db]


# @app.post("/categories", status_code=status.HTTP_201_CREATED)
# def create_category(
#     category_create: CategoryCreateSchema,
#     category_id=str(uuid4()),
#     db: Session = Depends(get_db),
# ) -> CategorySchema:
#     new_category = CategoryORM(name=category_create.name)
#     db.add(new_category)
#     db.commit()
#     db.refresh(new_category)
#     return new_category


# @app.patch(
#     "/categories/{category_id}", responses={404: {"description": "Category not found"}}
# )
# def update_category(
#     category_id: str,
#     payload: CategoryUpdateSchema,
#     db: Session = Depends(get_db),
# ) -> CategorySchema:
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code=404, detail="Category not found")

#     if payload.name is not None:
#         category.name = payload.name
#     db.commit()
#     db.refresh(category)
#     return category_orm_to_model(category)


# @app.delete(
#     "/categories/{category_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={404: {"description": "Category not found"}},
# )
# def delete_task(category_id: str, db: Session = Depends(get_db)):
#     find_category_for_delete = db.get(CategoryORM, category_id)
#     if find_category_for_delete is None:
#         raise HTTPException(status_code=404, detail="Category not found")

#     db.delete(find_category_for_delete)
#     db.commit()
