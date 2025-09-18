from uuid import UUID

from sqlmodel import Session

from repositories import bookauthor_repository


async def get_book_authors(book_id: UUID, session: Session):
    return await bookauthor_repository.get_book_authors(session, book_id)

async def add_author_to_book(book_id: UUID, author_id: UUID, session: Session):
    return await bookauthor_repository.add_author_to_book(book_id, author_id, session)

async def remove_author_from_book(book_id: UUID, author_id: UUID, session: Session):
    return await bookauthor_repository.remove_author_from_book(book_id, author_id, session)