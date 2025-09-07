from uuid import UUID
from fastapi import APIRouter
from database.sqlite_database import sessionDepends
from models import Categories

router = APIRouter(prefix="/category", tags=["Category"])

@router.get("/")
async def get_all_category():
    return

@router.get("/{category_id}")
async def get_category_by_id(category_id: UUID):
    return

@router.post("/")
async def create_category():
    return

@router.put("/{category_id}")
async def update_category(category_id: UUID):
    return

@router.delete("/{category_id}")
async def delete_category(category_id: UUID):
    return 