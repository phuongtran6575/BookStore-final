from uuid import UUID
from fastapi import APIRouter, HTTPException
from schema.user_schema import UserRoleCreate
from models.bookstore_models import UserRoles
from services import userrole_service
from core.helper import to_uuid
from database.sqlite_database import sessionDepends
router = APIRouter(prefix="/userroles", tags=["UserRoles"])


@router.get("/")
async def get_user_roles(user_id: UUID| str, session: sessionDepends):
    try:
        user_uuid = to_uuid(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    return await userrole_service.get_user_roles(user_uuid, session)


@router.post("/")
async def add_role_to_user(userrole: UserRoleCreate, session: sessionDepends):
    try:
        user_uuid = to_uuid(userrole.user_id)
        role_uuid = to_uuid(userrole.role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    userroles = await userrole_service.add_role_to_user(user_uuid, role_uuid, session)
    if not userroles:
        raise HTTPException(status_code=404, detail="role not found")
    return userroles


@router.delete("/{user_id}/{role_id}")
async def remove_role_from_user(user_id: UUID |str, role_id: UUID|str, session: sessionDepends):
    try:
        user_uuid = to_uuid(user_id)
        role_uuid = to_uuid(role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    userroles = await userrole_service.remove_role_from_user(user_uuid, role_uuid, session)
    if  userroles is None:
        raise HTTPException(status_code=404, detail="role not found")
    return {
        "status": "success",
        "remaining_roles": userroles  # có thể rỗng []
    }