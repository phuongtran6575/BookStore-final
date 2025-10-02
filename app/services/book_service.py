from uuid import UUID
from fastapi import Query
from sqlmodel import Session, select
from models.bookstore_models import Products
from schema.book_schema import ProductCreate, ProductUpdate
from repositories import book_repository


async def get_book_by_id(book_id: UUID, session: Session):
    
    
    return await book_repository.get_book_by_id(book_id, session)


async def get_all_books(session: Session,page: int, page_size: int):
    total = len(session.exec(select(Products)).all())
    offset = (page - 1) * page_size
    items = session.exec(select(Products).offset(offset).limit(page_size)).all()
    return {
        "total": total,
        "page": page,
        "size": page_size,
        "items": items
        
    }


async def create_book(book: ProductCreate, session: Session):
    return await book_repository.create_book(book, session)


async def update_book(book_id: UUID, book: ProductUpdate, session: Session):
    return await book_repository.update_book(book_id, book, session)


async def delete_book(book_id: UUID, session: Session):
    return await book_repository.delete_book(book_id, session)

async def filter_book(session: Session, author_ids: list[UUID], publisher_ids: list[UUID], category_ids: list[UUID]):
    return await book_repository.filter_book(session, author_ids, publisher_ids, category_ids)
