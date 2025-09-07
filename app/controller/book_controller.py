from fastapi import APIRouter
from database.sqlite_database import sessionDepends
from schema import book_schema
from models import Products
from services import book_service
router = APIRouter(prefix="/book", tags=["Book"])

@router.get("/")
async def get_all_book(session: sessionDepends):
    list_book = await book_service.get_all_book(session)
    return list_book

@router.get("/{book_id}")
async def get_book_by_id(book_id: str, session: sessionDepends):
    book = await book_service.get_book_by_id(book_id, session)
    return book

@router.post("/")
async def create_book(book: ProductCreate, session: sessionDepends):
    book = await book_service.create_book(book, session)
    return book

@router.put("/{book_id}")
async def update_book(book_id: str, book: ProductCreate, session: sessionDepends):
    book = await book_service.update_book(book_id, book, session)
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: str, session: sessionDepends):
    book = await book_service.delete_book(book_id, session)
    return {"status": "delete sucessful"}