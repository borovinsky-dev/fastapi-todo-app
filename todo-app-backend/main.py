from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, String, select, insert
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker, mapped_column, Session
from contextlib import asynccontextmanager

# подключение к БД на синхронном движке и создание сессии для синхронных подключений
DATABASE_URL = "postgresql://todo_user:todo_pass@localhost:5432/todo_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения")
    Base.metadata.create_all(bind=engine)
    yield
    print("Закрытие приложения")


# настройки для FastAPI и cors для нашего frontend
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)


# схемы для API
class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):

    title: str | None = None
    completed: bool | None = None


# HTTP-методы или роуты
@app.get("/")
def hello_world(db: Session = Depends(get_db)):
    return {"message": "Hello World!"}


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
        id=task_orm.id, title=task_orm.title, completed=task_orm.completed
    )


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    return [task_orm_to_model(task) for task in db.scalars(select(TaskORM)).all()]


# добавление 2 способами(более консерватиный через insert и через add)
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_tasks(
    payload: TaskCreateSchema, db: Session = Depends(get_db)
) -> TaskSchema:
    # new_task = db.scalars(
    #     insert(TaskORM).values(title=payload.title, completed=False).returning(TaskORM)
    # ).one()
    # db.commit()
    # return task_orm_to_model(new_task)
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}", responses={404: {"description": "Task not found"}})
def update_task(
    task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)
) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if task_for_update is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.title is not None:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    db.refresh(task_for_update)
    return task_orm_to_model(task_for_update)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()


# crud_views с категориями


class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(100))


def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.name)


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    category_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in category_from_db]


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    category_create: CategoryCreateSchema,
    category_id=str(uuid4()),
    db: Session = Depends(get_db),
) -> CategorySchema:
    new_category = CategoryORM(name=category_create.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.patch(
    "/categories/{category_id}", responses={404: {"description": "Category not found"}}
)
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    db: Session = Depends(get_db),
) -> CategorySchema:
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if payload.name is not None:
        category.name = payload.name
    db.commit()
    db.refresh(category)
    return category_orm_to_model(category)


@app.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Category not found"}},
)
def delete_task(category_id: str, db: Session = Depends(get_db)):
    find_category_for_delete = db.get(CategoryORM, category_id)
    if find_category_for_delete is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(find_category_for_delete)
    db.commit()
