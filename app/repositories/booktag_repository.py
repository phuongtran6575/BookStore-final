from uuid import UUID

from sqlmodel import Session, select
from models.bookstore_models import Tags, ProductTags
from repositories import tag_repository, book_repository


async def add_tag_to_book(book_id: UUID, tag_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    tag = await tag_repository.get_tag_by_id(session, tag_id)
    if not tag:
        return None
    session.add(ProductTags(product_id=book.id, tag_id=tag.id))
    session.commit()
    session.refresh(book)
    return book.tags

async def remove_tag_from_book(book_id: UUID, tag_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    tag = await tag_repository.get_tag_by_id(session, tag_id)
    if not tag:
        return None
    statement = select(ProductTags).where(
    ProductTags.product_id == book.id,
    ProductTags.tag_id == tag.id
    )
    book_tags = session.exec(statement).first()
    if book_tags:
        session.delete(book_tags)
        session.commit()
    return {"message": f"Tag {tag_id} removed from book successfully"}

async def get_book_tags(session: Session, book_id: UUID):
    statement = select(Tags).join(ProductTags).where(ProductTags.product_id == book_id)
    tags = session.exec(statement).all()
    results = []
    for tag in tags:
        results.append({"id": tag.id, "name": tag.name})
    return results