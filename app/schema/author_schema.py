from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class AuthorBase(SQLModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(SQLModel):
    name: Optional[str] = None
    bio: Optional[str] = None

class AuthorRead(AuthorBase):
    id: UUID