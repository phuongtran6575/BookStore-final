from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.bookstore_models import  ProductCategories
from services import bookcategory_service
from core.helper import to_uuid
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/bookcategories", tags=["BookCategories"])


@router.get("/")
async def get_book_categories(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    return await bookcategory_service.get_book_categories(book_uuid, session)


@router.post("/")
async def add_category_to_book(bookcategory: ProductCategories, session: sessionDepends):
    try:
        book_uuid = to_uuid(bookcategory.product_id)
        category_uuid = to_uuid(bookcategory.category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookcategories = await bookcategory_service.add_category_to_book(book_uuid, category_uuid, session)
    if not bookcategories:
        raise HTTPException(status_code=404, detail="Category not found")
    return bookcategories


@router.delete("/{book_id}/{category_id}")
async def remove_category_from_book(book_id: UUID | str, category_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
        category_uuid = to_uuid(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookcategories = await bookcategory_service.remove_category_from_book(book_uuid, category_uuid, session)
    if not bookcategories:
        raise HTTPException(status_code=404, detail="Category not found")
    return bookcategories