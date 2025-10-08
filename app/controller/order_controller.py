from uuid import UUID
from fastapi import APIRouter, HTTPException
from core.helper import to_uuid
from schema.order_schema import OrderCreate, OrderItemCreate, PaymentCreate
from services import order_service
from database.sqlite_database import sessionDepends
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/orders/checkout-success")
async def get_order_by_session_id(session: sessionDepends, session_id: str):
    order = await order_service.get_order_by_session_id(session_id, session)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return await order_service.get_order_by_session_id(session_id, session)

@router.get("/")
async def get_list_orders(session: sessionDepends):
    return await order_service.get_list_orders(session)

@router.post("/checkout")
async def checkout(order_create: OrderCreate, session: sessionDepends):
    
    order = await order_service.checkout( order_create, session)   
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/{order_id}")
async def get_order_by_id(session: sessionDepends, order_id: UUID | str):
    try:
        order_uuid = to_uuid(order_id) 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    order = await order_service.get_order_by_id(session, order_uuid)    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/")
async def create_order(session: sessionDepends,order: OrderCreate):
    return  await order_service.create_order(session, order)

@router.post("/add_item")
async def add_items_to_order(session: sessionDepends, orderitem: OrderItemCreate):
    
    items = await order_service.add_items_to_order(session, orderitem)
    return items





