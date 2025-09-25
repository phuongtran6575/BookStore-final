from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
from repositories import role_repository
from models.bookstore_models import Roles, UserRoles, Users
from core.constants import ALGORITHM, SECRET_KEY
from schema.user_schema import UserCreate, UserRead
from repositories import user_repository
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_hashed_password(password: str):
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def authentication_user(email: str, password:str, session: Session):
    user = await get_user(email, session)
    if not user or not await verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_roles(session: Session, user_id: UUID):
    statement = select(Roles).join(UserRoles).where(UserRoles.user_id == user_id)
    roles = session.exec(statement).all()
    roles_name = []
    for role in roles:
        roles_name.append(role.name)
    return roles_name

async def get_user(email: str, session: Session):
    return await user_repository.get_user_by_email(email, session)

async def read_me(token: str, session:Session):
    user = await get_current_user(token, session)
    return {
        "user": UserRead(
                full_name = user.full_name,
                email = user.email,
                phone_number = user.phone_number,
                created_at = user.created_at,
                updated_at = user.updated_at
                ),
        "roles": await get_user_roles(session, user.id),
    }

async def get_current_user(token: str, session: Session):    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Not found")
    try:
        user_uuid = UUID(user_id) 
    except InvalidTokenError:
        raise ValueError("Not found")
    user = await user_repository.get_user_by_id(user_uuid, session)
    if user is None:
        raise ValueError("Not found")
    return user

async def registered(user: UserCreate, session: Session):
    user_create = Users(
        full_name= user.full_name,
        email=user.email,
        password_hash= await get_hashed_password(user.password_hash),
        phone_number= user.phone_number)
    role = await role_repository.get_role_by_name(session, "user")
    if role is None:
        raise ValueError("Not Found")
    
    session.add(UserRoles(user_id=user_create.id, role_id=role.id))
    session.commit()    
    return await user_repository.create_user(user_create, session)