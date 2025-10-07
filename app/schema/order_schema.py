# Orders
from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"           # mới tạo, chưa xử lý
    PROCESSING = "processing"     # đang chuẩn bị hàng
    SHIPPED = "shipped"           # đã giao cho đơn vị vận chuyển
    DELIVERED = "delivered"       # đã giao thành công
    CANCELLED = "cancelled"       # đã hủy

class PaymentMethod(str, Enum):
    STRIPE = "STRIPE"
    COD = "COD"
    BANK = "BANK"
    MOMO = "MOMO"  # nếu bạn có tích hợp
    VNPAY = "VNPAY"


class ShippingMethod(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    GHTK = "ghtk"
    GHN = "ghn"

class OrderItemCreate(BaseModel):
    image: str
    product_id: UUID
    quantity: int
    price: float


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    payment_method: str
    shipping_method: str
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    image: str
    product_id: UUID
    quantity: int
    price: float
    subtotal: float

class OrderRead(BaseModel):
    id: UUID
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    payment_method: str
    shipping_method: str
    total_amount: float
    status: str
    items: List[OrderItemRead] = []


# Payments
class PaymentCreate(BaseModel):
    amount: float
    method: str

class PaymentRead(BaseModel):
    id: UUID
    amount: float
    status: str
    method: str
    created_at: datetime
