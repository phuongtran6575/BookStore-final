from uuid import UUID
from sqlmodel import Session
from models.bookstore_models import UserRoles
from repositories import role_repository
from schema.user_schema import UserCreate, UserUpdate  # Giả sử bạn có các schema này
from repositories import user_repository

# =========================
# USER SERVICE
# =========================

async def get_user_by_id(user_id: UUID, session: Session):
    return await user_repository.get_user_by_id(user_id, session)

async def get_all_users(session: Session):
    return await user_repository.get_all_user(session)

async def create_user(user: UserCreate, session: Session):
    return await user_repository.create_user(user, session)

async def update_user(user_id: UUID, user: UserUpdate, session: Session):
    return await user_repository.update_user(user_id, user, session)

async def delete_user(user_id: UUID, session: Session):
    return await user_repository.delete_user(user_id, session)

