from fastapi import APIRouter, HTTPException
from uuid import UUID
from services import category_service
from schema.category_schema import CategoryCreate, CategoryUpdate
from database.sqlite_database import sessionDepends
from core.helper import to_category_read, to_uuid

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/")
async def get_all_categories(session: sessionDepends):
    return await category_service.get_all_categories_service(session)


@router.get("/{category_id}")
async def get_category_by_id(category_id: UUID | str, session: sessionDepends):
    try:
        category_uuid = to_uuid(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    category = await category_service.get_category_by_id_service(session, category_uuid)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return to_category_read(category)


@router.post("/")
async def create_category(category: CategoryCreate, session: sessionDepends):
    return await category_service.create_category_service(session, category)


@router.put("/{category_id}")
async def update_category(category_id: UUID | str, category: CategoryUpdate, session: sessionDepends):
    try:
        category_uuid = to_uuid(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_category = await category_service.update_category_service(session, category_uuid, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}")
async def delete_category(category_id: UUID | str, session: sessionDepends):
    try:
        category_uuid = to_uuid(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = await category_service.delete_category_service(session, category_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"status": "delete successful", "category_id": str(category_id)}
