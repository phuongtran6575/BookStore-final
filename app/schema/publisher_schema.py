from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class PublisherBase(SQLModel):
    name: str
    address: Optional[str] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None

class PublisherRead(PublisherBase):
    id: UUID