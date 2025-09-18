from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.bookstore_models import ProductAuthors
from services import bookauthor_service
from core.helper import to_uuid
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/bookauthors", tags=["BookAuthors"])


@router.get("/")
async def get_book_authors(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    return await bookauthor_service.get_book_authors(book_uuid, session)


@router.post("/")
async def add_author_to_book(bookauthor: ProductAuthors, session: sessionDepends):
    try:
        book_uuid = to_uuid(bookauthor.product_id)
        author_uuid = to_uuid(bookauthor.author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookauthors = await bookauthor_service.add_author_to_book(book_uuid, author_uuid, session)
    if not bookauthors:
        raise HTTPException(status_code=404, detail="Author not found")
    return bookauthors


@router.delete("/{book_id}/{author_id}")
async def remove_author_from_book(book_id: UUID | str, author_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id)
        author_uuid = to_uuid(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    bookauthors = await bookauthor_service.remove_author_from_book(book_uuid, author_uuid, session)
    if  bookauthors is None:
        raise HTTPException(status_code=404, detail="role not found")
    return {
        "status": "success",
        "authors": bookauthors  # có thể rỗng []
    }