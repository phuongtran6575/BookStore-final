from uuid import UUID
from sqlmodel import Session
from schema.book_schema import ProductCreate, ProductUpdate
from repositories import book_repository


async def get_book_by_id(book_id: UUID, session: Session):
    return await book_repository.get_book_by_id(book_id, session)


async def get_all_books(session: Session):
    return await book_repository.get_all_book(session)


async def create_book(book: ProductCreate, session: Session):
    return await book_repository.create_book(book, session)


async def update_book(book_id: UUID, book: ProductUpdate, session: Session):
    return await book_repository.update_book(book_id, book, session)


async def delete_book(book_id: UUID, session: Session):
    return await book_repository.delete_book(book_id, session)
