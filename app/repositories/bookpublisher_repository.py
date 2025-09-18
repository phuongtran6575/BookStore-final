from uuid import UUID

from sqlmodel import Session, select
from models.bookstore_models import Publishers, ProductPublishers
from repositories import publisher_repository, book_repository


async def add_publisher_to_book(book_id: UUID, publisher_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    publisher = await publisher_repository.get_publisher_by_id(session, publisher_id)
    if not publisher:
        return None
    session.add(ProductPublishers(product_id=book.id, publisher_id=publisher.id))
    session.commit()
    session.refresh(book)
    return book.publishers

async def remove_publisher_from_book(book_id: UUID, publisher_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    publisher = await publisher_repository.get_publisher_by_id(session, publisher_id)
    if not publisher:
        return None
    statement = select(ProductPublishers).where(
    ProductPublishers.product_id == book.id,
    ProductPublishers.publisher_id == publisher.id
    )
    book_publishers = session.exec(statement).first()
    session.delete(book_publishers)
    session.commit()
    return {"message": f"Publisher {publisher_id} removed from book successfully"}

async def get_book_publishers(session: Session, book_id: UUID):
    statement = select(Publishers).join(ProductPublishers).where(ProductPublishers.product_id == book_id)
    publishers = session.exec(statement).all()
    publishers_name = []
    for publisher in publishers:
        publishers_name.append(publisher.name)
    return publishers_name