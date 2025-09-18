from sqlmodel import Session, select
from uuid import UUID
from schema.role_schema import RoleCreate
from models.bookstore_models import Roles

from .base_repository import create_item, get_item_by_id, get_list_items, update_item_by_id, delete_item_by_id


def create_role(session: Session, schema: RoleCreate):
    return create_item(session, Roles, schema)


def get_role_by_id(session: Session, role_id: UUID):
    return get_item_by_id(session, Roles, role_id)


def get_list_roles(session: Session):
    return get_list_items(session, Roles)


def update_role(session: Session, role_id: UUID, schema: Roles):
    return update_item_by_id(session, Roles, role_id, schema)


def delete_role(session: Session, role_id: UUID):
    return delete_item_by_id(session, Roles, role_id)