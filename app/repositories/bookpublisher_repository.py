from uuid import UUID

from sqlmodel import Session, select
from schema.publisher_schema import ProductPublisherCreate
from models.bookstore_models import Products, Publishers, ProductPublishers
from repositories import publisher_repository, book_repository


async def add_publisher_to_book(bookpublisher: ProductPublisherCreate,session: Session):
    product = session.get(Products, bookpublisher.product_id)
    publisher = session.get(Publishers, bookpublisher.publisher_id)
    if not product or not publisher:
        return None

    book_publisher = ProductPublishers(
        product_id=bookpublisher.product_id,
        publisher_id=bookpublisher.publisher_id,
        edition=bookpublisher.edition,
        year=bookpublisher.year,
        isbn=bookpublisher.isbn
    )
    session.add(book_publisher)
    session.commit()
    session.refresh(book_publisher)
    return book_publisher

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
    if book_publishers:
        session.delete(book_publishers)
        session.commit()
    return {"message": f"Publisher {publisher_id} removed from book successfully"}

async def get_book_publishers(session: Session, book_id: UUID):
    statement = select(ProductPublishers).where(ProductPublishers.product_id == book_id)
    relations = session.exec(statement).all()

    results = []
    for rel in relations:
        results.append({
            "id": rel.publisher.id,
            "name": rel.publisher.name,
            "edition": rel.edition,
            "year": rel.year,
            "isbn": rel.isbn,
        })
    return results


async def update_book_publisher(
    bookpublisher: ProductPublisherCreate,
    session: Session 
):
    relation = session.get(
        ProductPublishers, 
        (bookpublisher.product_id, bookpublisher.publisher_id)
    )
    if not relation:
        raise ValueError("Not Found")

    update_data = bookpublisher.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key not in ["product_id", "publisher_id"]:  # khóa chính, không update
            setattr(relation, key, value)

    session.add(relation)
    session.commit()
    session.refresh(relation)

    return relation
