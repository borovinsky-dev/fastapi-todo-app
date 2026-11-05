from fastapi import FastAPI
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router
from app.db.session import engine
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
app.include_router(category_router)
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"]
)
