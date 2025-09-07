from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# =========================
# PRODUCT SCHEMAS
# =========================

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    sku: str
    price: float
    sale_price: Optional[float] = None
    stock_quantity: int = 0
    page_count: Optional[int] = None
    cover_type: Optional[str] = None
    publication_date: Optional[date] = None


class (ProductBase):
    pass  # giữ nguyên vì tất cả field đã có trong Base


class ProductRead(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    sale_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    page_count: Optional[int] = None
    cover_type: Optional[str] = None
    publication_date: Optional[date] = None
