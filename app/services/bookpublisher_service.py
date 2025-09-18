from uuid import UUID

from sqlmodel import Session

from repositories import bookpublisher_repository


async def get_book_publishers(book_id: UUID, session: Session):
    return await bookpublisher_repository.get_book_publishers(session, book_id)

async def add_publisher_to_book(book_id: UUID, publisher_id: UUID, session: Session):
    return await bookpublisher_repository.add_publisher_to_book(book_id, publisher_id, session)

async def remove_publisher_from_book(book_id: UUID, publisher_id: UUID, session: Session):
    return await bookpublisher_repository.remove_publisher_from_book(book_id, publisher_id, session)