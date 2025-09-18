from uuid import UUID

from sqlmodel import Session

from repositories import bookcategory_repository


async def get_book_categories(book_id: UUID, session: Session):
    return await bookcategory_repository.get_book_categories(session, book_id)

async def add_category_to_book(book_id: UUID, category_id: UUID, session: Session):
    return await bookcategory_repository.add_category_to_book(book_id, category_id, session)

async def remove_category_from_book(book_id: UUID, category_id: UUID, session: Session):
    return await bookcategory_repository.remove_category_from_book(book_id, category_id, session)