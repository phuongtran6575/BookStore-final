from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel


class CategoryBase(SQLModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    parent_id: Optional[UUID] = None

class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[UUID] = None

class CategoryRead(CategoryBase):
    id: UUID
    parent_id: Optional[UUID] = None