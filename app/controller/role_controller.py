from fastapi import APIRouter, HTTPException
from uuid import UUID
from schema.role_schema import RoleCreate
from models.bookstore_models import Roles
from services import role_service
from database.sqlite_database import sessionDepends
from core.helper import to_uuid

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
async def get_all_roles(session: sessionDepends):
    return await role_service.get_all_roles_service(session)


@router.get("/{role_id}")
async def get_role_by_id(role_id: UUID | str, session: sessionDepends):
    try:
        role_uuid = to_uuid(role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    role = await role_service.get_role_by_id_service(session, role_uuid)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/")
async def create_role(role: RoleCreate, session: sessionDepends):
    return await role_service.create_role_service(session, role)


@router.put("/{role_id}")
async def update_role(role_id: UUID | str, role: Roles, session: sessionDepends):
    try:
        role_uuid = to_uuid(role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_role = await role_service.update_role_service(session, role_uuid, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role


@router.delete("/{role_id}")
async def delete_role(role_id: UUID | str, session: sessionDepends):
    try:
        role_uuid = to_uuid(role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = await role_service.delete_role_service(session, role_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"status": "delete successful", "role_id": str(role_id)}