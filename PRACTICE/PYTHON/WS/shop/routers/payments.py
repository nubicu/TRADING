from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth_utils import get_current_user
import os, json, httpx
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")

PAYPAL_BASE = "https://api-m.sandbox.paypal.com" if PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

def create_order_from_cart(user_id: int, shipping_address: str, payment_method: str, payment_id: str, db: Session):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Coșul este gol")
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    order = models.Order(
        user_id=user_id,
        total=total,
        status="paid",
        payment_method=payment_method,
        payment_id=payment_id,
        shipping_address=shipping_address
    )
    db.add(order)
    db.flush()
    
    for item in cart_items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)
        # Scade stoc
        item.product.stock -= item.quantity
    
    # Goleste cosul
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    db.refresh(order)
    return order

# =================== STRIPE ===================

@router.post("/stripe/create-intent")
async def create_stripe_payment_intent(
    checkout: schemas.CheckoutRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Coșul este gol")
    
    total_ron = sum(item.product.price * item.quantity for item in cart_items)
    amount_bani = int(total_ron * 100)  # Stripe foloseste subdiviziuni
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.stripe.com/v1/payment_intents",
            auth=(STRIPE_SECRET_KEY, ""),
            data={
                "amount": amount_bani,
                "currency": "ron",
                "metadata[user_id]": str(current_user.id),
                "metadata[shipping_address]": checkout.shipping_address,
            }
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Eroare la crearea plății Stripe")
    
    intent = response.json()
    return {
        "client_secret": intent["client_secret"],
        "amount": total_ron,
        "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY")
    }

@router.post("/stripe/confirm")
async def confirm_stripe_payment(
    data: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment_intent_id = data.get("payment_intent_id")
    shipping_address = data.get("shipping_address")
    
    order = create_order_from_cart(current_user.id, shipping_address, "stripe", payment_intent_id, db)
    return {"message": "Plată confirmată", "order_id": order.id}

# =================== PAYPAL ===================

async def get_paypal_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE}/v1/oauth2/token",
            auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
            data={"grant_type": "client_credentials"}
        )
    return response.json().get("access_token")

@router.post("/paypal/create-order")
async def create_paypal_order(
    checkout: schemas.CheckoutRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Coșul este gol")
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    token = await get_paypal_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE}/v2/checkout/orders",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {"currency_code": "RON", "value": f"{total:.2f}"},
                    "description": f"Comanda ShopAll - User {current_user.id}"
                }]
            }
        )
    
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=400, detail="Eroare PayPal")
    
    order_data = response.json()
    return {"paypal_order_id": order_data["id"], "amount": total}

@router.post("/paypal/capture")
async def capture_paypal_order(
    data: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    paypal_order_id = data.get("paypal_order_id")
    shipping_address = data.get("shipping_address")
    
    token = await get_paypal_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYPAL_BASE}/v2/checkout/orders/{paypal_order_id}/capture",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
    
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=400, detail="Eroare la capturarea plății PayPal")
    
    order = create_order_from_cart(current_user.id, shipping_address, "paypal", paypal_order_id, db)
    return {"message": "Plată confirmată", "order_id": order.id}