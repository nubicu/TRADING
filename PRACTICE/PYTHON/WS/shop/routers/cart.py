from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas
from auth_utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.CartItemOut])
def get_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()

@router.post("/add")
def add_to_cart(product_id: int, quantity: int = 1, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produs negăsit")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Stoc insuficient")
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == product_id
    ).first()
    if existing:
        existing.quantity += quantity
    else:
        cart_item = models.CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
    db.commit()
    return {"message": "Produs adăugat în coș"}

@router.put("/update/{item_id}")
def update_cart(item_id: int, quantity: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item negăsit")
    if quantity <= 0:
        db.delete(item)
    else:
        item.quantity = quantity
    db.commit()
    return {"message": "Coș actualizat"}

@router.delete("/remove/{item_id}")
def remove_from_cart(item_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item negăsit")
    db.delete(item)
    db.commit()
    return {"message": "Produs eliminat din coș"}

@router.delete("/clear")
def clear_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Coș golit"}