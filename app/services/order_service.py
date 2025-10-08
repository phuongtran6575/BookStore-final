from datetime import datetime
import os
from uuid import UUID
from sqlmodel import Session, select
import stripe

from repositories import useraddress_repository
from repositories import order_repository
from models.bookstore_models import Addresses, OrderItems, Orders, Payments, Users
from schema.order_schema import OrderCreate, OrderItemCreate, OrderStatus, PaymentCreate, PaymentMethod, PaymentStatus, ShippingMethod

async def get_order_by_session_id(session_id: str, session: Session ):
    # Lấy Stripe session
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    # Tìm order tương ứng với session_id hoặc customer_email
    order = session.exec(select(Orders).where(Orders.stripe_session_id == session_id)).first()

    if not order:
        raise ValueError("Not Found")
    # Có thể cập nhật trạng thái nếu thanh toán thành công
    if checkout_session.payment_status == "paid":
        order.status = OrderStatus.PAID
        session.add(order)
        session.commit()
        session.refresh(order)

    # Reuse lại hàm get_order_by_id đã có
    return get_order_by_id(session, order.id)



async def checkout(order_data: OrderCreate, session: Session):
    if not order_data.items:
        raise ValueError("Not Found")

    # 1️⃣ Tính tổng tiền
    total_amount = sum(item.price * item.quantity for item in order_data.items)

    # 2️⃣ Tạo Orders
    order = Orders(
        user_id=None,  # có thể lấy từ current_user
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        customer_phone=order_data.customer_phone,
        shipping_address=order_data.shipping_address,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
        payment_method=PaymentMethod(order_data.payment_method),
        shipping_method=ShippingMethod(order_data.shipping_method),
        created_at=datetime.utcnow()
    )
    session.add(order)
    session.flush()  # để có order.id

    # 3️⃣ Thêm OrderItems
    for item in order_data.items:
        session.add(OrderItems(
            image_url=item.image,
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            subtotal=item.price * item.quantity
        ))

    # 4️⃣ Tạo Payments (pending)
    payment = Payments(
        order_id=order.id,
        transaction_id=None,
        amount=total_amount,
        status=PaymentStatus.PENDING,
        method=PaymentMethod(order_data.payment_method)
    )
    session.add(payment)
    session.commit()
    session.refresh(order)

    # 5️⃣ Nếu là COD → hoàn tất tại đây
    if order_data.payment_method == PaymentMethod.COD:
        order.status = OrderStatus.PENDING  # chờ xác nhận
        session.commit()
        return {
            "message": "Order created successfully (COD)",
            "order_id": str(order.id),
            "payment_method": "COD",
            "status": order.status,
            "total_amount": total_amount
        }

    # 6️⃣ Nếu là STRIPE → trả về order_id cho FE gọi tiếp /payments/stripe/create-checkout-session
    if order_data.payment_method == PaymentMethod.STRIPE:
        return {
            "message": "Order created successfully (Stripe)",
            "order_id": str(order.id),
            "payment_method": "STRIPE",
            "next_step": "/payments/stripe/create-checkout-session"
        }

    return {"order_id": str(order.id), "status": order.status, "total_amount": total_amount}

async def create_order(session: Session, order: OrderCreate):
    return await order_repository.create_order(session, order)

async def get_order_by_id(session: Session, order_id: UUID):
    return await order_repository.get_order_by_id(session, order_id)

async def get_list_orders(session: Session):   
    return await order_repository.get_list_orders(session)

async def add_items_to_order(session: Session, item: OrderItemCreate,):
    return await order_repository.add_items_to_order(session, item)
    

async def create_payments(session: Session, payment: PaymentCreate, order_id: UUID):
    return await order_repository.create_payment(session, payment, order_id)