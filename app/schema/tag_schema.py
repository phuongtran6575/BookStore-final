from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel


class TagBase(SQLModel):
    name: str
    slug: str

class TagCreate(TagBase):
    pass

class TagUpdate(SQLModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class TagRead(TagBase):
    id: UUID