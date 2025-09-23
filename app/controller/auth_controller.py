from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from models.bookstore_models import Users
from core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from services import auth_service
from schema.user_schema import UserCreate, UserRead
from services import user_service
from database.sqlite_database import sessionDepends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])
token = auth_service.oauth2_scheme

@router.get("/read_me")
async def read_me( token: Annotated[str, Depends(token)],session: sessionDepends):
    current_user = await auth_service.get_current_user(token, session)
    if not current_user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return current_user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: sessionDepends):
    user = await auth_service.authentication_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    roles = await auth_service.get_user_roles(session, user.id)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "roles": roles}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserCreate)
async def register(user: Users,session: sessionDepends):
    created_user = await auth_service.registered(user, session)
    return created_user