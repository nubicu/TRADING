from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth_utils import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def get_profile(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_profile(data: schemas.UserUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if data.full_name:
        user.full_name = data.full_name
    if data.phone:
        user.phone = data.phone
    if data.address:
        user.address = data.address
    db.commit()
    db.refresh(user)
    return user