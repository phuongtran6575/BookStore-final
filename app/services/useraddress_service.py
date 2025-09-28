from uuid import UUID

from sqlmodel import Session, select, update

from models.bookstore_models import Addresses
from repositories import useraddress_repository
from schema.user_schema import AddressCreate


async def add_address_to_user(session: Session, address: AddressCreate, user_id: UUID):
    address_create = Addresses(user_id = user_id,
                                   phone_number = address.phone_number,
                                   full_name=address.full_name,
                                   full_address=address.full_address,
                                   is_default=address.is_default)
    return await useraddress_repository.add_address_to_user(session, address_create)

async def remove_address_from_user(session: Session, address_id: UUID):
    return await useraddress_repository.remove_address_from_user(session, address_id)

async def get_addresses_user(session: Session, user_id:UUID):
    return await useraddress_repository.get_user_addresses(session, user_id)


async def get_address_by_id(session: Session, address_id: UUID):
    return await useraddress_repository.get_address_by_id(session, address_id)

async def update_address(session: Session, address_id: UUID, address: AddressCreate ):
    return await useraddress_repository.update_address(address_id, address, session)

async def set_default_address(address_id: UUID, session: Session ):
    address = await useraddress_repository.get_address_by_id(session, address_id)
    if not address:
        raise ValueError("Not  Found")
    
    statement = select(Addresses).where(Addresses.user_id == address.user_id)
    list_addresses = session.exec(statement)
    for record in list_addresses:
        record.is_default = False

    # Set địa chỉ này thành true
    address.is_default = True
    session.add(address)
    session.commit()
    session.refresh(address)
    return address
