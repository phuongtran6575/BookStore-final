from sqlmodel import Session, select
from uuid import UUID
from core.helper import to_category_read
from models import Categories
from schema.category_schema import CategoryCreate, CategoryRead, CategoryUpdate
from .base_repository import create_item, get_item_by_id, get_list_items, update_item_by_id, delete_item_by_id


def create_category(session: Session, schema: CategoryCreate):
    return create_item(session, Categories, schema)


def get_category_by_id(session: Session, category_id: UUID):
    return get_item_by_id(session, Categories, category_id)


async def get_list_categories(session: Session):
    categories = await get_list_items(session, Categories)
    return [to_category_read(c) for c in categories]


def update_category(session: Session, category_id: UUID, schema: CategoryUpdate):
    return update_item_by_id(session, Categories, category_id, schema)


def delete_category(session: Session, category_id: UUID):
    return delete_item_by_id(session, Categories, category_id)