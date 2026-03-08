from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth_utils import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Verifica daca emailul exista deja
        existing = db.query(models.User).filter(models.User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email deja înregistrat")
        
        # Creeaza userul
        db_user = models.User(
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Genereaza token
        token = create_access_token({"sub": db_user.email})
        return {"access_token": token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Eroare server: {str(e)}")

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Email sau parolă incorectă")
        
        token = create_access_token({"sub": db_user.email})
        return {"access_token": token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare server: {str(e)}")