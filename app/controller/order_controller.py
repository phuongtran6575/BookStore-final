from fastapi import APIRouter

router = APIRouter()

from sqlmodel import Session

@router.post("/")
async def create_order(session: Session):
    return

@router.get("/")
async def get_order(session: Session):
    return

@router.get("/")
async def get_list_orders(session: Session):
    return

@router.post("/")
async def add_items_to_order(session: Session):
    return

@router.post("/")
async def create_paymanets(session: Session):
    return 