from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    old_price: Optional[float]
    stock: int
    image_url: Optional[str]
    images: Optional[str]
    category: Optional[CategoryOut]
    rating: float
    reviews_count: int
    is_featured: bool
    class Config:
        from_attributes = True

class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    class Config:
        from_attributes = True

class OrderItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    price: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total: float
    status: str
    payment_method: str
    shipping_address: str
    created_at: datetime
    items: List[OrderItemOut]
    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    payment_method: str  # "stripe" or "paypal"
    shipping_address: str

class StripePaymentIntent(BaseModel):
    amount: int
    currency: str = "ron"