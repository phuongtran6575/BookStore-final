from fastapi import APIRouter
from database.sqlite_database import sessionDepends

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def login():
    return

@router.post("register")
async def register(session: sessionDepends):
    return