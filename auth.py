from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas, database

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register/")
async def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_model = models.User(
        fullname=user.fullname,
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(user_model)
    await db.commit()
    return {"message": "User registered successfully"}

@router.post("/login/")
async def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = await db.execute(
        "SELECT * FROM users WHERE username = :username", {"username": user.username}
    )
    db_user = db_user.fetchone()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"message": "Login successful"}