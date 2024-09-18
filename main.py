from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from models import User
from schemas import UserCreate
from fastapi.responses import RedirectResponse

DATABASE_URL = "postgresql+asyncpg://proyecto_user:u7UC5KMyyivMpJ8oWmPODt0DABU0h9wm@dpg-crk7qkm8ii6s73ej2ep0-a.oregon-postgres.render.com/proyecto_db_c7i9"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hash de contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

@app.get("/register/")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
async def register_user(
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(User).filter(User.email == email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = hash_password(password)
        new_user = User(email=email, full_name=full_name, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()

        # Redirige al usuario a la página de inicio de sesión con un mensaje
        response = RedirectResponse(url="/?message=Registration+successful", status_code=status.HTTP_302_FOUND)
        return response

@app.get("/")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token/")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    async with db as session:
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

        # Aquí puedes generar un token o manejar la sesión
        return {"message": "Login successful"}