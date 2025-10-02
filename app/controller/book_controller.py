from uuid import UUID
from fastapi import APIRouter, Query
from core.helper import to_uuid
from database.sqlite_database import sessionDepends
from schema.book_schema import ProductBase, ProductCreate, ProductRead, ProductUpdate
from services import book_service
from fastapi import APIRouter, HTTPException
from uuid import UUID
from fastapi import APIRouter, HTTPException
from uuid import UUID


router = APIRouter(prefix="/books", tags=["Books"])


# ================= GET ALL =================
@router.get("/")
async def get_all_books(session: sessionDepends,page: int = Query(1, ge=1),page_size: int = Query(12, ge=1, le=50)):
    books = await book_service.get_all_books(session, page, page_size)
    return books


# ================= GET ONE =================
@router.get("/{book_id}")
async def get_book_by_id(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id) 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    book = await book_service.get_book_by_id(book_uuid, session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ================= CREATE =================
@router.post("/")
async def create_book(book: ProductCreate, session: sessionDepends):
    created_book = await book_service.create_book(book, session)
    return created_book


# ================= UPDATE =================
@router.put("/{book_id}")
async def update_book(book_id: UUID | str, book: ProductUpdate, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id) 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    updated_book = await book_service.update_book(book_uuid, book, session)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


# ================= DELETE =================
@router.delete("/{book_id}")
async def delete_book(book_id: UUID | str, session: sessionDepends):
    try:
        book_uuid = to_uuid(book_id) 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    deleted_book = await book_service.delete_book(book_uuid, session)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "delete successful", "book_id": str(book_id)}

@router.get("/")
async def filter_book(session: sessionDepends, author_ids: list[UUID], publisher_ids: list[UUID], category_ids: list[UUID]):
    books = await book_service.filter_book(session, author_ids, publisher_ids, category_ids)
    return books
