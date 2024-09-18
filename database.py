from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://proyecto_user:u7UC5KMyyivMpJ8oWmPODt0DABU0h9wm@dpg-crk7qkm8ii6s73ej2ep0-a.oregon-postgres.render.com/proyecto_db_c7i9"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session