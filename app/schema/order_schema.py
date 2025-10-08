# Orders
from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel

from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"     # Đang chờ xử lý
    PAID = "paid"           # Thanh toán thành công
    FAILED = "failed"       # Thanh toán thất bại
    REFUNDED = "refunded"   # Đã hoàn tiền


class OrderStatus(str, Enum):
    PENDING = "pending"         # Vừa tạo, chưa thanh toán
    PAID = "paid"               # Đã thanh toán (hoặc COD xác nhận)
    PROCESSING = "processing"   # Đang chuẩn bị hàng
    SHIPPED = "shipped"         # Đã giao cho đơn vị vận chuyển
    DELIVERED = "delivered"     # Đã giao thành công
    CANCELLED = "cancelled"     # Đã hủy


class PaymentMethod(str, Enum):
    STRIPE = "STRIPE"
    COD = "COD"
    BANK = "BANK"
    MOMO = "MOMO"
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
