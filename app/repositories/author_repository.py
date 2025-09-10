from sqlmodel import Session, select
from uuid import UUID
from models import Authors
from schema.author_schema import AuthorCreate, AuthorRead, AuthorUpdate
from .base_repository import create_item, get_item_by_id, get_list_items, update_item_by_id, delete_item_by_id


def create_author(session: Session, schema: AuthorCreate):
    return create_item(session, Authors, schema)


def get_author_by_id(session: Session, author_id: UUID):
    return get_item_by_id(session, Authors, author_id)


def get_list_authors(session: Session):
    return get_list_items(session, Authors)


def update_author(session: Session, author_id: UUID, schema: AuthorUpdate):
    return update_item_by_id(session, Authors, author_id, schema)


def delete_author(session: Session, author_id: UUID):
    return delete_item_by_id(session, Authors, author_id)
