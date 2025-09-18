from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.bookstore_models import ProductPublishers
from services import bookpublisher_service
from core.helper import to_uuid
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/bookpublishers", tags=["BookPublishers"])


@router.get("/")
async def get_book_publishers(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    return await bookpublisher_service.get_book_publishers(book_uuid, session)


@router.post("/")
async def add_publisher_to_book(bookpublisher: ProductPublishers, session: sessionDepends):
    try:
        book_uuid = to_uuid(bookpublisher.product_id)
        publisher_uuid = to_uuid(bookpublisher.publisher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookpublishers = await bookpublisher_service.add_publisher_to_book(book_uuid, publisher_uuid, session)
    if not bookpublishers:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return bookpublishers


@router.delete("/{book_id}/{publisher_id}")
async def remove_publisher_from_book(book_id: UUID | str, publisher_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
        publisher_uuid = to_uuid(publisher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookpublishers = await bookpublisher_service.remove_publisher_from_book(book_uuid, publisher_uuid, session)
    if  bookpublishers is None:
        raise HTTPException(status_code=404, detail="role not found")
    return {
        "status": "success",
        "publishers": bookpublishers  # có thể rỗng []
    }