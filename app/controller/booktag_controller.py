from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.bookstore_models import ProductTags
from services import booktag_service
from core.helper import to_uuid
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/booktags", tags=["BookTags"])


@router.get("/")
async def get_book_tags(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    return await booktag_service.get_book_tags(book_uuid, session)


@router.post("/")
async def add_tag_to_book(booktag: ProductTags, session: sessionDepends):
    try:
        book_uuid = to_uuid(booktag.product_id)
        tag_uuid = to_uuid(booktag.tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    booktags = await booktag_service.add_tag_to_book(book_uuid, tag_uuid, session)
    if not booktags:
        raise HTTPException(status_code=404, detail="Tag not found")
    return booktags


@router.delete("/{book_id}/{tag_id}")
async def remove_tag_from_book(book_id: UUID | str, tag_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
        tag_uuid = to_uuid(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    booktags = await booktag_service.remove_tag_from_book(book_uuid, tag_uuid, session)
    if not booktags:
        raise HTTPException(status_code=404, detail="Tag not found")
    return booktags