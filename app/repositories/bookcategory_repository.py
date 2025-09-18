from uuid import UUID

from sqlmodel import Session, select
from models.bookstore_models import Categories, ProductCategories
from repositories import category_repository, book_repository


async def add_category_to_book(book_id: UUID, category_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        return None
    session.add(ProductCategories(product_id=book.id, category_id=category.id))
    session.commit()
    session.refresh(book)
    return book.categories

async def remove_category_from_book(book_id: UUID, category_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    category = await category_repository.get_category_by_id(session, category_id)
    if not category:
        return None
    statement = select(ProductCategories).where(
    ProductCategories.product_id == book.id,
    ProductCategories.category_id == category.id
    )
    book_categories = session.exec(statement).first()
    session.delete(book_categories)
    session.commit()
    return {"message": f"Category {category_id} removed from book successfully"}

async def get_book_categories(session: Session, book_id: UUID):
    statement = select(Categories).join(ProductCategories).where(ProductCategories.product_id == book_id)
    categories = session.exec(statement).all()
    categories_name = []
    for category in categories:
        categories_name.append(category.name)
    return categories_name