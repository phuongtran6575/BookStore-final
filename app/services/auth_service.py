from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session
from core.constants import ALGORITHM, SECRET_KEY
from schema.user_schema import UserCreate
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
    if not user or not verify_password(password, user.password_hash):
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

async def get_user(email: str, session: Session):
    return await user_repository.get_user_by_email(email, session)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session):    
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
    return await user_repository.create_user(user, session)