from uuid import UUID

from sqlmodel import Session, select
from models.bookstore_models import Authors, ProductAuthors
from repositories import author_repository, book_repository


async def add_author_to_book(book_id: UUID, author_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    author = await author_repository.get_author_by_id(session, author_id)
    if not author:
        return None
    session.add(ProductAuthors(product_id=book.id, author_id=author.id))
    session.commit()
    session.refresh(book)
    return book.authors

async def remove_author_from_book(book_id: UUID, author_id: UUID, session: Session):
    book = await book_repository.get_book_by_id(book_id, session)
    if not book:
        return None
    author = await author_repository.get_author_by_id(session, author_id)
    if not author:
        return None
    statement = select(ProductAuthors).where(
    ProductAuthors.product_id == book.id,
    ProductAuthors.author_id == author.id
    )
    book_authors = session.exec(statement).first()
    session.delete(book_authors)
    session.commit()
    return {"message": f"Author {author_id} removed from book successfully"}

async def get_book_authors(session: Session, book_id: UUID):
    statement = select(Authors).join(ProductAuthors).where(ProductAuthors.product_id == book_id)
    authors = session.exec(statement).all()
    authors_name = []
    for author in authors:
        authors_name.append(author.name)
    return authors_name