from fastapi import APIRouter, HTTPException
from uuid import UUID
from services import author_service
from schema.author_schema import AuthorCreate, AuthorUpdate
from database.sqlite_database import sessionDepends
from core.helper import to_uuid

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/")
async def get_all_authors(session: sessionDepends):
    return await author_service.get_all_authors_service(session)


@router.get("/{author_id}")
async def get_author_by_id(author_id: UUID | str, session: sessionDepends):
    try:
        author_uuid = to_uuid(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    author = await author_service.get_author_by_id_service(session, author_uuid)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/")
async def create_author(author: AuthorCreate, session: sessionDepends):
    return await author_service.create_author_service(session, author)


@router.put("/{author_id}")
async def update_author(author_id: UUID | str, author: AuthorUpdate, session: sessionDepends):
    try:
        author_uuid = to_uuid(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    updated_author = await author_service.update_author_service(session, author_uuid, author)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.delete("/{author_id}")
async def delete_author(author_id: UUID | str, session: sessionDepends):
    try:
        author_uuid = to_uuid(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    deleted = await author_service.delete_author_service(session, author_uuid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"status": "delete successful", "author_id": str(author_id)}
