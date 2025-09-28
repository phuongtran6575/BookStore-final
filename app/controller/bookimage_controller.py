from uuid import UUID
from fastapi import APIRouter, HTTPException
from schema.book_schema import BookImageCreate
from core.helper import to_uuid
from services import bookimage_service
from database.sqlite_database import sessionDepends
router = APIRouter(prefix="/bookimages", tags=["BookImages"]) 

@router.post("/")
async def add_image_to_book(session: sessionDepends, book: BookImageCreate  ):
    try:
        book_uuid = to_uuid(book.book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    image = await bookimage_service.add_image_to_book(session, book.image_url, book_uuid )
    if not image:
        raise HTTPException(status_code=404, detail="image not found")
    
    return image

@router.delete("/{image_id}")
async def remove_image_from_book(session: sessionDepends, image_id ):
    try:
        image_uuid = to_uuid(image_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    image = await bookimage_service.remove_image_from_book(session, image_uuid)
    return image

@router.get("/")
async def get_images_book(session: sessionDepends, book_id):
    try:
        book_uuid = to_uuid(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    images = await bookimage_service.get_images_book(session, book_uuid)
    if not images:
        raise HTTPException(status_code=404, detail="image not found")
    return images

@router.put("/{image_id}/set-thumbnail")
async def set_thumbnail_image(session: sessionDepends, image_id):
    try:
        image_uuid = to_uuid(image_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    image = await bookimage_service.set_thumbnail_image(session, image_uuid)
    if not image:
        raise HTTPException(status_code=404, detail="image not found")
    
    return image