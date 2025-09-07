from sqlmodel import Session, select
from models import Categories
from uuid import UUID
from repositories import category_repository


async def get_category_by_id(category_id: UUID, session: Session):
    category = await category_repository.get_category_by_id(category_id, session)
    return category

async def get_all_category(session: Session):
    list_category = await category_repository.get_all_category(session)
    return list_category

async def create_category(category: Categories, session: Session):
    category_create = await category_repository.create_category(category, session)
    return category_create

async def update_category(category_id: UUID, category: Categories, session: Session):
    category_update = await category_repository.update_category(category_id, category, session)
    return category_update

async def delete_category(category_id: UUID, session: Session):
    category_delete = await category_repository.delete_category(category_id, session)
    if not category_delete:
        return {"status": "delete fail"}
    return {"status": "delete sucessful"}
