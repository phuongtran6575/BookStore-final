from uuid import UUID
from fastapi import Query
from sqlmodel import Session, col, select
from models.bookstore_models import ProductAuthors, ProductCategories, ProductPublishers, Products
from schema.book_schema import ProductCreate, ProductUpdate
from repositories import book_repository


async def get_book_by_id(book_id: UUID, session: Session):
    return await book_repository.get_book_by_id(book_id, session)


async def get_all_books(session: Session,page: int, page_size: int, author_ids: list[UUID], publisher_ids: list[UUID], category_ids: list[UUID] ):
    total = len(session.exec(select(Products)).all())
    offset = (page - 1) * page_size
    
    if not (author_ids or publisher_ids or category_ids):
        results =  session.exec(select(Products).offset(offset).limit(page_size)).all()
        return {
            "total": total,
            "page": page,
            "size": page_size,
            "items": results        
    }    
    
    statement = select(Products)

    if author_ids:
        statement = statement.join(ProductAuthors).where(col(ProductAuthors.author_id).in_(author_ids))
    if publisher_ids:
        statement = statement.join(ProductPublishers).where(col(ProductPublishers.publisher_id).in_(publisher_ids))
    if category_ids:
        statement = statement.join(ProductCategories).where(col(ProductCategories.category_id).in_(category_ids))

    statement = statement.distinct()
    results = session.exec(statement.offset(offset).limit(page_size)).all()
     
    return {
        "total": total,
        "page": page,
        "size": page_size,
        "items": results        
    }


async def create_book(book: ProductCreate, session: Session):
    return await book_repository.create_book(book, session)


async def update_book(book_id: UUID, book: ProductUpdate, session: Session):
    return await book_repository.update_book(book_id, book, session)


async def delete_book(book_id: UUID, session: Session):
    return await book_repository.delete_book(book_id, session)


