from sqlmodel import Session, select
from uuid import UUID
from models import Tags
from schema.tag_schema import TagCreate, TagRead, TagUpdate
from .base_repository import create_item, get_item_by_id, get_list_items, update_item_by_id, delete_item_by_id


def create_tag(session: Session, schema: TagCreate):
    return create_item(session, Tags, schema)


def get_tag_by_id(session: Session, tag_id: UUID):
    return get_item_by_id(session, Tags, tag_id)


def get_list_tags(session: Session):
    return get_list_items(session, Tags)


def update_tag(session: Session, tag_id: UUID, schema: TagUpdate):
    return update_item_by_id(session, Tags, tag_id, schema)


def delete_tag(session: Session, tag_id: UUID):
    return delete_item_by_id(session, Tags, tag_id)