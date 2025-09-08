from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import EmailStr
from sqlmodel import SQLModel, Field


# =========================
# USER SCHEMAS
# =========================

class UserBase(SQLModel):
    full_name: Optional[str] = None
    email: EmailStr


class UserCreate(UserBase):
    password_hash: str
    phone_number: Optional[str] = None


class UserRead(UserBase):
    id: UUID
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password_hash: Optional[str] = None
