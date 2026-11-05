from fastapi import APIRouter, Depends, status, HTTPException

from app.services.category import CategoryService
from app.schemas.category import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
from app.api.dependencies import get_category_service

from app.services.exceptions import CategoryNotFound

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def get_categories(
    category_service: CategoryService = Depends(get_category_service),
) -> list[CategorySchema]:
    return category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    category_payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service),
) -> CategorySchema:
    return category_service.create_category(category_payload)


@router.patch("/{category_id}", responses={404: {"description": "Category not found"}})
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_service),
) -> CategorySchema:
    try:
        return category_service.update_category(category_id, payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Category not found"}},
)
def delete_task(
    category_id: str, category_service: CategoryService = Depends(get_category_service)
):
    try:
        return category_service.delete_category(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
