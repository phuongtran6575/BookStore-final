from sqlmodel import  Session, select
from bookstore.app.schema.book_schema import ProductCreate, ProductUpdate
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
    if book_update:
        book_update.title = book.title
        description: Optional[str] = None
        price: Optional[float] = None
        sale_price: Optional[float] = None
        stock_quantity: Optional[int] = None
        page_count: Optional[int] = None
        cover_type: Optional[str] = None
        publication_date: Optional[date] = None 
        session.add(book_update)
        session.commit()
    return book_update

async def create_book(book: ProductCreate, session: Session):
    book_data = Products(
        title= book.title,
        description= book.description,
        sku = book.sku,
        price = book.price,
        sale_price = book.sale_price,
        stock_quantity= book.stock_quantity,
        page_count = book.page_count,
        cover_type = book.cover_type,
        publication_date = book.publication_date
    )
    session.add(book_data)
    session.commit()
    session.refresh(book_data)
    return book_data

async def delete_book(book_id: UUID, session: Session):
    statement = select(Products).where(Products.id == book_id)
    book = session.exec(statement).first()
    if book:
        session.delete(book)
        session.commit()
    return {"status": "delete sucessful"}

