from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass