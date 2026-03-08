from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas
from seed_data import seed_products

router = APIRouter()

# !! /seed TREBUIE sa fie INAINTEA /{product_id} !!
@router.get("/seed")  # schimbat din POST in GET
def seed(db: Session = Depends(get_db)):
    seed_products(db)
    return {"message": "Date seed adăugate cu succes"}

@router.get("/categories", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.get("/", response_model=List[schemas.ProductOut])
def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    featured: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.join(models.Category).filter(models.Category.slug == category)
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if featured is not None:
        query = query.filter(models.Product.is_featured == featured)
    return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Produs negăsit")
    return product