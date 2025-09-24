from uuid import UUID
from sqlmodel import Session, select

from models.bookstore_models import Addresses
from schema.user_schema import AddressCreate




async def add_address_to_user(session: Session, address: AddressCreate):
    address_create = Addresses(**address.model_dump())
    session.add(address_create)
    session.commit()
    session.refresh(address_create)
    return address


async def remove_address_from_user(session: Session, address_id: UUID):
    statement = select(Addresses).where(Addresses.id == address_id)
    result = session.exec(statement).first()
    if result is None:
        raise ValueError("Not found")  # Or raise an exception, e.g., HTTPException
    session.delete(result)
    session.commit()
    return {"status": "delete successful"}


async def get_user_addresses(session: Session, user_id: UUID):
    statement = select(Addresses).where(Addresses.user_id == user_id)
    results = session.exec(statement).all()
    return results