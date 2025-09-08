from sqlmodel import  Session, select
from schema.book_schema import ProductCreate, ProductUpdate
from models import Products
from uuid import UUID, uuid4

async def get_book_by_id(book_id: UUID, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book = session.exec(statement).first()
    return book

async def get_all_book(session: Session):
    statement = select(Products)
    list_book = session.exec(statement).all()
    return list_book

async def update_book(book_id: UUID, book: ProductUpdate, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book_update = session.exec(statement).first()
    if not book_update:
        return None

    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book_update, key, value)

    session.add(book_update)
    session.commit()
    session.refresh(book_update)
    return book_update

async def create_book(book: ProductCreate, session: Session):
    book_data = Products(**book.model_dump()) 
    session.add(book_data)
    session.commit()
    session.refresh(book_data)
    return book_data

async def delete_book(book_id: UUID, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book = session.exec(statement).first()
    if not book:
        return None

    session.delete(book)
    session.commit()
    return {"status": "delete sucessful"}

