from fastapi import APIRouter, HTTPException
from uuid import UUID
from services import publisher_service
from schema.publisher_schema import PublisherCreate, PublisherUpdate
from database.sqlite_database import sessionDepends
from core.helper import to_uuid

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.get("/")
async def get_all_publishers(session: sessionDepends):
    return await publisher_service.get_all_publishers_service(session)


@router.get("/{publisher_id}")
async def get_publisher_by_id(publisher_id: UUID | str, session: sessionDepends):
    try:
        publisher_uuid = to_uuid(publisher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    publisher = await publisher_service.get_publisher_by_id_service(session, publisher_uuid)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


@router.post("/")
async def create_publisher(publisher: PublisherCreate, session: sessionDepends):
    return await publisher_service.create_publisher_service(session, publisher)


@router.put("/{publisher_id}")
async def update_publisher(publisher_id: UUID | str, publisher: PublisherUpdate, session: sessionDepends):
    try:
        publisher_uuid = to_uuid(publisher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_publisher = await publisher_service.update_publisher_service(session, publisher_uuid, publisher)
    if not updated_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return updated_publisher


@router.delete("/{publisher_id}")
async def delete_publisher(publisher_id: UUID | str, session: sessionDepends):
    try:
        publisher_uuid = to_uuid(publisher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = await publisher_service.delete_publisher_service(session, publisher_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return {"status": "delete successful", "publisher_id": str(publisher_id)}
