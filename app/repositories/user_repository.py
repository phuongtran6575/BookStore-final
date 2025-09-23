from sqlmodel import Session, select
from schema.user_schema import UserCreate, UserUpdate
from models import Users
from uuid import UUID, uuid4

async def get_user_by_id(user_id: UUID, session: Session):
    statement = select(Users).where(Users.id == user_id)
    user = session.exec(statement).first()
    if not user:
        return None
    return user

async def get_user_by_email(email: str, session: Session):
    statement = select(Users).where(Users.email == email)
    user = session.exec(statement).first()
    if not user:
        return None
    return user

async def create_user(user: Users, session: Session):
    user_data = Users(**user.model_dump()) 
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

async def get_all_user(session: Session):
    statement = select(Users)
    list_users = session.exec(statement).all()
    return list_users

async def update_user(user_id: UUID, user: UserUpdate, session: Session):
    statement = select(Users).where(Users.id == user_id)
    user_update = session.exec(statement).first()
    if not user_update:
        return None

    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user_update, key, value)

    session.add(user_update)
    session.commit()
    session.refresh(user_update)
    return user_update

async def delete_user(user_id: UUID, session: Session):
    statement = select(Users).where(Users.id == user_id)
    user = session.exec(statement).first()
    if not user:
        return None
    session.delete(user)
    session.commit()
    return {"status": "delete sucessful"}
