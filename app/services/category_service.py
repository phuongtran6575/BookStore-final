from sqlmodel import Session
from uuid import UUID
from repositories import category_repository
from schema.category_schema import CategoryCreate, CategoryRead, CategoryUpdate


def create_category_service(session: Session, category: CategoryCreate):
    return category_repository.create_category(session, category)


def get_category_by_id_service(session: Session, category_id: UUID):
    return category_repository.get_category_by_id(session, category_id)


def get_all_categories_service(session: Session):
    return category_repository.get_list_categories(session)


def update_category_service(session: Session, category_id: UUID, category: CategoryUpdate):
    return category_repository.update_category(session, category_id, category)


def delete_category_service(session: Session, category_id: UUID):
    return category_repository.delete_category(session, category_id)

