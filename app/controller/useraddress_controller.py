from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from services import auth_service
from models.bookstore_models import Addresses
from schema.user_schema import AddressCreate
from core.helper import to_uuid
from services import useraddress_service
from database.sqlite_database import sessionDepends
router = APIRouter(prefix="/addresses", tags=["Addresses"])
token = auth_service.oauth2_scheme

@router.get("/")
async def get_addresses_user(token: Annotated[str, Depends(token)], session: sessionDepends):
    user = await auth_service.get_current_user(token, session)
    try:
        user_uuid = to_uuid(user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    return await useraddress_service.get_addresses_user(session, user_uuid)

@router.post("/", response_model=AddressCreate)
async def add_address_to_user(token: Annotated[str, Depends(token)],session: sessionDepends, address: AddressCreate ):
    user = await auth_service.get_current_user(token, session)
    try:
        user_uuid = to_uuid(user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    
    address_create = await useraddress_service.add_address_to_user(session, address, user_uuid)
    if not address_create:
        return HTTPException(status_code=404, detail="Address not found")
    
    return address_create

@router.delete("/{address_id}")
async def remove_address_from_user(token: Annotated[str, Depends(token)],  session: sessionDepends, address_id: UUID):
    user = await auth_service.get_current_user(token, session)
    
    try:
        address_uuid = to_uuid(address_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    address = await  useraddress_service.get_address_by_id(session, address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    
    if user.id != address.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this address")
    
    address_delete =  await useraddress_service.remove_address_from_user(session, address_uuid)
    if not address_delete:
        return HTTPException(status_code=404, detail="Address not found")
    
    return address_delete

@router.put("/{address_id}")
async def update_address(token: Annotated[str, Depends(token)],address_id: UUID, session: sessionDepends, address: AddressCreate):
    user = await auth_service.get_current_user(token, session)
    try:
        address_uuid = to_uuid(address_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    address_check = await  useraddress_service.get_address_by_id(session, address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    if user.id != address_check.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this address")
    
    address_update = await useraddress_service.update_address(session, address_uuid, address)
    if not address_update:
        return HTTPException(status_code=404, detail="Address not found")
    
    return address_update


@router.put("/{address_id}/set-default")
async def set_default_address(address_id: UUID, session: sessionDepends):
    try:
        address_uuid = to_uuid(address_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    address = await useraddress_service.set_default_address(address_uuid, session)
    if not address:
        raise HTTPException(status_code=404, detail="address not found")
    return  address