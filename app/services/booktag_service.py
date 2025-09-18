from uuid import UUID

from sqlmodel import Session

from repositories import booktag_repository


async def get_book_tags(book_id: UUID, session: Session):
    return await booktag_repository.get_book_tags(session, book_id)

async def add_tag_to_book(book_id: UUID, tag_id: UUID, session: Session):
    return await booktag_repository.add_tag_to_book(book_id, tag_id, session)

async def remove_tag_from_book(book_id: UUID, tag_id: UUID, session: Session):
    return await booktag_repository.remove_tag_from_book(book_id, tag_id, session)