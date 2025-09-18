from uuid import UUID

from sqlmodel import Session, select
from models.bookstore_models import Roles, UserRoles
from repositories import role_repository, user_repository


async def add_role_to_user(user_id: UUID, role_id: UUID, session: Session):
    user = await user_repository.get_user_by_id(user_id, session)
    if not user:
        return None
    role = await role_repository.get_role_by_id(session, role_id)
    if not role:
        return None
    session.add(UserRoles(user_id=user.id, role_id=role.id))
    session.commit()
    session.refresh(user)
    return user.roles

async def remove_role_from_user(user_id: UUID, role_id: UUID, session: Session):
    user = await user_repository.get_user_by_id(user_id, session)
    if not user:
        return None
    role = await role_repository.get_role_by_id(session, role_id)
    if not role:
        return None
    statement = select(UserRoles).where(
    UserRoles.user_id == user.id,
    UserRoles.role_id == role.id
    )
    user_roles =  session.exec(statement).first()
    if  user_roles:
        session.delete(user_roles)
        session.commit()
    return user.roles

async def get_user_roles(session: Session, user_id: UUID):
    statement = select(Roles).join(UserRoles).where(UserRoles.user_id == user_id)
    roles = session.exec(statement).all()
    result = []   # dùng biến khác
    for role in roles:
        result.append({"id": role.id, "name": role.name})
    return result