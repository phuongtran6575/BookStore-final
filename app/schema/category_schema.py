from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    parent_id: Optional[UUID] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[UUID] = None

class CategoryRead(CategoryBase):
    id: UUID
    parent_id: Optional[UUID] = None