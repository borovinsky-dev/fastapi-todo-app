from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None
