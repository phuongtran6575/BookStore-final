import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List
from uuid import UUID
from stripe import SignatureVerificationError

from sqlmodel import select
import stripe

from models.bookstore_models import Orders, Payments
from schema.order_schema import OrderStatus, PaymentMethod, PaymentStatus
from database.sqlite_database import sessionDepends
from pydantic import BaseModel

load_dotenv()
print("🔑 Stripe Key:", os.getenv("STRIPE_SECRET_KEY"))

router = APIRouter(prefix="/payments", tags=["Payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

class StripeCheckoutRequest(BaseModel):
    order_id: UUID
    # có thể truyền thêm metadata tùy bạn muốn: user_id, email,...

@router.post("/stripe/create-checkout-session")
def create_stripe_checkout(session_req: StripeCheckoutRequest, session: sessionDepends):
    # 1️⃣ Kiểm tra order
    order = session.get(Orders, session_req.order_id)
    if not order:
        raise HTTPException(404, "Order not found")

    # 2️⃣ Tạo bản ghi payment (pending)
    payment = Payments(
        order_id=order.id,
        amount=order.total_amount,
        status=PaymentStatus.PENDING,
        method=PaymentMethod.STRIPE
    )
    session.add(payment)
    session.commit()

    # 3️⃣ Tạo Stripe Checkout Session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",  # ⚠️ Stripe không hỗ trợ VND
                    "unit_amount": int(order.total_amount * 100 / 25000),  # quy đổi sang USD
                    "product_data": {
                        "name": f"Order {order.id}",
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url = "http://localhost:5173/checkoutsuccess?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourfrontend.com/cancel?session_id={CHECKOUT_SESSION_ID}",
            metadata={
                "order_id": str(order.id),
                "payment_id": str(payment.id)
            }
        )

        return JSONResponse({
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        })

    except Exception as e:
        import traceback
        print("🔥 Stripe Error:", traceback.format_exc())  # 👉 thêm dòng này
        raise HTTPException(400, f"Stripe error: {e}")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, session: sessionDepends):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    data = event["data"]["object"]

    print("🔔 Stripe Event:", event_type)

    if event_type == "checkout.session.completed":
        order_id = data.get("metadata", {}).get("order_id")
        if not order_id:
            return {"received": True}

        order = session.get(Orders, order_id)
        payment = session.exec(select(Payments).where(Payments.order_id == order_id)).first()
        if order and payment:
            order.status = OrderStatus.PAID
            payment.status = PaymentStatus.PAID
            payment.transaction_id = data.get("payment_intent")
            session.commit()

    elif event_type == "payment_intent.payment_failed":
        intent = data
        order_id = intent.get("metadata", {}).get("order_id")
        payment = session.exec(select(Payments).where(Payments.order_id == order_id)).first()
        if payment:
            payment.status = PaymentStatus.FAILED
            session.commit()

    elif event_type == "charge.refunded":
        charge = data
        order_id = charge.get("metadata", {}).get("order_id")
        payment = session.exec(select(Payments).where(Payments.order_id == order_id)).first()
        if payment:
            payment.status = PaymentStatus.REFUNDED
            session.commit()

    return {"received": True}

