from uuid import UUID
from sqlmodel import Session, select

from models.bookstore_models import Addresses


async def add_address_to_user(session: Session, user_id: UUID, full_address: str, is_default: bool):
    address = Addresses(
        user_id=user_id,
        full_address=full_address,
        is_default=is_default
    )
    session.add(address)
    session.commit()
    session.refresh(address)
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