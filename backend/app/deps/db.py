# backend\app\deps\db.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

# Dependencia de Base de Datos (ASÍNCRONA)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit explícito después de cada operación
        except Exception as e:
            await session.rollback()  # Rollback en caso de error
            raise e
        