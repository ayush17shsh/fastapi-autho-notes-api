from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.security import hash_password, verify_password
from app.jwt import create_access_token
from app.deps import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router = APIRouter(
    prefix="/user/db",
    tags=["User"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.UserDB(
        name=user.name,
        age=user.age,
        password=hash_password(user.password)  # ✅ bcrypt here
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "age": new_user.age
    }



@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.UserDB).filter(
        models.UserDB.name == form_data.username
    ).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.name}

    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

@router.get("/me")
def read_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.UserDB).filter(
        models.UserDB.name == current_user
    ).first()
    
    return {
        "id": user.id,
        "name": user.name,
        "age": user.age
    }


    

@router.get("/", response_model=List[UserResponse])
def get_user(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.UserDB).all()