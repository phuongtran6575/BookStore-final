from fastapi import APIRouter, HTTPException
from uuid import UUID
from services import tag_service
from schema.tag_schema import TagCreate, TagUpdate
from database.sqlite_database import sessionDepends
from core.helper import to_uuid

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/")
async def get_all_tags(session: sessionDepends):
    return await tag_service.get_all_tags_service(session)


@router.get("/{tag_id}")
async def get_tag_by_id(tag_id: UUID | str, session: sessionDepends):
    try:
        tag_uuid = to_uuid(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    tag = await tag_service.get_tag_by_id_service(session, tag_uuid)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/")
async def create_tag(tag: TagCreate, session: sessionDepends):
    return await tag_service.create_tag_service(session, tag)


@router.put("/{tag_id}")
async def update_tag(tag_id: UUID | str, tag: TagUpdate, session: sessionDepends):
    try:
        tag_uuid = to_uuid(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_tag = await tag_service.update_tag_service(session, tag_uuid, tag)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@router.delete("/{tag_id}")
async def delete_tag(tag_id: UUID | str, session: sessionDepends):
    try:
        tag_uuid = to_uuid(tag_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = await tag_service.delete_tag_service(session, tag_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"status": "delete successful", "tag_id": str(tag_id)}