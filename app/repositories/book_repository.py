from sqlmodel import  Session
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

async def update_book(book_id: UUID, book: Products, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book_update = session.exec(statement).first()
    if book_update:
        book_update.name = book.name
        book_update.price = book.price
        book_update.description = book.description
        book_update.category_id = book.category_id
        session.add(book_update)
        session.commit()
    return book_update

async def create_book(book: Products, session: Session):
    book_data = Products(
        id = uuid4(),
        name = book.name,
        price = book.price,
        description = book.description,
        category_id = book.category_id
    )
    session.add(book_data)
    session.commit()
    sessin.refresh(book_data)
    return book_data

async def delete_book(book_id: UUID, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book = session.exec(statement).first()
    if book:
        session.delete(book)
        session.commit()
    return {"status": "delete sucessful"}

