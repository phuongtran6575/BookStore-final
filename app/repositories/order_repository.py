from typing import List
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from schema.order_schema import OrderCreate, OrderItemCreate, OrderItemRead, OrderRead, OrderStatus, PaymentCreate, PaymentMethod, PaymentStatus
from models.bookstore_models import OrderItems, Orders, Payments


async def create_order(session: Session, order: OrderCreate):
    try:
        # 1️⃣ Tạo đơn hàng
        order_data = Orders(**order.model_dump())

        # ✅ Set trạng thái ban đầu theo phương thức thanh toán
        if order.payment_method == PaymentMethod.COD:
            order_data.status = OrderStatus.PROCESSING  # COD => chuẩn bị giao luôn
        else:
            order_data.status = OrderStatus.PENDING  # Stripe, MoMo, v.v. => chờ thanh toán

        session.add(order_data)
        session.commit()
        session.refresh(order_data)

        # 2️⃣ Tạo bản ghi thanh toán
        payment = Payments(
            order_id=order_data.id,
            amount=order_data.total_amount,
            method=PaymentMethod(order.payment_method),
            status=PaymentStatus.PENDING
        )
        session.add(payment)
        session.commit()
        session.refresh(payment)

        # 3️⃣ Nếu là Stripe, trả về link thanh toán
        if order.payment_method == PaymentMethod.STRIPE:
            return {
                "order_id": str(order_data.id),
                "payment_method": order.payment_method,
                "status": order_data.status,
                "redirect_to": "/payment/stripe"
            }

        # 4️⃣ Nếu là COD → trả kết quả ngay, không cần redirect Stripe
        return {
            "order_id": str(order_data.id),
            "payment_method": order.payment_method,
            "status": order_data.status
        }

    except Exception as e:
        session.rollback()
        raise ValueError("Not Found")


from sqlmodel import Session, select
from uuid import UUID

async def get_order_by_id(session: Session, order_id: UUID) -> OrderRead:
    # Truy vấn Order + OrderItems
    statement = (
        select(Orders, OrderItems)
        .join(OrderItems, isouter=True)
        .where(Orders.id == order_id)
    )
    results = session.exec(statement).all()

    if not results:
        raise ValueError("Order not found")

    order = results[0][0]
    order.items = [item for _, item in results if item is not None]

    # Chuyển Order -> OrderRead
    return OrderRead(
        id=order.id,
        customer_email=order.customer_email,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        shipping_method=order.shipping_method,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItemRead(
                image= i.image_url,
                product_id=i.product_id,
                quantity=i.quantity,
                price=i.price,
                subtotal=i.subtotal
            )
            for i in order.items
        ]
    )

async def get_list_orders(session: Session):
    statement = select(Orders)
    results = session.exec(statement).all()
    return results

async def add_items_to_order(session: Session, item: OrderItemCreate,):
    subtotal = item.quantity * item.price
    db_item = OrderItems(**item.model_dump(), subtotal=subtotal)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
    

async def create_payment(session: Session, payment: PaymentCreate, order_id: UUID):
    db_payment = Payments(
        order_id=order_id,
        amount=payment.amount,
        method=PaymentMethod(payment.method),
        status=PaymentStatus("pending")
    )
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment