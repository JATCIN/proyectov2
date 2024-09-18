# create_tables.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, Base

async def create_tables():
    async with engine.begin() as conn:
        # Crear las tablas en la base de datos
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())