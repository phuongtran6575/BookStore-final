from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PublisherBase(BaseModel):
    name: str
    address: Optional[str] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class PublisherRead(PublisherBase):
    id: UUID