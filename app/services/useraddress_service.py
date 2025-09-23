from uuid import UUID

from sqlmodel import Session

from repositories import useraddress_repository


async def add_address_to_user(session: Session, user_id: UUID, full_address: str, is_default: bool ):
    return await useraddress_repository.add_address_to_user(session, user_id, full_address, is_default)

async def remove_address_from_user(session: Session, address_id: UUID):
    return await useraddress_repository.remove_address_from_user(session, address_id)

async def get_addresses_user(session: Session, user_id:UUID):
    return await useraddress_repository.get_user_addresses(session, user_id)
