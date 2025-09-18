
from sqlmodel import Session
from uuid import UUID
from schema.role_schema import RoleCreate
from models.bookstore_models import Roles
from repositories import role_repository


def create_role_service(session: Session, role: RoleCreate):
    return role_repository.create_role(session, role)


def get_role_by_id_service(session: Session, role_id: UUID):
    return role_repository.get_role_by_id(session, role_id)


def get_all_roles_service(session: Session):
    return role_repository.get_list_roles(session)


def update_role_service(session: Session, role_id: UUID, role: Roles):
    return role_repository.update_role(session, role_id, role)


def delete_role_service(session: Session, role_id: UUID):
    return role_repository.delete_role(session, role_id)