from sqlmodel import Session
from uuid import UUID
from repositories import author_repository
from schema.author_schema import AuthorCreate, AuthorRead, AuthorUpdate


def create_author_service(session: Session, author: AuthorCreate):
    return author_repository.create_author(session, author)


def get_author_by_id_service(session: Session, author_id: UUID):
    return author_repository.get_author_by_id(session, author_id)


def get_all_authors_service(session: Session):
    return author_repository.get_list_authors(session)


def update_author_service(session: Session, author_id: UUID, author: AuthorUpdate):
    return author_repository.update_author(session, author_id, author)


def delete_author_service(session: Session, author_id: UUID):
    return author_repository.delete_author(session, author_id)
