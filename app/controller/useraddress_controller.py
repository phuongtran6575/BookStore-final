from uuid import UUID
from fastapi import APIRouter, HTTPException
from services import auth_service
from models.bookstore_models import Addresses
from schema.user_schema import AddressCreate
from core.helper import to_uuid
from services import useraddress_service
from database.sqlite_database import sessionDepends
router = APIRouter(prefix="/addresses", tags=["Addresses"])
token = auth_service.oauth2_scheme

@router.get("/")
async def get_addresses_user(session: sessionDepends, user_id: UUID):
    try:
        user_uuid = to_uuid(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    return await useraddress_service.get_addresses_user(session, user_uuid)

@router.post("/", response_model=AddressCreate)
async def add_address_to_user(session: sessionDepends, address: AddressCreate ):
    
    try:
        user_uuid = to_uuid(address.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    
    address_create = await useraddress_service.add_address_to_user(session, address)
    if not address_create:
        return HTTPException(status_code=404, detail="Book not found")
    
    return address_create

@router.delete("/")
async def remove_address_from_user(session: sessionDepends, address_id: UUID):
    
    try:
        address_uuid = to_uuid(address_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    address =  await useraddress_service.remove_address_from_user(session, address_uuid)
    if not address:
        return HTTPException(status_code=404, detail="Book not found")
    
    return address