from fastapi import APIRouter, HTTPException
from uuid import UUID
from services import auth_service
from core.helper import to_uuid
from schema.user_schema import UserCreate, UserRead, UserUpdate
from services import user_service
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/users", tags=["Users"])

# ================= GET ALL =================
@router.get("/")
async def get_all_users(session: sessionDepends):
    users = await user_service.get_all_users(session)
    return users

# ================= GET ONE =================
@router.get("/{user_id}")
async def get_user_by_id(user_id: UUID | str, session: sessionDepends):
    try:
        user_uuid = to_uuid(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    user = await user_service.get_user_by_id(user_uuid, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ================= CREATE =================
@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: sessionDepends):
    created_user = await auth_service.registered(user, session)
    return created_user

# ================= UPDATE =================
@router.put("/{user_id}")
async def update_user(user_id: UUID | str, user: UserUpdate, session: sessionDepends):
    try:
        user_uuid = to_uuid(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    updated_user = await user_service.update_user(user_uuid, user, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# ================= DELETE =================
@router.delete("/{user_id}")
async def delete_user(user_id: UUID | str, session: sessionDepends):
    try:
        user_uuid = to_uuid(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    deleted_user = await user_service.delete_user(user_uuid, session)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status": "delete successful", "user_id": str(user_id)}
