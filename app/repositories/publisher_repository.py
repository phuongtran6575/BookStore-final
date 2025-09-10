from sqlmodel import Session, select
from uuid import UUID
from models import Publishers
from schema.publisher_schema import PublisherCreate, PublisherRead, PublisherUpdate
from .base_repository import create_item, get_item_by_id, get_list_items, update_item_by_id, delete_item_by_id


def create_publisher(session: Session, schema: PublisherCreate):
    return create_item(session, Publishers, schema)


def get_publisher_by_id(session: Session, publisher_id: UUID):
    return get_item_by_id(session, Publishers, publisher_id)


def get_list_publishers(session: Session):
    return get_list_items(session, Publishers)


def update_publisher(session: Session, publisher_id: UUID, schema: PublisherUpdate):
    return update_item_by_id(session, Publishers, publisher_id, schema)


def delete_publisher(session: Session, publisher_id: UUID):
    return delete_item_by_id(session, Publishers, publisher_id)