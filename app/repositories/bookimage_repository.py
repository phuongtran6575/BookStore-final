from uuid import UUID
from sqlmodel import Session, select

from models.bookstore_models import ProductImages


async def add_image_to_book(session: Session, book_id: UUID, image_url:str):
    image = ProductImages(
        product_id=book_id,
        image_url=image_url, 
    )
    session.add(image)
    session.commit()
    session.refresh(image)
    return image

async def remove_image_from_book(session: Session, image_id: UUID):
    statement = select(ProductImages).where(ProductImages.id == image_id)
    result = session.exec(statement).first()
    session.delete(result)
    session.commit()
    return {"status": "delete successfull"}

async def get_book_images(session: Session, book_id: UUID):
    statement = select(ProductImages).where(ProductImages.product_id == book_id)
    results = session.exec(statement).all()
    return results

async def get_image_by_id(session: Session, image_id):
    statement = select(ProductImages).where(ProductImages.id == image_id)
    result = session.exec(statement).first()
    return result