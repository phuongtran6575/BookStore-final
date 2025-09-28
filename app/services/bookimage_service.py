from uuid import UUID
from sqlmodel import Session, select

from models.bookstore_models import ProductImages
from repositories import bookimage_repository


async def add_image_to_book(session: Session, image_url: str, book_id: UUID):
    return await bookimage_repository.add_image_to_book(session, book_id, image_url, )

async def remove_image_from_book(session: Session, image_id: UUID ):
    return await bookimage_repository.remove_image_from_book(session, image_id)

async def get_images_book(session: Session, book_id: UUID):
    return await bookimage_repository.get_book_images(session, book_id)

async def set_thumbnail_image(session: Session,image_id ):
    image= await bookimage_repository.get_image_by_id(session, image_id)
    if not image:
        raise ValueError("Not  Found")
    
    statement = select(ProductImages).where(ProductImages.product_id == image.product_id)
    list_image = session.exec(statement)
    for record in list_image:
        record.is_thumbnail = False
        
    image.is_thumbnail = True
    session.add(image)
    session.commit()
    session.refresh(image)
    return image