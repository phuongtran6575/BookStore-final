from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import UUID4, BaseModel, EmailStr


# =========================
# USER SCHEMAS
# =========================

class UserBase(BaseModel):
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


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password_hash: Optional[str] = None
    
    
class UserRoleCreate(BaseModel):
    user_id: UUID4 | str
    role_id: UUID4 | str
