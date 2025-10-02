from sqlmodel import  Session, col, select
from schema.book_schema import ProductCreate, ProductUpdate 
from models import Products, ProductAuthors,  ProductCategories, ProductPublishers
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

async def filter_book(session: Session, author_ids: list[UUID], publisher_ids: list[UUID], category_ids: list[UUID]):
    if not (author_ids or publisher_ids or category_ids):
        return session.exec(select(Products)).all()
    
    statement = select(Products).join(ProductAuthors).where(col(ProductAuthors.author_id).in_(author_ids))  # vẫn chạy.distinct()
    statement = select(Products).join(ProductAuthors).where(col(ProductPublishers.publisher_id).in_(publisher_ids))
    statement = select(Products).join(ProductAuthors).where(col(ProductCategories.category_id).in_(category_ids))
    
    results = session.exec(statement).all()
    return results
