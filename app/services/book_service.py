from sqlmodel import  Session
from models import Products
from uuid import UUID, uuid4
from repositories import book_repository

async def get_book_by_id(book_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    return book

async def get_all_book(session: Session):
    list_book = await book_repository.get_all_book(session)
    return list_book

async def create_book(book: Products, session: Session):
    book_data = await book_repository.create_book(book, session)
    return book_data

async def update_book(book_id: UUID, book: Products, session: Session):
    book_update = await book_repository.update_book(book_id, book, session)
    if not book_update:
        return None
    return book_update

async def delete_book(book_id: UUID, session: Sessions):
    book_delete = await book_repository.delete_book(book_id, session)
    if not book_delete:
        return {"status": "delete fail"}
    return {"status": "delete sucessful"}