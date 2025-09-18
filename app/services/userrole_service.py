from uuid import UUID

from sqlmodel import Session

from repositories import  userrole_repository


async def get_user_roles(user_id: UUID, session: Session):
    return await userrole_repository.get_user_roles(session, user_id)

async def add_role_to_user(user_id: UUID, role_id: UUID, session: Session):
    return await userrole_repository.add_role_to_user(user_id, role_id, session)

async def remove_role_from_user(user_id: UUID, role_id: UUID, session: Session):
    return await userrole_repository.remove_role_from_user(user_id, role_id, session)